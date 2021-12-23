import neovim
from cuesdk import CueSdk
import logging

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim: neovim.Nvim):
        #logging.basicConfig(level=logging.DEBUG)
        self.vim = vim
        self.vim.out_write("vim-icue is initializing...")
        self.cue = CueSdk()
        self.connected = self.cue.connect()
        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}")
            return

        self.leds = self.get_available_leds()

        self.insert_mode_on = self.vim.subscribe("InsertEnter")
        self.insert_mode_off = self.vim.subscribe("InsertLeave")
        self.vim.out_write("vim-icue is ready!")

    @neovim.function("VimICUE")
    def vimicue(self):
        print("prova 1")
        self.vim.out_write("prova 2")


    def get_available_leds(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        return leds

    def insert_mode_on(self):
        for led in self.leds:
            led = (1, 1, 1)

    def insert_mode_off(self):
        pass


