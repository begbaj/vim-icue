# Vim-iCUE
<p align="center">
  <img src="readme/img/vimicue_logo.png" alt="drawing" width="200"/>
</p>

Vim-iCUE is the first Neovim plugin that links together your [Corsair](https://www.corsair.com/) RGB device with
[Neovim](https://neovim.io/)! Make your Neovim experience even better with keyboard RGB themes that changes 
automatically as you pass from **Insert** to **Normal** to **Command** mode. Vim-iCUE is tested only on Windows 10, 
but it should work
with any Windows or MacOS version that supports iCUE.

## WARNING!
At the moment, I'm testing Vim-iCUE on my own keyboard which is a [Corsair Strafe](https://www.corsair.com/eu/en/Categories/Products/Gaming-Keyboards/Standard-Gaming-Keyboards/STRAFE-Mechanical-Gaming-Keyboard-%E2%80%94-CHERRY%C2%AE-MX-Silent/p/CH-9104023-NA) and supports only red color.
Also, Vim-iCUE is tested only on Windows 10.

In theory, it should work even on RGB Corsair keyboards in both Windows and MacOS, but I'm not sure about that. Let me know if it works.

Unfortunatly, it will not work on Linux, as iCUE is still not supported yet.

## Installation
### Requirements
  * [iCUE](https://www.corsair.com/downloads)
  * [Neovim](https://neovim.io/)
  * Python >= 3.10 (maybe 3.7 is enough) 
  * A Corsair keyboard
  * Any Vim plugin manager, I recommend [Vim-plug](https://github.com/junegunn/vim-plug)

### Plugging-in
Plug Vim-iCUE into your Neovim in the  *plugin section* in your **init.vim**.

For example, using Vim-plug it will look something like this:
```init.vim
call plug#begin()
" ... other plugins, if any
Plug 'begbaj/vim-icue'
" .. other plugins, if any
call plug#end()
```
### Non-RGB Keyboard support

If your keyboard doesn't support RGB, you also need to set this variable in **init.vim**
```init.vim
let g:vimicue_is_rgb = 0
```
Now you're ready to go! Vim-iCUE will automatically start after installation is complete.

## Themes
By default, Vim-iCUE uses the *begbaj-default-red* theme. To change theme just edit your **init.vim** as follows:
```init.vim
let g:vimicue_theme = '<theme-name>'
```
To use a theme you either need to create one or download one.

If you want to change the behaviour of one layout, you can override themes in your **init.vim**:

```init.vim
" --- if RGB support is enabled:
let g:vimicue_<mode>_layout = {'<keyname>': [<R>, <G>, <B>], ... , 'default': [<R>, <G>, <B>]}
" --- if RGB support is disabled:
let g:vimicue_<mode>_layout = {'<keyname>':[0, <Brightness>], ... , 'default': [0, <Brightness>]}
```

This will still load the previously selected theme, but will also override one (or more) layout(s).

### Create a new theme
Keep in mind that, at the moment, there are only three modes supported (*Normal, Insert and Command*).
I'm planning to increase this number to 5 (*Normal, Insert, Command, Visual, Search*) or more in the future.
To create a theme, you first need to create a new directory under *templates/* folder:

* Windows users: open `~/AppData/Local/nvim/plugged/vim-icue/templates` and create a new folder named as your theme;

* MacOS users: open `~/.vim/plugged/vim-icue/templates` and create a new folder named as your theme;

Under your theme folder, create the following files:

* Non-RGB templates: *command.json; insert.json; normal.json;*
* RGB templates: *command-rgb.json; insert-rgb.json; normal-rgb.json;*
* 
### Template

Now you have to define the behavior of the lights of each single key you want to change. All the other keys will take
on the color defined by the 'default' Keyname.

Each `.json` should be in this format:

In RGB templates:
```
{"first_keyname" : [R, G, B], "second_keyname" : [R, G, B], ... , "default" : [R, G, B]}
```

In Non-RGB templates:
```
{"first_keyname": [0,Brightness], "second_keyname": [0,Brightness], ... , "default": [0,Brightness]}
```
Where:

* Keyname: a String value, surrounded by `'`, which identifies each key. 
* \[R,G,B\] or \[0, Brightness\]: a list of 3 or 2 integer values from 0 to 255.
* 
Keyname examples:
```
Keyname for H: K_H
Keyname for J: K_J
Keyname for K: K_K
Keyname for L: K_L
and so on...
```

Here is a [List](Keys.md) of all Keyname values.

### Usage after configuration is done
Once you configured  the layouts as you like, just reload your **init.vim** and use nvim as usual. You will see effects
on your keyboard immediately as you type.

# FocusLost/FocusGained events
Windows doesn't support these Vim events, which means that I'm not able to temporally disable Vim-iCUE exclusive device
control while Neovim is open.

I hope that this works on MacOS, but I can't test it.

# TODO:
- [ ] Keyname grouping (like: *numbers*, *letters*, ...)
- [ ] Keyboard effects
- [ ] Mouse support

