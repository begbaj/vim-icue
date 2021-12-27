import pynvim
from cuesdk import CueSdk

@pynvim.plugin
class VimICUE(object):
    def __init__(self, vim: pynvim.Nvim):
        self.vim = vim
        self.cue = CueSdk()
        self.mode = "normal"
        self.cue_connected = self.cue.connect()
        self.connected = False
        self.connect()
        if not self.cue_connected:
            err = self.cue.get_last_error()
            self.vim.out_write(f"Handshake failed: {err}\n")
            return
        self.leds = self.leds_count()
        self.auto_layout()

    @pynvim.function("VimICUEConnect")
    def connect(self, handler=None):
        self.vim.out_write("FOCUS GAINED \n")
        self.cue.request_control()
        self.connected = True

    @pynvim.function("VimICUEDisconnect")
    def disconnect(self, handler=None):
        self.vim.out_write("FOCUS LOST \n")
        self.cue.release_control()
        self.connected = False

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
        # self.vim.out_write(f"{args}\n")
        mode = args[0]
        # match mode:
        #     case 'n':
        #         self.mode = 'normal'
        #     case 'i':
        #         self.mode = 'insert'
        #     case 'c':
        #         self.mode = 'command'
        if mode == 'n':
            self.mode = 'normal'
        elif mode == 'i':
            self.mode = 'insert'
        elif mode == 'c':
            self.mode = 'command'
        self.auto_layout()

    @pynvim.command("VimICUEAutoLayout")
    def auto_layout(self):
        mode = self.mode
        # self.vim.out_write(f"vimicue_{mode}_layout\n")
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


