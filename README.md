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

`pip install -r requirements`

### Plugging in
Now you can plug vim-icue into your nvim just by inserting (if you're using vim-plug as your plugin manager) `Plug 'begbaj/vim-icue'` in the  *plugin section* in your **init.vim** as follows:

```
call plug#begin()
" ... other plugins, if any
Plug 'begbaj/vim-icue'
" .. other plugins, if any
call plug#end()
```

And now you're ready to go!

## Usage
### Configuration
By default, all layouts are set to default value of [0,255] which means that all keys in any mode you're on are fully
brightened. You can change the keyboard lightning behaviour by configuring vim-icue in your **init.vim**.
### Change layout by mode
As of now, there are only three modes supported (*Normal, Insert and Command* modes). I'm planning to increase this number to 6,
that is *Normal, Insert, Command, Visual, Search, Reversed Search* and maybe others in the future.

To customize the layouts you need to follow the following format:
```
" ONE COLOR BRIGTHNESS TEMPLATE
" plugin section
" ... other init.vim stuff
let g:vimicue_<mode>_layout = {'<keyname>': [0, <brightness>], ... , 'default': [0, <birghtness>]}
" ... other init.vim stuff
" NOTE: This is if your keyboard only supports one color, as mine does
```

```
" RGB TEMPLATE
" NOTE: THIS IS NOT TESTED YET, I don't know if this works
" plugin section
" ... other init.vim stuff
let g:vimicue_<mode>_layout = {'<keyname>': [<R>, <G>, <B>], ... , 'default': [<R>, <G>, <B>]}
" ... other init.vim stuff
" NOTE: This is if your keyboard only supports one color, as mine does
```
Values between `[]` are all integers from 0 to 255.

* Mode: the mode name. Supported modes are `normal, command, insert`
* Keyname: a String value, surrounded by `'`, which identifies each key. 
* Value: a list of integer values.

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