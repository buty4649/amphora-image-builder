#!/opt/amphora-agent-venv/bin/python3

import os
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

def retrivePortID(neutron):
  interface_file = "/var/lib/octavia/plugged_interfaces"
  if not os.path.exists(interface_file):
    return None

  with open(interface_file, "r") as f:
    mac_address = f.readline().split(" ")[0]

  res = neutron.list_ports(mac_address=mac_address)
  return res["ports"][0]["id"]

def update_port():
  neutron = getNeutronClient()
  port_id = retrivePortID(neutron)
  if port_id is None:
    return False

  neutron.update_port(port_id, {"port":{"admin_state_up": True}})

if __name__ == '__main__':
  update_port()
