# Vim-iCUE
<p align="center">
  <img src="readme/img/vimicue_logo.png" alt="drawing" width="200"/>
</p>

Vim-iCUE is the first vim plugin that links together your [Corsair](https://www.corsair.com/it/it/) RGB device with [Neovim](https://neovim.io/)! Make your Neovim experience even better with keyboard RGB themes that changes automatically as you pass from **Insert** to **Normal** mode. Vim-icue is tested only on Windows 10, but it should work with any Windows or MacOS version that supports iCUE.

## WARNING!
As of now, I'm testing Vim-iCUE on my own keyboard which is a [Corsair Strafe](https://www.corsair.com/eu/en/Categories/Products/Gaming-Keyboards/Standard-Gaming-Keyboards/STRAFE-Mechanical-Gaming-Keyboard-%E2%80%94-CHERRY%C2%AE-MX-Silent/p/CH-9104023-NA) and supports only red color.
Also, Vim-ICUE is tested only on Windows 10.

Theoretically, it should work on RGB Corsair keyboards in both Windows and MacOS, but I'm not sure about that. Let me know if it works.

Unfortunatly, it will not work on Linux, as ICUE is still not supported yet.

## Installation
### Requirements
1. iCUE
2. Nvim with python3 support (if you use nvim, you should already support python3)
3. Python >= 3.10 
4. A Corsair keyboard
5. Vim-Plug or any other plugin manager

Make sure you have all python3 dependencies installed on your machine by running `pip install -r requirements.txt`.

### Plugging in
Plug vim-icue into your nvim just by putting (if you're using vim-plug as your plugin manager) `Plug 'begbaj/vim-icue'` in the  *plugin section* in your **init.vim** as follows:

```init.vim
call plug#begin()
" ... other plugins, if any
Plug 'begbaj/vim-icue'
" .. other plugins, if any
call plug#end()
```

If your keyboard doesn't support rgb, you also need to put this line in your **init.vim**
```init.vim
let g:vimicue_is_rgb = 0
```
Now you're ready to go! Vim-icue will automatically start after installation is complete.

## Themes
By default, vim-icue uses the *begbaj-default-red* theme. To change theme just edit your **init.vim** as follows:
```init.vim
let g:vimicue_theme = '<theme-name>'
```
To use a theme you either need to create one or download one.

If you want to change just the behaviour of one layout, you can override themes in your **init.vim**:

```init.vim
" --- if your keyboard does support rgb:
let g:vimicue_<mode>_layout = {'<keynam>': [<R>, <G>, <B>], ... , 'default': [<R>, <G>, <B>]}
" --- if your keyboard doesn't support rgb:
let g:vimicue_<mode>_layout = {'<keynam>':[0, <Brightness>], ... , 'default': [0, <Brightness>]}
```
### Create a new theme
Keep in mind that, as of now, there are only three modes supported (*Normal, Insert and Command* modes). I'm planning to increase this number to 6,
that is *Normal, Insert, Command, Visual, Search, Reversed Search* and maybe others in the future.
To create a theme, you first need to create a new directory under *templates/* folder:

* Windows users: open `~/AppData/Local/nvim/plugged/vim-icue/templates` and create a new folder named as your theme;

* MacOS users: open `~/.vim/plugged/vim-icue/templates` and create a new folder named as your theme;

Under your theme folder, create the following files:

* Non-RGB templates: *command.json; insert.json; normal.json; visual.json;*
* RGB templates: *command-rgb.json; insert-rgb.json; normal-rgb.json; visual-rgb.json;*

You need to create *visual.json* or *visual-rgb.json* even if this file will be empty until visual mode is supported.

Now you have to define the behavior of the lights of each single key you want to change. All the other keys will take on the color defined by the 'default' Keyname.
Each `.json` file should be in this format:
If your keyboard supports RGB:
```
{"first_keyname" : [R, G, B], "second_keyname" : [R, G, B], ... , "default" : [R, G, B]}
```
If your keyboard supports only one color:
```
{"first_keyname": [0,Brightness], "second_keyname": [0,Brightness], ... , "default": [0,Brightness]}
```

* Keyname: a String value, surrounded by `'`, which identifies each key. 
* Value: a list of 2 or 3 integer values from 0 to 255.

Here is a [List](Keys.md) of all Keyname values  (For common keys, just use the prefix `K_<Key>`)

Keyname examples:
```
Keyname for H: K_H
Keyname for J: K_J
Keyname for K: K_K
Keyname for L: K_L
and so on...
```
### Usage after configuration is done
Once you configured  the layouts as you like, just reload your **init.vim** and use nvim as usual. You will see effects
on your keyboard immediately as you type.
