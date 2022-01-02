import traceback
from threading import Thread

import cuesdk
import pynvim
from cuesdk import CueSdk


@pynvim.plugin
class VimICUE(object):
    def __init__(self, nvim: pynvim.Nvim):
        # enable __nvim_print function
        self.allow_queue = False
        self.updater_is_on = False
        self.print_enabled = False
        self.mode = 'default'
        self.connected = False
        self.leds = []
        self.key_queue = []
        self.is_close = False
        self.can_update = False
        self.cached_layouts = {}

        # cuesdk default values
        self.cue = CueSdk()
        self.nvim = nvim
        self.updater = Thread(target=self.layout_updater)

    @pynvim.function("VimICUERefreshForce")
    def refresh_forced(self, mode):
        if self.connected:
            nmode = ''.join(mode)
            self.mode = nmode
            self.can_update = True
            self.__refresh_key_queue(self.mode)
        return

    @pynvim.function("VimICUERefresh")
    def refresh(self, mode):
        try:
            if self.connected:
                nmode = ''.join(mode)
                if self.mode != nmode:
                    self.mode = nmode
                    self.can_update = True
                    self.__refresh_key_queue(self.mode)
        except Exception as err:
            self.__nvim_print(err)
        return

    @pynvim.command("VimICUEConnect")
    def connect(self):
        if not self.cue.connect():
            self.connected = False
            err = self.cue.get_last_error()
            self.nvim.out_write(f"Handshake failed: {err}\n")
            return False
        else:
            self.connected = True
            self.leds = self.__leds_count()
            self.cue.request_control()
            self.__load_cached_layout()
            return True

    @pynvim.command("VimICUEDisconnect")
    def disconnect(self):
        if self.connected:
            self.stop()
            self.updater.join()
            self.cue.release_control()
            self.cue = None
            self.connected = False
            self.cached_layouts = {}
            self.key_queue = []

    @pynvim.command("VimICUEPlay")
    def play(self):
        self.is_close = False
        if not self.updater.is_alive():
            self.updater = Thread(target=self.layout_updater)
            self.updater.start()
        self.cue.request_control()
        self.refresh_forced(self.mode)

    @pynvim.command("VimICUEStop")
    def stop(self):
        self.is_close = True
        if self.updater.is_alive():
            self.updater.join()
        self.cue.release_control()

    def __leds_count(self):
        leds = list()
        self.cue.get_devices()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        return leds

    def __nvim_print(self, message, auto_newline=True):
        if self.print_enabled:
            if auto_newline:
                self.nvim.call('VimICUEPrintDebug', str(message) + "\n")
            else:
                self.nvim.call('VimICUEPrintDebug', str(message))

    def __get_layout(self, mode):
        """
        Returns a list that Updater can process
        [[colors], led_to_set_colors_to, device_in_which_led_is_located]
        """
        key_layout = []
        self.__nvim_print(f"~Generating layout for mode {mode}")
        # Check for groupings: if any, compile to g:theme
        keys = self.nvim.vars['vimicue_keys']
        theme = self.nvim.vars['vimicue_theme']
        # WORKFLOW EXPLAINED
        # First: check if there are groupings in the theme
        # if sa, substitute the grouping with actual keynames contained in the group
        # Second: get layout per mode
        for di in range(len(self.leds)):
            device_leds = self.leds[di]
            for led in device_leds:
                if mode in theme and keys[str(led.value)] in theme[mode]:
                    nl = [theme[mode][keys[str(led.value)]], led, di]
                elif keys[str(led.value)] in theme['default']:
                    nl = [theme['default'][keys[str(led.value)]], led, di]
                elif mode in theme and 'default' in theme[mode]:
                    nl = [theme[mode]['default'], led, di]
                else:
                    nl = [theme['default']['default'], led, di]
                key_layout.append(nl)

        self.__nvim_print(f"~Layout generated for {mode} mode. This layout contains {len(key_layout)} entries.")
        return key_layout

    def __precompile(self):
        self.__nvim_print("!!!!!Precompiling...")
        theme = self.nvim.vars['vimicue_theme']
        if 'groupings' not in theme:
            return

        groupings = self.nvim.vars['vimicue_theme']['groupings']

        for group in groupings:
            self.__nvim_print(group)
            for mode in theme:
                if mode == "groupings":
                    continue
                for key in theme[mode]:
                    if group == key:
                        for groupkey in groupings[group]:
                            self.__nvim_print(f"MODE: {mode} GROUPKEY: {groupkey} mode_key: {theme[mode][key]}")
                            if groupkey not in theme[mode] and groupkey not in theme["default"]:
                                self.nvim.call("VimICUEAddToTheme", mode, groupkey, theme[mode][key])
                            # self.nvim.vars['vimicue_theme'][mode][groupkey] = theme[mode][key]
                        self.__nvim_print(f"{self.nvim.vars['vimicue_theme'][mode]}")
        self.__nvim_print("!!!!!Precomipling finished.")

    def __load_cached_layout(self):
        """
        Reload layouts to cache
        """
        self.__nvim_print("-------Caching layout...")
        self.cached_layouts = {}
        self.__precompile()
        for mode in self.nvim.vars['vimicue_theme'].keys():
            self.__nvim_print(f"--Caching mode: {mode}")
            self.cached_layouts[mode] = self.__get_layout(mode)
        self.__nvim_print("-------Caching completed")
        self.allow_queue = True
        self.refresh_forced(self.mode)

    def __refresh_key_queue(self, mode):
        """
        Refill key queue
        """
        try:
            if self.allow_queue:
                self.__nvim_print(f"Key queue will contain {len(self.cached_layouts[mode])} entries.")
                self.__nvim_print("Refreshing key_queue...")
                self.key_queue = self.cached_layouts[mode].copy()
                self.__nvim_print("Refreshing completed")
            else:
                self.__nvim_print("Layouts are not ready yet!")
        except KeyError as err:
            self.__nvim_print(f"{mode} not found. Maybe its too early...")

    def layout_updater(self):
        def nprint(message):
            self.nvim.async_call(self.__nvim_print, message)
        nprint("LAYOUT UPDATER LAUNCHED!!")
        if not self.updater_is_on:
            self.updater_is_on = True
            while not self.is_close:
                try:
                    if len(self.key_queue) != 0 and self.can_update:
                        nprint("Loading layout")
                        self.can_update = False
                        leds = self.leds
                        while len(self.key_queue) != 0:
                            #nprint(f"{self.key_queue[0]}")
                            key = self.key_queue.pop(0)
                            color = key[0]
                            led = key[1]
                            di = key[2]
                            if len(color) == 2:
                                leds[0][led] = (int(color[0]), int(color[1]))
                            else:
                                leds[0][led] = (int(color[0]), int(color[1]), int(color[2]))
                            if len(self.key_queue) == 0:
                                self.cue.set_led_colors_buffer_by_device_index(di, leds[di])
                        self.cue.set_led_colors_flush_buffer()
                except Exception as err:
                    nprint("LAYOUT UPDATER STOPPED!!")
                    nprint(f"Error {err} \n {traceback.format_exc()}")
                    self.key_queue = []
            self.updater_is_on = False
        else:
            nprint("WARNING, Updater is already running")
