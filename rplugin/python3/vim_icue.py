import neovim
import pynvim
from cuesdk import CueSdk
from cuesdk.structs import CorsairLedId
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
        try:
            for di in range(len(self.colors)):
                device_leds = self.colors[di]
                for led in device_leds:
                    if len(device_leds[led]) == 2:
                        device_leds[led] = (0, 255)
                    if len(device_leds[led]) == 3:
                        device_leds[led] = (0, 255, 0)
                self.cue.set_led_colors_buffer_by_device_index(di, device_leds)
            self.cue.set_led_colors_flush_buffer()
            self.vim.out_write("Insert keyboard layout enabled\n")
        except Exception as e:
            self.vim.err_write(f"Error occured: {e}")


    @pynvim.command("VimICUEInsertModeOff")
    def insert_mode_off(self):
        on_keys = [CorsairLedId.K_J, CorsairLedId.K_K, CorsairLedId.K_L, CorsairLedId.K_H,
                   CorsairLedId.K_W, CorsairLedId.K_Q, CorsairLedId.K_SemicolonAndColon]
        try:
            for di in range(len(self.colors)):
                device_leds = self.colors[di]
                for led in device_leds:
                    if len(device_leds[led]) == 2:
                        if led in on_keys:
                            device_leds[led] = (0, 255)
                        else:
                            device_leds[led] = (0, 50)
                    if len(device_leds[led]) == 3:
                        device_leds[led] = (0, 50, 0)
                self.cue.set_led_colors_buffer_by_device_index(di, device_leds)
            self.cue.set_led_colors_flush_buffer()
            self.vim.out_write("Insert keyboard layout disabled\n")
        except Exception as e:
            self.vim.err_write(f"Error occured: {e}")


