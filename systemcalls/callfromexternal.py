from user import getusers, getuser, getgroups
import re

users = getgroups()

for i in users:
	print(i)
