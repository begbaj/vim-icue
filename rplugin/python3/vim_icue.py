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
        self.vim.out_write("vim-icue is initializing...\n")
        self.cue = CueSdk()
        self.connected = False
        self.vim.command_output("VimICUEConnect")
        self.mode = "normal"
        self.key_ids = ['klesc', 'klf1', 'klf2', 'klf3', 'klf4', 'klf5', 'klf6', 'klf7', 'klf8', 'klf9', 'klf10',
                        'klf11', 'klf12', 'kl1', 'kl2', 'kl3', 'kl4', 'kl5', 'kl6', 'kl7', 'kl8', 'kl9', 'kl0', 'klq',
                        'klw', 'kle', 'klr', 'klt', 'kly', 'klu', 'kli', 'klo', 'klp', 'kla', 'kls', 'kld', 'klf',
                        'klg', 'klh', 'klj', 'kl', 'kl', 'kll', 'klz', 'klx', 'klc', 'klv', 'klb', 'kln', 'klm',
                        'klsemic', 'klperiod', 'klcomma', 'klslash', 'klbslash', 'klsclosed', 'klsopened', 'klminus',
                        'kleq', 'kltilde', 'kltab', 'klbloc', 'klm', 'klrshift', 'kllshift', 'klrctr', 'kllctrl',
                        'klsuper', 'klalt', 'klspace', 'klenter', 'klup', 'kldown', 'klleft', 'klright']



        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return

        self.vim.command('let g: vimicue_insert_layout = {"default": "0,0,0}')
        self.vim.command('let g: vimicue_normal_layout = {"default": "0,0,0}')
        self.vim.command('let g: vimicue_visual_layout = {"default": "0,0,0}')
        self.vim.command('let g: vimicue_command_layout = {"default": "0,0,0}')

        self.vim.command("nnoremap r :call VimICUEDetectMode('replace')<CR>")
        self.vim.command("nnoremap i :call VimICUEDetectMode('insert')<CR>")
        self.vim.command("nnoremap v :call VimICUEDetectMode('visual')<CR>")
        self.vim.command("nnoremap : :call VimICUEDetectMode('command')<CR>")
        self.vim.command("nnoremap / :call VimICUEDetectMode('search')<CR>")
        self.vim.command("nnoremap ? :call VimICUEDetectMode('reverse_search')<CR>")
        self.vim.command("noremap <esc> :call VimICUEDetectMode('normal')<CR>")
        self.vim.command("noremap <bs> :call VimICUEDetectMode('unknown')<CR>")

        self.vim.out_write("vim-icue is ready!\n")
        self.colors = self.get_available_colors()

    @pynvim.command("VimICUEConnect")
    def cue_connect(self):
        self.connected = self.cue.connect()

    @pynvim.command("VimICUEDisconnect")
    def cue_connect(self):
        self.connected = self.cue.release_control()

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
        new_mode = args
        match self.mode:
            case 'normal':
                self.mode = new_mode
            case _:
                self.vim.out_write("Mode was not changed")
        self.vim.command("VimICUEAutoLayout")



    @pynvim.command("VimICUEAutoLayout")
    def automatic_layout(self):
        match self.mode:
            case 'normal':
                pass
            case 'insert':
                pass
            case 'command':
                pass
            case 'search':
                pass
            case 'reverse_search':
                pass
            case 'visual':
                pass

    @pynvim.command("VimICUEChangeMode")
    def change_mode(self):
        try:
            for di in range(len(self.colors)):
                device_leds = self.colors[di]
                for led in device_leds:
                    if len(device_leds[led]) == 2:
                        if led in self.key_ids:
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


