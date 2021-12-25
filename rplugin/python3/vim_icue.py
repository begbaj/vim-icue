import neovim
import pynvim
from cuesdk import CueSdk
from cuesdk.structs import CorsairLedId
import logging
import time

@pynvim.plugin
class VimICUE(object):
    def __init__(self, vim: neovim.Nvim):
        """
            NOTES:
            l:vimicue_insert_layout = { "keyid" : "rgb",
                                        "default" : "rgb" }
            l:vimicue_normal_layout = { "keyid" : "rgb",
                                        "default" : "rgb" }
            l:vimicue_command_layout = { "keyid" : "rgb",
                                        "default" : "rgb" }
            l:vimicue_visual_layout = { "keyid" : "rgb",
                                        "default" : "rgb" }
        """
        self.vim = vim
        self.cue = CueSdk()
        self.connected = False
        self.mode = "normal"
        self.key_ids: dict
        self.key_ids = dict(self.vim.command_output(":echo vimicue_keys"))
        self.cue_connect()
        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return
        self.vim.out_write(f"VimIcue initialized\n")
        self.leds = self.get_available_leds()

    @pynvim.autocmd("VimICUEStart")
    def vim_icue_start(self):
        pass

    @pynvim.command("VimICUEConnect")
    def cue_connect(self):
        self.connected = self.cue.connect()

    @pynvim.command("VimICUEDisconnect")
    def cue_disconnect(self):
        self.connected = self.cue.release_control()

    @pynvim.command("VimICUELedsCount")
    def get_available_leds(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        self.vim.out_write(f"There are {len(leds)} leds available\n")
        return leds

    @pynvim.function("VimICUEDetectMode")
    def detect_mode(self, args):
        new_mode = args[0]
        self.vim.out_write(f"Mode changed to {new_mode}\n")
        # match self.mode:
        #     case 'normal':
        #         self.mode = new_mode
        #
        #     case _:
        #         self.vim.out_write("Mode was not changed\n")
        self.automatic_layout()



    @pynvim.command("VimICUEAutoLayout")
    def automatic_layout(self):
        match self.mode:
            case 'normal':
                self.change_mode()
            case 'insert':
                self.change_mode()
            case 'command':
                self.change_mode()
            case 'search':
                pass
            case 'reverse_search':
                pass
            case 'visual':
                pass

    @pynvim.command("VimICUEChangeMode")
    def change_mode(self):
        try:
            for di in range(len(self.leds)):
                device_leds = self.leds[di]
                for led in device_leds:
                    if len(device_leds[led]) == 2:
                        if led in self.key_ids.values():
                            device_leds[led] = (0, 100)
                        else:
                            device_leds[led] = (0, 50)
                    if len(device_leds[led]) == 3:
                        device_leds[led] = (0, 50, 0)
                self.cue.set_led_colors_buffer_by_device_index(di, device_leds)
            self.cue.set_led_colors_flush_buffer()
            self.vim.out_write("Insert keyboard layout disabled\n")
        except Exception as e:
            self.vim.err_write(f"Error occured: {e}\n")


