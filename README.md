# vim-icue
I CUE integration for nvim
## WARNING
As of now, I'm testing vim-icue on my own keyboard which is a [Corsair Strafe](https://www.corsair.com/eu/en/Categories/Products/Gaming-Keyboards/Standard-Gaming-Keyboards/STRAFE-Mechanical-Gaming-Keyboard-%E2%80%94-CHERRY%C2%AE-MX-Silent/p/CH-9104023-NA) and supports only red color.
For this reason, I only need one value (from 0, which means off, to 255, full brightness). 

Theoretically, it should work even on RGB Corsair keyboards, but I'm not sure about that.

In this case, `g:vimicue_<mode>_layout = {'default': [0,<value>]}` global variables should be in this form:
`g:vimicue_<mode>_layout = {'default': [<R>,<G>,<B>]'}`, but it's just a guess.

Let me know if this works fine.

## Installation
### Requirements
1. Nvim with python3 support (if you use nvim, you should already support python3)
2. Python >= 3.10 
3. A Corsair keyboard
4. Vim-Plug or any other plugin manager

To install vim-icue, make sure you have all python3 dependencies installed on your machine:

`pip install -r requirements.txt`

### Plugging in
Now you can plug vim-icue into your nvim just by inserting (if you're using vim-plug as your plugin manager) `Plug 'begbaj/vim-icue'` in the  *plugin section* in your **init.vim** as follows:

```init.vim
call plug#begin()
" ... other plugins, if any
Plug 'begbaj/vim-icue'
" .. other plugins, if any
call plug#end()
```

If your keyboard doesn't support rgb, you also need to put this line in your **init.vim**
```init.vim
...
let g:vimicue_is_rgb = 0
...
```
Now you're ready to go! Vim-icue will automatically start after installation is complete.

## Themes
By default, vim-icue uses the *begbaj-default-red* theme. To change theme just edit your **init.vim** as follows:
``` init.vim
...
let g:vimicue_theme = '<theme-name>'
...
```
To use a theme you either need to create one or download one.
### Create a new theme
Keep in mind that, as of now, there are only three modes supported (*Normal, Insert and Command* modes). I'm planning to increase this number to 6,
that is *Normal, Insert, Command, Visual, Search, Reversed Search* and maybe others in the future.
To create a theme, you first need to create a new directory under *templates/* folder:

* Windows users: open `~/AppData/Local/nvim/plugged/vim-icue/templates` and create a new folder named as your theme;

* Linux users: open `~/.vim/plugged/vim-icue/templates` and create a new folder named as your theme;

Under your theme folder, create the following files: `command.json; insert.json; normal.json; visual.json;`
You need to create `visual.json` even if this file will be empty until visual mode support.

Now you have to define the behavior of the lights of each single key you want to change. All the other keys will take on the color defined by the 'default' Keyname.
Each `.json` file should be in this format:
``` if your keyboard supports only one color
{'<keyname>': [0, <brightness>], ... , 'default': [0, <birghtness>]}
```
``` if your keyboard supports RGB
{'<keyname>': [<R>, <G>, <B>], ... , 'default': [<R>, <G>, <B>]}
```
* Keyname: a String value, surrounded by `'`, which identifies each key. 
* Value: a list of integer values.
* 
Values between `[]` are all integers from 0 to 255.

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
