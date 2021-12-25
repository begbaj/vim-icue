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
nnoremap r :call VimICUEDetectMode('replace<CR>')
nnoremap i :call VimICUEDetectMode('insert<CR>')
nnoremap v :call VimICUEDetectMode('visual<CR>')
nnoremap : :call VimICUEDetectMode('command<CR>')
nnoremap / :call VimICUEDetectMode('search<CR>')
nnoremap ? :call VimICUEDetectMode('reverse_search<CR>')
noremap <esc> :call VimICUEDetectMode('normal<CR>')
noremap <bs> :call VimICUEDetectMode('unknown<CR>')

"SECTION: Key ids list {{{2
let g:vimicue_keys = ['klesc', 'klf1', 'klf2', 'klf3', 'klf4', 'klf5', 'klf6', 'klf7', 'klf8', 'klf9', 'klf10',
                        'klf11', 'klf12', 'kl1', 'kl2', 'kl3', 'kl4', 'kl5', 'kl6', 'kl7', 'kl8', 'kl9', 'kl0', 'klq',
                        'klw', 'kle', 'klr', 'klt', 'kly', 'klu', 'kli', 'klo', 'klp', 'kla', 'kls', 'kld', 'klf',
                        'klg', 'klh', 'klj', 'kl', 'kl', 'kll', 'klz', 'klx', 'klc', 'klv', 'klb', 'kln', 'klm',
                        'klsemic', 'klperiod', 'klcomma', 'klslash', 'klbslash', 'klsclosed', 'klsopened', 'klminus',
                        'kleq', 'kltilde', 'kltab', 'klbloc', 'klm', 'klrshift', 'kllshift', 'klrctr', 'kllctrl',
                        'klsuper', 'klalt', 'klspace', 'klenter', 'klup', 'kldown', 'klleft', 'klright']

