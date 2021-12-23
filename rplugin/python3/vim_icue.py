import neovim
import cuesdk

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.vim.command('echo "hello from DoItPython"')