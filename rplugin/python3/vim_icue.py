import neovim
import cuesdk
import logging

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim):
        logging.basicConfig(level=logging.DEBUG)
        self.vim = vim

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.vim.command('echo "hello from DoItPython"')