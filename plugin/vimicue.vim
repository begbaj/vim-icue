" ============================================================================
" File:        vimicue.vim
" Maintainer:  Began Bajrami <beganbajrami at gmail dot com>
" License:     This program is free software. It comes without any warranty,
"              to the extent permitted by applicable law. You can redistribute
"              it and/or modify it under the terms of the Do What The Fuck You
"              Want To Public License, Version 2, as published by Sam Hocevar.
"              See http://sam.zoy.org/wtfpl/COPYING for more details.
"
" ============================================================================
"
" SECTION: Script init stuff {{{1
"============================================================
if exists('loaded_vim_icue')
    finish
endif
let loaded_vim_icue = 1

"SECTION: Initialize variable calls {{{2
let g:vimicue_insert_layout = {"default": "0,0,0"}
let g:vimicue_normal_layout = {"default": "0,0,0"}
let g:vimicue_visual_layout = {"default": "0,0,0"}
let g:vimicue_command_layout = {"default": "0,0,0"}

"SECTION: Default keybindings for mode detection {{{2
nnoremap r :call VimICUEDetectMode('replace')<CR>r
nnoremap i :call VimICUEDetectMode('insert')<CR>i
nnoremap v :call VimICUEDetectMode('visual')<CR>v
nnoremap : :call VimICUEDetectMode('command')<CR>:
nnoremap / :call VimICUEDetectMode('search')<CR>/
nnoremap ? :call VimICUEDetectMode('reverse_search')<CR>?
noremap <esc> :call VimICUEDetectMode('normal')<CR><esc>
noremap <bs> :call VimICUEDetectMode('unknown')<CR><bs>

"SECTION: Key ids list {{{2
let g:vimicue_keys = ['K_ESC','K_F1','K_F2','K_F3','K_F4','K_F5','K_F6','K_F7','K_F8','K_F9','K_F10','K_F11','K_F12','K_1','K_2','K_3','K_4','K_5','K_6','K_7','K_8','K_9','K_0','K_Q','K_W','K_E','K_R','K_T','K_Y','K_U','K_I','K_O','K_P','K_A','K_S','K_D','K_F','K_G','K_H','K_J','K_','K_','K_L','K_Z','K_X','K_C','K_V','K_B','K_N','K_M','K_SEMIC','K_PERIOD','K_COMMA','K_SLASH','K_BSLASH','K_SCLOSED','K_SOPENED','K_MINUS','K_EQ','K_TILDE','K_TAB','K_BLOC','K_M','K_RSHIFT','K_LSHIFT','K_RCTR','K_LCTRL','K_SUPER','K_ALT','K_SPACE','K_ENTER','K_UP','K_DOWN','K_LEFT','K_RIGHT']

