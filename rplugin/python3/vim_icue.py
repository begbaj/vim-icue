import datetime
import traceback
from threading import Thread
import pynvim
from cuesdk import CueSdk


@pynvim.plugin
class VimICUE(object):
    def __init__(self, vim: pynvim.Nvim):
        try:
            self.vim = vim
            self.aicue = AsyncICUE(vim)
            self.connect()
        except Exception as error:
            self.aicue.nvim_print(f"{error}")

    @pynvim.function("VimICUEConnect")
    def connect(self, handler=None):
        self.aicue.connect()
        layouts = {}
        self.aicue.nvim_print("FINO A QUI TUTTO BENE")
        for m in ["normal", "insert", "command"]:
            layouts[m] = self.aicue.get_layout(m)
        self.aicue.nvim_print("CI SIAMO")
        self.aicue.cache_layouts(layouts)

    @pynvim.command("VimICUEStop")
    def stop(self):
        self.aicue.stop()

    @pynvim.command("VimICUEPlay")
    def play(self):
        self.aicue.play()

    @pynvim.function("VimICUEDisconnect")
    def disconnect(self, handler=None):
        self.aicue.disconnect()

    @pynvim.function("VimICUEModeChange")
    def mode_change(self, args):
        mode = args[0]
        if mode == 'n':
            self.aicue.mode = 'normal'
        elif mode == 'i':
            self.aicue.mode = 'insert'
        elif mode == 'c':
            self.aicue.mode = 'command'
        else:
            return
        #self.aicue.refill()
        self.aicue.load_cached_layout()
        self.aicue.can_update = True


class AsyncICUE:
    def __init__(self, nvim: pynvim.Nvim):
        self.cue = CueSdk()
        self.nvim = nvim
        self.mode = 'normal'
        self.leds = []
        self.connected = False
        self.key_queue = []
        self.updater = Thread(target=self.layout_updater)
        self.is_close = False
        self.can_update = False
        self.cached_layouts = {}
        # self.refill()
        # self.play()

    def connect(self):
        if not self.cue.connect():
            err = self.cue.get_last_error()
            self.nvim.out_write(f"Handshake failed: {err}\n")
            return False
        else:
            self.leds = self.leds_count()
            self.cue.request_control()
            return True

    def disconnect(self):
        if self.connected:
            self.stop()
            self.updater.join()
            self.cue.release_control()
            self.cue = None
            self.connected = False
            self.key_queue = []

    def play(self):
        self.is_close = False
        if not self.updater.is_alive():
            self.updater.start()
        self.cue.request_control()

    def stop(self):
        self.is_close = True
        if self.updater.is_alive():
            self.updater.join()
        self.cue.release_control()

    def leds_count(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        # self.vim.out_write(f"There are {len(leds)} leds available\n")
        return leds

    def nvim_print(self, message, auto_newline=True):
        if auto_newline:
            self.nvim.out_write(message + "\n")
        else:
            self.nvim.out_write(message)

    def cache_layouts(self, layouts: {}):
        """
        Load to memory a list of layouts to fast switch from one another
        """
        self.cached_layouts = layouts

    def get_layout(self, mode):
        key_layout = []
        for di in range(len(self.leds)):
            device_leds = self.leds[di]
            # start = datetime.datetime.now()
            for led in device_leds:
                # per aumentare la velcoita bisogna agire in questo pezzo i codice
                # self.key_queue.append([self.get_color(self.mode, led.value), led, di])
                key_layout.append([self.nvim.call('VimICUEGetKeyColorById', mode, led.value), led, di])
                # self.nvim_print(f"{datetime.datetime.now() - start}")
        return key_layout

    def refill(self):
        #key_queue = []
        self.nvim_print(f"CHIAMATA con modo {self.mode}")

        #self.key_queue = key_queue.copy()
        self.can_update = True

    def load_cached_layout(self, layout_name=None):
        if layout_name is not None:
            self.key_queue = self.cached_layouts[layout_name].copy()
        else:
            self.key_queue = self.cached_layouts[self.mode].copy()

    def get_color(self, mode, id):
        return self.VimICUEGetKeyColor(mode, self.VimICUEGetKeyName(id))

    def VimICUEGetKeyName(self, id):
        return self.nvim.call('VimICUEGetKeyName', id)

    def VimICUEGetKeyColor(self, mode, keyname):
        return self.nvim.call('VimICUEGetKeyColor', mode, keyname)

    def layout_updater(self):
        while not self.is_close:
                try:
                    if not len(self.key_queue) == 0 and self.can_update:
                        self.can_update = False
                        leds = self.leds
                        while not len(self.key_queue) == 0:
                            key = self.key_queue.pop(0)
                            color = key[0]
                            led = key[1]
                            device = key[2]
                            if len(color) == 2:
                                leds[device][led] = (int(color[0]), int(color[1]))
                            else:
                                leds[device][led] = (int(color[0]), int(color[1]), int(color[2]))
                            #self.nvim.async_call(self.nvim_print, f"{color}")
                            if len(self.key_queue) == 0:
                                self.cue.set_led_colors_buffer_by_device_index(device, leds[device])

                        self.cue.set_led_colors_flush_buffer()
                except Exception as err:
                    self.nvim.async_call(self.nvim_print, f"Error {traceback.format_exc()}")
                    self.key_queue = []
        self.nvim.async_call(self.nvim_print, "Updater close")

