from user import getusers, getuser, getgroups, addusertogroup, removeuserfromgroup
import re


output = getusers('namesonly')

for i in output:
	print(i)
