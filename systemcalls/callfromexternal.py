from user import getusers, getuser, getgroups, addusertogroups, removeuserfromgroups, adduser, removeuser, updateuserpass, updateusershell, test
from apps import listinstalled, aptsearch, aptshow, aptinstall, aptremove
import os


test('tempa', 'dip')

#TODO: non cancellare le righe successive, discutere con Lucia dei Keyword Arguments
exit()
for i in listinstalled( summary=True ):
    print(i)

removeuser('temp', removehome=True)
