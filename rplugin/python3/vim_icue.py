import pynvim
from cuesdk import CueSdk

@pynvim.plugin
class VimICUE(object):
    def __init__(self, vim: pynvim.Nvim):
        self.vim = vim
        self.cue = CueSdk()
        self.connected = False
        self.mode = "normal"
        self.connect()
        if not self.connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return
        # self.vim.out_write(f"VimIcue initialized\n")
        self.leds = self.leds_count()

    @pynvim.autocmd("VimICUEConnect")
    def connect(self, handler=None):
        if not self.connected:
            # self.vim.out_write(f"connected\n")
            self.connected = self.cue.connect()

    @pynvim.autocmd("VimICUEDisconnect")
    def disconnect(self, handler=None):
        if self.connected:
            # self.vim.out_write(f"disconnected\n")
            self.connected = self.cue.release_control()

    @pynvim.command("VimICUELedsCount")
    def leds_count(self):
        leds = list()
        device_count = self.cue.get_device_count()
        for device_index in range(device_count):
            led_positions = self.cue.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
        # self.vim.out_write(f"There are {len(leds)} leds available\n")
        return leds

    @pynvim.function("VimICUEModeChange")
    def mode_change(self, args):
        self.mode = args[0]
        match self.mode:
            case 'n':
                self.change_mode('normal')
            case 'i':
                self.change_mode('insert')
            case 'c':
                self.change_mode('command')
            case 'search':
                pass
            case 'reverse_search':
                pass
            case 'visual':
                pass
        self.automatic_layout()

    @pynvim.function("VimICUEAutoLayout", sync=True)
    def auto_layout(self, mode):
        self.vim.out_write(f"vimicue_{mode}_layout\n")
        for di in range(len(self.leds)):
            device_leds = self.leds[di]
            for led in device_leds:
                keyname = self.vim.eval(f"vimicue_keys[{led.value}]")
                try:
                    color = self.vim.eval(f"vimicue_{mode}_layout['{keyname}']")
                except:
                    color = self.vim.eval(f"vimicue_{mode}_layout['default']")
                if len(color) == 2:
                    device_leds[led] = (color[0], color[1])
                if len(color) == 3:
                    device_leds[led] = (color[0], color[1], color[2])
            self.cue.set_led_colors_buffer_by_device_index(di, device_leds)
        self.cue.set_led_colors_flush_buffer()


