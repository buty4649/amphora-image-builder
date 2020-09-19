#!/opt/amphora-agent-venv/bin/python3

import os
import time
import signal
from subprocess import check_output
from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client

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
  return client.Client(session=sess, retries=5)

def is_keepalived_master():
    retry_cnt = 0
    data_path = "/tmp/keepalived.data"
    if os.path.isfile(data_path):
      os.remove(data_path)
    pid = sorted(list(map(int,check_output(["pidof", "keepalived"]).split())))[0]
    os.kill(int(pid), signal.SIGUSR1)
    while not os.path.exists(data_path):
      time.sleep(0.1)
      retry_cnt += 1
      if retry_cnt > 10:
          return False
    with open(data_path, "r") as f:
      return "State = MASTER" in f.read()

def is_state_change(is_master):
    data_path = "/tmp/keepalived.last_state"
    current = "MASTER" if is_master else "BACKUP"
    ret = False
    if os.path.exists(data_path):
      with open(data_path, "r") as f:
        if current not in f.read():
          ret = True

    with open(data_path, mode='w') as f:
      f.write(current)
    return ret

def retrivePortID(neutron):
  interface_file = "/var/lib/octavia/plugged_interfaces"
  if not os.path.exists(interface_file):
    return None

  with open(interface_file, "r") as f:
    mac_address = f.readline().split(" ")[0]

  res = neutron.list_ports(mac_address=mac_address)
  return res["ports"][0]["id"]

def update_port():
  is_master = is_keepalived_master()
  if not is_state_change(is_master):
    return "same state"

  if not is_master:
    return "I'm not a MASTER"
  neutron = getNeutronClient()
  port_id = retrivePortID(neutron)
  if port_id is None:
    return "failed: port_id was not found"

  if neutron.update_port(port_id, {"port":{"admin_state_up": True}}):
      return "update success"
  else:
      return "update failed: api call failed"

if __name__ == '__main__':
  update_port()
