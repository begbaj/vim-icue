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

" plugged_home is needed due to unreachable directory if otherwise
if has('win32') || has('win64')
    let s:vimicue_home = expand('~/AppData/Local/nvim/plugged/vim-icue/')
else
    let s:vimicue_home = expand('~/.config/nvim/plugged/vim-icue/')
endif
if !exists('vimicue_default_map')
    let g:vimicue_default_map = {}
endif
"SECTION: Mode mapping
" Changes this to add other modes, if you know there are others...
call extend(g:vimicue_default_map, {
        \ '__' : '------',
        \ 'c'  : 'COMMAND',
        \ 'i'  : 'INSERT',
        \ 'ic' : 'INSERT COMPL',
        \ 'ix' : 'INSERT COMPL',
        \ 'multi' : 'MULTI',
        \ 'n'  : 'NORMAL',
        \ 'ni' : '(INSERT)',
        \ 'no' : 'OP PENDING',
        \ 'R'  : 'REPLACE',
        \ 'Rv' : 'V REPLACE',
        \ 's'  : 'SELECT',
        \ 'S'  : 'S-LINE',
        \ '' : 'S-BLOCK',
        \ 't'  : 'TERMINAL',
        \ 'v'  : 'VISUAL',
        \ 'V'  : 'V-LINE',
        \ '' : 'V-BLOCK',
        \ }, 'keep')


"SECTION: Key ids list {{{2
let g:vimicue_names = json_decode(readfile(expand(s:vimicue_home . 'plugin/vimicue_names.json')))
let g:vimicue_keys = json_decode(join(readfile(expand(s:vimicue_home .  'plugin/vimicue_keys.json'))))

"SECTION: THEME Loading {{{1
if !exists('vimicue_theme_name')
    let g:vimicue_theme_name = "begbaj-default-red"
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
    let l:theme_directory = expand(s:vimicue_home . "/themes/")
    if filereadable(l:theme_directory . g:vimicue_theme_name. ".json")
       let g:vimicue_theme = json_decode(join(readfile(l:theme_directory . g:vimicue_theme_name . ".json" )))
    else
       " TODO: define a standard way to output messages to user
       echom "VimICUE Error: no theme named " .g: vimicue_theme_name
       let g:vimicue_theme = json_decode(join(readfile(l:theme_directory . "begbaj-default-red.json" )))
    endif
endfunction

function! s:update_current_mode()
        let l:cmode=mode()
        if g:vimicue_default_map->has_key(cmode)
            let l:nmode=tolower(g:vimicue_default_map[cmode])
        else
            let l:nmode=tolower(g:vimicue_default_map['default'])
        endif
        call VimICUERefresh(nmode)
        return
endfunction

"TODO: REMOVE THIS FUNCTION, just get the variable into python without calling any function
function! s:get_layout(cmode)
        if a:cmode == "normal"
            return g:vimicue_normal_layout
        elseif a:cmode == "command"
            return g:vimicue_command_layout
        elseif a:cmode == "insert"
            return g:vimicue_insert_layout
        elseif a:cmode == "visual"
            return g:vimicue_visual_layout
        endif
endfunction

function! VimICUEGetKeyColorById(cmode, cid)
    let l:keydict = VimICUEGetLayout(a:cmode)
    if l:keydict->has_key(g:vimicue_keys[a:cid])
        return l:keydict[g:vimicue_keys[a:cid]]
    else
        return l:keydict['default']
    endif
endfunction

function! s:focus_gained()
    call s:load_theme()
    VimICUEPlay
    call s:update_current_mode()
endfunction

function! s:focus_lost()
    VimICUEStop
endfunction

function! s:icue_connect()
    VimICUEConnect
    call s:focus_gained()
endfunction

function! s:icue_disconnect()
    VimICUEDisconnect
    call s:focus_lost()
endfunction




"SECTION: Autocommands {{{2
augroup VimICUEEvenets
    autocmd!
    autocmd ModeChanged *:* call s:update_current_mode()
    " TODO: stop script function
    autocmd FocusLost * call s:focus_lost()
    autocmd FocusGained * call s:focus_gained()
    "autocmd VimEnter, FocusGained * call s:icue_connect()
    " TODO: disconnect script function
    autocmd vimleave * call s:icue_disconnect()
augroup END
