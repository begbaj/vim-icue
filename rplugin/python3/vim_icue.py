import datetime
import traceback
from threading import Thread
import pynvim
from cuesdk import CueSdk


@pynvim.plugin
class VimICUE(object):
    def __init__(self, nvim: pynvim.Nvim):
        # enable __nvim_print function
        self.print_enabled = True
        self.mode = 'normal'
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

        self.connect()

    @pynvim.function("VimICUERefresh")
    def refresh(self, mode):
        nmode = ''.join(mode)
        if self.mode != nmode:
            self.mode = nmode
            self.can_update = True
            self.__refresh_key_queue(self.mode)
        return

    @pynvim.command("VimICUEConnect")
    def connect(self):
        if not self.cue.connect():
            err = self.cue.get_last_error()
            self.nvim.out_write(f"Handshake failed: {err}\n")
            return False
        else:
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
        self.refresh(self.mode)

    @pynvim.command("VimICUEStop")
    def stop(self):
        self.is_close = True
        if self.updater.is_alive():
            self.updater.join()
        self.cue.release_control()

    def __leds_count(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        return leds

    def __nvim_print(self, message, auto_newline=True):
        if self.print_enabled:
            if auto_newline:
                self.nvim.out_write(message + "\n")
            else:
                self.nvim.out_write(message)

    def __get_layout(self, mode):
        """
        Returns a list that Updater can process
        [[colors], led_to_set_colors_to, device_in_which_led_is_located]
        """
        key_layout = []
        self.__nvim_print(f"Getting layout for mode {mode}")
        for di in range(len(self.leds)):
            device_leds = self.leds[di]
            keys = self.nvim.vars['vimicue_keys']
            theme = self.nvim.vars['vimicue_theme']
            for led in device_leds:
                if keys[str(led.value)] in theme[mode]:
                    nl = [theme[mode][keys[str(led.value)]], led, di]
                else:
                    nl = [theme[mode]['default'], led, di]
                key_layout.append(nl)
        self.__nvim_print(f"Completed for {mode}")
        return key_layout

    def __load_cached_layout(self):
        """
        Reload layouts to cache
        """
        self.__nvim_print(f"Caching layout...")
        self.cached_layouts = {}
        for mode in self.nvim.vars['vimicue_theme'].keys():
            self.cached_layouts[mode] = self.__get_layout(mode)
        self.__nvim_print(f"Caching completed")

    def __refresh_key_queue(self, mode):
        """
        Refill key queue
        """
        self.__nvim_print(f"Current list of cached layouts: {self.cached_layouts}")
        self.__nvim_print(f"Refreshing key_queue...")
        self.key_queue = self.cached_layouts[mode].copy()
        self.__nvim_print(f"Refreshing completed")

    def layout_updater(self):
        while not self.is_close:
            try:
                if len(self.key_queue) != 0 and self.can_update:
                    self.nvim.async_call(self.__nvim_print, "UPDATER: key_queue has been refreshed")
                    self.can_update = False
                    leds = self.leds
                    while len(self.key_queue) != 0:
                        self.nvim.async_call(self.__nvim_print, f"{self.key_queue[0]}")
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
                self.nvim.async_call(self.__nvim_print, f"Error {err} \n {traceback.format_exc()}")
                self.key_queue = []
