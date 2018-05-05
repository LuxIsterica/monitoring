import sys
sys.path.append('systemcalls')
from user import getusers, getuser, getgroups, getshells, updateusershell
from apps import listinstalled, aptsearch
from systemfile import locate
from system import getsysteminfo, hostname
from network import ifacestat
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from collections import defaultdict

app = Flask(__name__, template_folder = "templates", static_folder = "static", static_url_path = "/static")
app.secret_key = 'random string'
bootstrap = Bootstrap(app)

##### FUNZIONALITÀ user.py #####

#http://localhost:5000/dash
# definizione base dash con componente fissa navbar
@app.route('/dash')
def dash():
<<<<<<< Updated upstream
	#error = None
	#tpl = getsysteminfo()
	#if tpl['returncode'] != 0:
	#	flash(tpl['stderr'])
	#else:
	#	(cpu,mem,proc) = tpl['data']
	#	return render_template('dash.html', cpu = cpu, mem = mem, proc = proc)

	#return render_template('dash.html')
=======
#	error = None
#	tpl = getsysteminfo()
#	if tpl['returncode'] != 0:
#		flash(tpl['stderr'])
#	else:
#		(cpu,mem,proc) = tpl['data']
#		return render_template('dash.html', cpu = cpu, mem = mem, proc = proc)

#	return render_template('dash.html')
>>>>>>> Stashed changes
	tpl = getsysteminfo()
	(cpu,mem,proc) = tpl['data']
	return render_template('dash.html', cpu = cpu, mem = mem, proc = proc)

# http://localhost:5000/listUser/
@app.route('/listUserAndGroups')
def listUserAndGroups():
	users = getusers()
	groups = getgroups()

	if users['returncode'] != 0 or groups['returncode'] != 0:
		flash("getusers or getgroups fallita")
	else:
		return render_template('users.html', users = users,groups = groups)

	return redirect(url_for('listUserAndGroups'))

# http://localhost:5000/getInfoUser/<clicca valore uname>
@app.route('/getInfoUser/<string:uname>')
def getInfoUser(uname):
	infouser = getuser(uname)
	shells = getshells()
	return render_template('info-user.html', infouser = infouser, shells = shells)

@app.route('/updateShell', methods=['POST'])
def updateShell():
	error = None
	uname = request.form['unameUpdate'];
	shell = request.form['newShell'];
	if shell == '-- Seleziona nuova shell --':
		flash('Opzione nuova shell non valida')
	else:
		log = updateusershell(uname, shell)
		if(log['returncode'] != 0):
			flash(log['stderr'])
			flash(log['command'])
		else:
			flash('Comando shell modificato correttamente')
	
	return redirect(url_for('listUserAndGroups'))
	#return render_template('info-user.html', log = log)

##### FUNZIONALITÀ apps.py #####

# http://localhost:5000/listInstalled
@app.route('/listInstalled')
def listInstalled():
	listAppInst = listinstalled(True)
	return render_template('applications.html', listAppInst = listAppInst)

@app.route('/findPkgInstalled', methods=['POST'])
def findPkgInstalled():
	error = None
	pkg = request.form['pkgSearch'];
	if not pkg:
		flash('Operazione errata')
		return redirect(url_for('listInstalled'))
	appFound = aptsearch(pkg)
	return render_template('find-pkg-installed.html', appFound = appFound)

##### FUNZIONALITÀ file.py #####
@app.route('/file')
def file():
	return render_template('file.html')

@app.route('/findFile', methods=['POST'])
def findFile():
	error = None
	fs = request.form['fileSearch'];
	if not fs:
		flash('Operazione errata')
	else:
		pathFileFound = locate(fs);
		return render_template('file.html', pathFileFound = pathFileFound)
		
	return redirect(url_for('file'))

##### FUNZIONALITÀ system.py #####
@app.route('/param')
def param():
	error = None
	hname = hostname()
	if(hname['returncode'] != 0):
		flash(hname['stderr'])
		flash(hname['command'])
	else:
		return render_template('param.html', hname=hname)

	return render_template('param.html')

@app.route('/newHostname', methods=['POST'])
def newHostname():
	error = None
	hname = request.form['newHname'];
	if not hname:
		flash('Hostname non può essere vuoto!')
	else:
		log = hostname(hname)
		if(log['returncode'] != 0):
			flash(log['stderr'])
			flash(log['command'])
		else:
			flash('Hostname modificato correttamente')
	
	return redirect(url_for('param'))

##### FUNZIONALITÀ systemfile.py #####

##### FUNZIONALITÀ network.py #####
@app.route('/network')
def network():
	facestat = ifacestat()
	return render_template('net.html', facestat=facestat)

if __name__ == '__main__':
	app.run(debug = True)
