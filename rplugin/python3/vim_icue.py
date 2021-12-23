import neovim
import pynvim
from cuesdk import CueSdk
import logging
import time

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
        self.vim.command('au InsertEnter * VimICUEInsertModeOn')
        self.vim.command('au InsertLeave * VimICUEInsertModeOff')
        self.vim.out_write("vim-icue is ready!\n")
        self.colors = self.get_available_colors()

    @pynvim.command("VimICUELedsCount")
    def get_available_colors(self):
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
        for di in range(len(self.colors)):
            device_leds = self.colors[di]
            for led in device_leds:
                device_leds[led] = (0, 1)
            self.cue.set_led_colors_buffer_by_device_index(di, device_leds)
            time.sleep(1)

    @pynvim.command("VimICUEInsertModeOff")
    def insert_mode_off(self):
        pass


