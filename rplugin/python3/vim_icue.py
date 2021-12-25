import neovim
import pynvim
from cuesdk import CueSdk
from cuesdk.structs import CorsairLedId
import logging
import time

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim: neovim.Nvim):
        """
            NOTES:
            g:vimicue_on_insert_KEYID = (color)
            g:vimicue_on_insert_default = (color)

            g:vimicue_on_normal_KEYID = (color)
            g:vimicue_on_normal_default = (color)

            g:vimicue_on_visual_KEYID = (color)
            g:vimicue_on_visual_default = (color)

            g:vimicue_on_command_KEYID = (color)
            g:vimicue_on_command_default = (color)
        """
        self.vim = vim
        self.vim.out_write("vim-icue is initializing...\n")
        self.mode = "normal"
        self.key_ids = []
        with open("keys.txt", 'r') as fk:
            self.key_ids.append(fk.readline().replace("\n", ''))
        self.cue = CueSdk()
        self.connected = self.cue.connect()
        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return

        self.vim.command("noremap r :call VimICUEDetectMode('replace')<CR>")
        self.vim.command("noremap i :call VimICUEDetectMode('insert')<CR>")
        self.vim.command("noremap v :call VimICUEDetectMode('visual')<CR>")
        self.vim.command("noremap : :call VimICUEDetectMode('command')<CR>")
        self.vim.command("noremap / :call VimICUEDetectMode('search')<CR>")
        self.vim.command("noremap ? :call VimICUEDetectMode('reverse_search')<CR>")
        self.vim.command("noremap <esc> :call VimICUEDetectMode('normal')<CR>")

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

    @pynvim.function("VimICUEDetectMode")
    def detect_mode(self, args):
        self.mode = args


    @pynvim.command("VimICUEAutoLayout")
    def automatic_layout(self):
        mode = ""


    @pynvim.command("VimICUEChangeMode")
    def insert_mode_off(self):
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


