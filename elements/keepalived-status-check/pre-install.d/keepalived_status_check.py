#!/opt/amphora-agent-venv/bin/python3

import os
import sys
import select
import json
import urllib2
from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client


# skeleton config parameters
pollPeriod = 0.2 # the number of seconds between polling for new messages
maxAtOnce = 1024  # max nbr of messages that are processed within one batch

# App logic global variables
def getNeutronClient():
  username='%%{OS_USERNAME}%%'
  password='%%{OS_PASSWORD}%%'
  project_name='admin'
  project_domain_id='default'
  user_domain_id='default'
  auth_url='%%{OS_AUTH_URL}%%'
  auth = identity.Password(auth_url=auth_url,
                           username=username,
                           password=password,
                           project_name=project_name,
                           project_domain_id=project_domain_id,
                           user_domain_id=user_domain_id)
  sess = session.Session(auth=auth)
  return client.Client(session=sess)

def retrivePortID():
  interface_file = "/var/lib/octavia/plugged_interfaces"
  if not os.path.exists(interface_file):
    return None

  with open(interface_file, "r") as f:
    mac_address = f.readline().split(" ")[0]

  response = urllib2.urlopen("http://169.254.169.254/openstack/latest/network_data.json")
  network_data = json.loads(response.read())

  info = filter((lambda n: n["ethernet_mac_address"] == mac_address), network_data["links"])
  return info[0]["vif_id"]

def onInit():
  pass

def onReceive(msgs):
  port_id = retrivePortID()
  if port_id is None:
    return False

  neutron = getNeutronClient()
  neutron.update_port(port_id, {"port":{"admin_state_up": True}})

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
