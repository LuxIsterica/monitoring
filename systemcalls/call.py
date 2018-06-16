from pprint import pprint
from network import ifacestat

facestat = ifacestat()['data']

for key,value in facestat.items():
    if 'LOOPBACK' in value[-1]:
        print("'" + key + "' is a loopback interface")
    elif ':' in key:
        print("'" + key + "' is an alias interface")
    else:
        print("'" + key + "' is a normal interface")
