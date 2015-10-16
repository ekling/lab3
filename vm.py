import os
import time
from novaclient.client import Client

config = {'username':os.environ['OS_USERNAME'],
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

nc = Client('2',**config)
nc.keypairs.findall(name="emilKey")

ubuntu_image = nc.images.find(name='Ubuntu Server 14.04 LTS (Trusty Tahr)')
flavor = nc.flavors.find(name='m1.medium')
userdata = open('userdata.yml', 'r')

instance = nc.servers.create(name='EmilInstance', image=ubuntu_image, flavor=
                            flavor, key_name='emilKey', userdata=userdata)

userdata.close()

status = instance.status
while status == 'BUILD':
    time.sleep(10)
    instance = nc.servers.get(instance.id)
    status = instance.status

ips = nc.floating_ips.list()
for ip in ips:
    if ((getattr(ip, 'instance_id')) == None):
            floating_ip = getattr(ip, 'ip')
            break

ins = nc.servers.find(name='EmilInstance')
ins.add_floating_ip(floating_ip)
