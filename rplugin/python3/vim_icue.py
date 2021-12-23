import neovim
import pynvim
from cuesdk import CueSdk
import logging

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim: neovim.Nvim):
        #logging.basicConfig(level=logging.DEBUG)
        self.vim = vim
        self.vim.out_write("vim-icue is initializing...\n")
        self.cue = CueSdk()
        self.connected = self.cue.connect()
        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return
        self.insert_mode_on = self.vim.subscribe("InsertEnter")
        self.insert_mode_off = self.vim.subscribe("InsertLeave")
        self.vim.out_write("vim-icue is ready!\n")
        self.leds = self.get_available_leds()

    @pynvim.command("VimICUELedsCount")
    def get_available_leds(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        self.vim.out_write(f"There are {len(leds)} leds available\n")
        return leds

    @pynvim.command("VimICUEInsertModeOn")
    def insert_mode_on(self):
        self.vim.out_write("Insert keyboard layout enabled\n")
        for led in self.leds:
            led = (1, 1, 1)

    @pynvim.command("VimICUEInsertModeOff")
    def insert_mode_off(self):
        pass


