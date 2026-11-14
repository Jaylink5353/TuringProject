# Linux Support:

It's weird. On Windows, things work nicely, but for Linux you need to install `WebKit2GTK`

### Required Packages:
Debian / Ubuntu:
```sudo apt install libwebkit2gtk-4.1-dev```

Arch:
```sudo pacman -S webkit2gtk-4.1```

Fedora:
```sudo dnf install webkit2gtk4.1-devel```

### Limitations:

Due to limitations in pynput, the window needs to run in x11. If you already run x11, good, if wayland, you have to run it in xwayland. This means that the keyboard inputs will only be caputed when the window is active. The code handles this by itself.

More info here: https://pynput.readthedocs.io/en/latest/limitations.html