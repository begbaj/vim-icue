import neovim
import cuesdk
import logging

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim:neovim.Nvim):
        logging.basicConfig(level=logging.DEBUG)
        self.vim = vim

    @neovim.function('DoItPython', sync=False)
    def get_mode(self, args):
       mode = self.vim.command('mode')
       self.vim.current.line = mode


