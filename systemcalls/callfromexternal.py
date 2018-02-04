from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, updateusershell
from apps import listinstalled, aptsearch, aptshow




p1 = aptshow('sudo')
print(type(p1))
p1 = p1.split('\n\n')

for i in p1:
    print(i)

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
