from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, updateusershell
from apps import listinstalled, aptsearch



for i in listinstalled(summary=False):
    print(i)

exit()



#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
