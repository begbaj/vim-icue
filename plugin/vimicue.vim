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

" SECTION: Script init stuff {{{1
"============================================================
if exists('loaded_vim_icue')
    finish
endif
let loaded_vim_icue = 1

let g:vimicue_debug_mode = 1

function! Vimicue_print(message)
    if exists("vimicue_debug_mode")
        echom a:message
    endif
endfunction

" plugged_home is needed due to unreachable directory if otherwise
if has('win32') || has('win64')
    let s:vimicue_home = expand('~/AppData/Local/nvim/plugged/vim-icue/')
    " call Vimicue_print(" vimicue home directory: " . s:vimicue_home)
else
    let s:vimicue_home = expand('~/.config/nvim/plugged/vim-icue/')
    " call Vimicue_print(" vimicue home directory: " . s:vimicue_home)
endif

"SECTION: Mode mapping
" Changes this to add other modes, if you know there are others...

if !exists('vimicue_default_map')
    let g:vimicue_default_map = {}
    " call Vimicue_print("loading default mapping!")
else
    " call Vimicue_print("merging user defined mapping!")
    call extend( g:vimicue_default_map, {
            \ 'default' : 'default',
            \ 'c'  : 'command',
            \ 'i'  : 'insert',
            \ 'ic' : 'insert_compl',
            \ 'ix' : 'insert_compl',
            \ 'multi' : 'multi',
            \ 'n'  : 'normal',
            \ 'ni' : 'insert',
            \ 'no' : 'op_pending',
            \ 'R'  : 'replace',
            \ 'Rv' : 'v_replace',
            \ 's'  : 'select',
            \ 'S'  : 's_line',
            \ 't'  : 'terminal',
            \ 'v'  : 'visual',
            \ 'V'  : 'v_line',
            \ }, 'keep')
endif

"SECTION: Key ids list {{{2
let g:vimicue_names = json_decode(readfile(expand(s:vimicue_home . 'plugin/vimicue_names.json')))
let g:vimicue_keys = json_decode(join(readfile(expand(s:vimicue_home .  'plugin/vimicue_keys.json'))))

"SECTION: THEME Loading {{{1
if !exists('vimicue_theme_name')
    let g:vimicue_theme_name = "begbaj-default-red"
    " call Vimicue_print("default theme will be loaded")
endif

" Introducing modular loading
"=============================== 
" Brief description of the new Theme formatting
"=============================== 
" Now it is possible to load any mode. So the ideal way
" to load themes is to just call a theme like the wanted mode
" and then vimicue will do the rest.
"
" As a major change, now will be need only one file, which will be called
" as the theme.
"
" vimi-icue process for doing this would be:
"   search for a file nemed {theme}.json, if exists, load it.
"   Othterwise, launch an error.

function! s:load_theme()
    " call Vimicue_print("loading theme...")

    let l:theme_directory = expand(s:vimicue_home . "/themes/")

    " call Vimicue_print("vimicue theme directory: " . l:theme_directory)

    if filereadable(l:theme_directory . g:vimicue_theme_name. ".json")
        " call Vimicue_print("loading theme: " . vimicue_theme_name)
        let g:vimicue_theme = json_decode(join(readfile(l:theme_directory . g:vimicue_theme_name . ".json" )))
       
    else
       " TODO: define a standard way to output messages to user
       echom "VimICUE Error: no theme named " . vimicue_theme_name
       let g:vimicue_theme = json_decode(join(readfile(l:theme_directory . "begbaj-default-red.json" )))
    endif
endfunction

function! s:update_current_mode(force)
    " call Vimicue_print("updating current mode")
    let l:cmode=mode()
    " call Vimicue_print("current mode is " . cmode)
    if g:vimicue_default_map->has_key(cmode)
        let l:nmode=tolower(g:vimicue_default_map[cmode])
    else
        let l:nmode="default"
    endif
    " call Vimicue_print("translated as: " . nmode)

    if a:force == 1
        " call Vimicue_print("calling refresh() in forced mode")
        call VimICUERefreshForce(nmode)
    else
        " call Vimicue_print("calling refresh()")
        call VimICUERefresh(nmode)
    return
endfunction

function! s:on_focus_gain()
    " call Vimicue_print("focus gained")
    call s:load_theme()
    call s:update_current_mode(1)
    " call Vimicue_print("running play()")
    VimICUEPlay
endfunction

function! s:focus_lost()
    " call Vimicue_print("focus lost")
    VimICUEStop
endfunction

function! s:icue_connect()
    " call Vimicue_print("connecting icue")
    VimICUEConnect
endfunction

function! s:icue_disconnect()
    " call Vimicue_print("disconnecting")
    VimICUEDisconnect
    VimICUEStop
endfunction

"SECTION: Autocommands {{{2
augroup VimICUEEvenets
    autocmd!
    autocmd ModeChanged *:* call s:update_current_mode(0)
    " TODO: stop script function
    autocmd FocusLost * call s:focus_lost()
    autocmd FocusGained * call s:on_focus_gain()
    " TODO: disconnect script function
    autocmd vimleave * call s:icue_disconnect()
augroup END

call s:icue_connect()
