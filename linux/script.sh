#!/bin/bash
title=$1  # Window title or a portion of it, Mozilla Firefox can be firefox
key=$2    # Key to send, 1 = left mouse, 2 = middle, 3 = right
          # If you want a keystroke thant change "click" to "key" in the last command
          # and pass the key you want to (it can be a combination).

win=$(xdotool search --onlyvisible -name $title | head -1)

xdotool click --clearmodifiers --repeat 100000000000000000 --delay 1000 --window $win $key
