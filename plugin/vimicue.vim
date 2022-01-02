if exists('loaded_vim_icue')
    finish
endif
let loaded_vim_icue=1

" SECTION: Configuration
" ===============================================================================

let g:vimicue_debug_enabled=0     " enable debugging outputs
if !exists('vimicue_home')
    if has('win32') || has('win64')
        let g:vimicue_home=expand('~/AppData/Local/nvim/plugged/vim-icue/')
    else
        let g:vimicue_home=expand('~/.config/nvim/plugged/vim-icue/')
    endif
endif


function! VimICUEPrintDebug(message)
    if g:vimicue_debug_enabled == 1
        if type(a:message) == 1
            echom "Vim-iCUE DEBUG: " . a:message
        else
            echom a:message
        endif
    endif
endfunction


" SECTION: Vim-iCUE global variables 
" ===============================================================================
let g:vimicue_theme={}



" SECTION: Vim-iCUE mode mapping
" ===============================================================================

" checks if user has defined a custom mode mapping, if not define an empty one
if !exists('vimicue_default_map')
    let g:vimicue_default_map={}
endif

" merge the default mode mapping to the user defined mapping
call extend( g:vimicue_default_map, {
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

" SECTION: key-names directory loading
" ===============================================================================

let g:vimicue_names=json_decode(join(readfile(expand(g:vimicue_home . 'plugin/vimicue_names.json'))))
let g:vimicue_keys=json_decode(join(readfile(expand(g:vimicue_home . 'plugin/vimicue_keys.json'))))

" SECTION: global functions
" ===============================================================================

function! VimICUEAddToTheme(tmode, keyname, value)
    let g:vimicue_theme[a:tmode][a:keyname] = a:value
endfunction

function! VimICUELoadTheme()
    call VimICUEPrintDebug("Loading theme...")
    try
        " check selected theme. If none, default theme will be applied
        if exists('vimicue_theme_name') && filereadable(g:vimicue_home . 'themes/' . g:vimicue_theme_name . ".json")
            let g:vimicue_theme_name=g:vimicue_theme_name
        else
            let g:vimicue_theme_name="begbaj-default-red"
        endif
        call VimICUEPrintDebug("Selected theme is: " . g:vimicue_theme_name)
        let g:vimicue_theme=json_decode(join(readfile(g:vimicue_home . "themes/" . g:vimicue_theme_name . ".json")))
        call VimICUEPrintDebug("Theme ". g:vimicue_theme_name . " loaded!")
    catch /*/
        call VimICUEPrintDebug("Exception: " . v:excpetion)
    endtry
endfunction

function! VimICUEUpdateCurrentMode(force)
    let l:cmode=mode()    " get current mode
    let l:nmode='default'
    if g:vimicue_default_map->has_key(l:cmode)
        let l:nmode=g:vimicue_default_map[l:cmode]
    endif

    if a:force == 1
        call VimICUERefreshForce(nmode)
    else
        call VimICUERefresh(nmode)
    endif 
endfunction

" SECTION: script functions
" ===============================================================================

function! s:on_focus_gain()
    call VimICUELoadTheme()
    call VimICUEUpdateCurrentMode(1)
    VimICUEPlay
endfunction

function! s:on_focus_lost()
    VimICUEStop
endfunction

function! s:on_enter()
    VimICUEConnect
endfunction

function! s:on_leave()
    VimICUEDisconnect
    VimICUEStop
endfunction

" SECTION: Autocommands
" ===============================================================================

augroup modechanges
    autocmd!
    autocmd ModeChanged *:* call VimICUEUpdateCurrentMode(0)
    autocmd FocusLost * call s:on_focus_lost()
    autocmd FocusGained * call s:on_focus_gain()
    autocmd VimEnter * call s:on_enter()
    autocmd VimLeave * call s:on_leave()
augroup END

call VimICUEPrintDebug(g:vimicue_home)
call VimICUEPrintDebug(g:vimicue_default_map)

