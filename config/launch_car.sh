#!/bin/sh

sleep 60 # wait some time to give time to connect to internet and start the Desktop manager

tmux new -d -s car 'source $HOME/local_config ; DISPLAY=:0 python3 $HOME/ex.py'
