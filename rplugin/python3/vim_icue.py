import datetime
import traceback
from threading import Thread
import pynvim
from cuesdk import CueSdk


@pynvim.plugin
class VimICUE(object):
    def __init__(self, vim: pynvim.Nvim):
        self.vim = vim
        self.aicue = AsyncICUE(vim)
        self.connect()

    @pynvim.function("VimICUEConnect")
    def connect(self, handler=None):
        self.aicue.connect()

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
        self.aicue.refill()


class AsyncICUE:
    def __init__(self, nvim: pynvim.Nvim):
        self.cue = CueSdk()
        self.nvim = nvim
        self.mode = 'normal'
        self.leds = []
        self.connected = self.connect()
        self.key_queue = []
        self.updater = Thread(target=self.layout_updater)
        self.is_close = False
        self.can_update = False
        self.refill()
        self.play()

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
        self.updater.start()

    def stop(self):
        self.is_close = True
        self.updater.join()

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

    def refill(self):
        self.key_queue = []
        for di in range(len(self.leds)):
            device_leds = self.leds[di]
            start = datetime.datetime.now()
            for led in device_leds:
                # per aumentare la velcoita bisogna agire in questo pezzo i codice
                self.key_queue.append([self.get_color(self.mode, led.value), led, di])
                self.nvim_print(f"{datetime.datetime.now() - start}")
            self.can_update = True


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

