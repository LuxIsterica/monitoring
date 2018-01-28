from subprocess import Popen, PIPE


def getuser(user=None):
	p1 = Popen(['getent', 'passwd',  user], stdout=PIPE, universal_newlines=True).communicate()[0]
	output = p1.splitlines()
	output = output[0].split(':')
	users = list()
	users.append({
		'uname': output[0],
		'canlogin': 'yes' if output[1]=='x' else 'no',
		'uid': output[2],
		'gid': output[3],
		'geco': output[4].split(','),
		'home': output[5],
		'shell': output[6]
	})
	
	return users

def getuserslist():
	p1 = Popen(["cat", "/etc/passwd"], stdout=PIPE)
	p2 = Popen(["cut", "-d:", "-f4-", "--complement"], stdin=p1.stdout, stdout=PIPE, universal_newlines=True).communicate()[0]
	p1.stdout.close()
	#universal newlines serve a restutuire l'output come stringa e non come bytes
	#p3 = Popen(["sed", "s/:.:/:/g"], stdin=p2.stdout, stdout=PIPE, universal_newlines=True).communicate()[0] #, stdout=outputfile)
	#p2.stdout.close()

	output = p2.splitlines()

	users = list()
	for i in output:
		actual = i.split(':')
		users.append({
			'uname': actual[0],
			'uid': actual[2]
	})

	return users


	#print(users)
	#print(*string, sep='\n')

	#for line in p1.stdout:
	#	print(line)
	#
	#p2.stdout.close()
