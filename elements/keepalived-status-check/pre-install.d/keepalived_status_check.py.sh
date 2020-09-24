#!/bin/bash

sudo /bin/rm -f /tmp/keepalived.last_state
sudo /usr/local/bin/keepalived_status_check.py
