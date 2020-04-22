#!/opt/amphora-agent-venv/bin/python3

import sys
import select
import datetime
import status_check


# skeleton config parameters
pollPeriod = 0.2 # the number of seconds between polling for new messages
maxAtOnce = 1024  # max nbr of messages that are processed within one batch

def onInit():
  pass

def onReceive(msgs):
  with open('/var/log/keepalived_status_check.log', 'a') as f:
    result = status_check.update_port()
    f.write("{} recieved: msg: {} result: {}\n".format(datetime.datetime.now(), msgs, result))
  return

def onExit():
  pass


"""
-------------------------------------------------------
This is plumbing that DOES NOT need to be CHANGED
-------------------------------------------------------
Implementor's note: Python seems to very agressively
buffer stdout. The end result was that rsyslog does not
receive the script's messages in a timely manner (sometimes
even never, probably due to races). To prevent this, we
flush stdout after we have done processing. This is especially
important once we get to the point where the plugin does
two-way conversations with rsyslog. Do NOT change this!
See also: https://github.com/rsyslog/rsyslog/issues/22
"""
import pdb;
onInit()
keepRunning = 1
while keepRunning == 1:
    while keepRunning and sys.stdin in select.select([sys.stdin], [], [], pollPeriod)[0]:
        msgs = []
        msgsInBatch = 0
        while keepRunning and sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line:
                msgs.append(line)
            else: # an empty line means stdin has been closed
                keepRunning = 0
            msgsInBatch = msgsInBatch + 1
            if msgsInBatch >= maxAtOnce:
                break;
        if len(msgs) > 0:
            onReceive(msgs)
            sys.stdout.flush() # very important, Python buffers far too much!
onExit()
