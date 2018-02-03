from user import getusers, getuser, getgroups, addusertogroup, removeuserfromgroup
import re


print('addusertogroup')
logid = addusertogroup('giuseppe', 'dip')
print(logid)

print('removeuserfromgroup')
logid = removeuserfromgroup('giuseppe', 'dip')
print(logid)
