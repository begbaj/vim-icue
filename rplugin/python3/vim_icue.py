import neovim
import cuesdk
import logging

@neovim.plugin
class VimICUE(object):
    def __init__(self, vim:neovim.Nvim):
        logging.basicConfig(level=logging.DEBUG)
        self.vim = vim
        self.insertModeOn = self.vim.subscribe("InsertEnter")
        self.insertModeOff = self.vim.subscribe("InsertLeave")

    @neovim.function('VimICUEGetMode', sync=False)
    def getMode(self, args):
       mode = self.vim.call('mode')
       self.vim.current.line = mode


