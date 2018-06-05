import sys
sys.path.append('systemcalls')
from user import getusers, getuser, getgroups, getshells, updateusershell, getusernotgroups, getusergroups
from apps import listinstalled, aptsearch
from systemfile import locate,updatedb
from system import getsysteminfo, hostname
#from network import ifacestat
from apache import apachestart, apachestop, apacherestart, apachereload, apachestatus, getvhosts, activatevhost, deactivatevhost
from cron import listcrontabs, getcrontabcontent
from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from network import ifacestat
from flask import Flask, render_template, flash, request, redirect, url_for

from flask_bootstrap import Bootstrap
from collections import defaultdict

app = Flask(__name__, template_folder = "templates", static_folder = "static", static_url_path = "/static")
app.secret_key = 'random string'
bootstrap = Bootstrap(app)

########## FUNZIONALITÀ user.py ##########

#http://localhost:5000/dash
# definizione base dash con componente fissa navbar
@app.route('/dash')
def dash():
#	error = None
#	tpl = getsysteminfo()
#	if tpl['returncode'] != 0:
#		flash(tpl['stderr'])
#	else:
#		(cpu,mem,proc) = tpl['data']
#		return render_template('dash.html', cpu = cpu, mem = mem, proc = proc)
	tpl = getsysteminfo()
	(cpu,mem,proc) = tpl['data']
	return render_template('dash.html', cpu = cpu, mem = mem, proc = proc)

# http://localhost:5000/listUser/
@app.route('/listUserAndGroups')
def listUserAndGroups():
	error = None
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
	nogroups = getusernotgroups(uname)
	groupsuser = getusergroups(uname)
	return render_template('info-user.html', infouser = infouser, shells = shells, nogroups = nogroups, groupsuser=groupsuser)

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

@app.route('/addUserGroup', methods=['POST'])
def addUserGroup():
	error = None
	uname = request.form['unameAdd'];
	moreGr = request.form['moreGroups'];
	if moreGr == '-- Seleziona uno o più dei seguenti gruppi --':
		flash('Opzione non valida')
	else:
		log = addusertogroups(uname, moreGr)
		if(log['returncode'] != 0):
			flash(log['stderr'])
			flash(log['command'])
		else:
			flash('User aggiunto correttamente al/i gruppo/i')
	
	return redirect(url_for('listUserAndGroups'))

@app.route('/removeUserGroup', methods=['POST'])
def removeUserGroup():
	error = None
	uname = request.form['unameRem'];
	moreGr = request.form['moreGroups'];
	if moreGr == '-- Seleziona uno o più dei seguenti gruppi --':
		flash('Opzione non valida')
	else:
		log = removeuserfromgroups(uname, moreGr)
		if(log['returncode'] != 0):
			flash(log['stderr'])
			flash(log['command'])
		else:
			flash('User eliminato correttamente dal/i gruppo/i')
	
	return redirect(url_for('listUserAndGroups'))

########## FUNZIONALITÀ cron.py ##########

@app.route('/listCron')
def listCron():
	listCrontabs = listcrontabs()
	return render_template("jobs.html",listCrontabs=listCrontabs)

@app.route('/getContentCrontab/<string:cronk>/<string:cronv>')
def getContentCrontab(cronk,cronv):
	basedir='/etc/'
	pathCron=basedir+cronk+'/'+cronv
	content = getcrontabcontent(pathCron)
	#return send_file(pathCron,attachment_filename=cronv) fa il download
	return render_template("jobs.html", content=content, pathCron=pathCron)

@app.route('/updateCrontab/<string:pathCron>', methods=['POST'])
def updateCrontab(pathCron):
	#manca contenuto
	error = None
	updatedCrontab = request.form['content-textarea']
	#aggingi contenuto textarea
	log = writecron(pathCron, updatedCrontab)
	if(log['returncode'] != 0):
		error = log['command']
	else:
		flash('Crontab modificato correttamente!')
		return redirect(url_for('listCron'))
	return render_template('listCron.html',error=error)

########## FUNZIONALITÀ apps.py ##########

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

########## FUNZIONALITÀ file.py ##########

@app.route('/file')
def file():
	return render_template('file.html')

@app.route('/findFile', methods=['POST'])
def findFile():
	error = None
	fs = request.form['fileSearch'];
	if not fs:
		flash(u'Operazione errata','error')
	else:
		pathFileFound = locate(fs);
		return render_template('file.html', pathFileFound = pathFileFound)
		
	return redirect(url_for('file'))

@app.route('/updateDbFile', methods=['POST'])
def updateDbFile():
	error = None
	if request.form['updateDbFile'] == 'Aggiorna DB File':
		log = updatedb()
		if(log['returncode'] != 0):
			error = log['command']
		else:
			flash(u'Aggiornato!','info')
			return redirect(url_for('file'))
	else:
		error = 'Non funzica' 
	return render_template('file.html', error=error)

########## FUNZIONALITÀ system.py ##########

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

########## FUNZIONALITÀ systemfile.py ##########

########## FUNZIONALITÀ network.py ##########
#@app.route('/network')
#def network():
#	facestat = ifacestat()
#	return render_template('network.html', facestat=facestat)

########## FUNZIONALITÀ apache.py ##########

@app.route('/startApache', methods=['POST'])
def startApache():
	error = None
	if request.form['b-start-a'] == 'Start':
		log = apachestart()
		if(log['returncode'] != 0):
			error = log['stderr']
		else:
			flash("Apache startato correttamente")
			return redirect(url_for('getVHosts'))
	else:
		error = 'Non funzica' 
	return render_template('apache.html', error=error)

#errore 500
@app.route('/stopApache', methods=['POST'])
def stopApache():
	error = None
	if request.form['b-stop-a'] == 'Stop':
		log = apachestop()
		if(log['returncode'] != 0):
			error = log['stderr']
		else:
			flash("Apache stoppato correttamente")
			return redirect(url_for('getVHosts'))
	else:
		error = 'Non funzica' 
	return render_template('apache.html', error=error)

# return HTTP/1.1" 302
@app.route('/restartApache', methods=['POST'])
def restartApache():
	error = None
	if request.form['b-restart-a'] == 'Restart':
		log = apacherestart()
		if(log['returncode'] != 0):
			error = log['stderr']
		else:
			flash("Restart Apache avvenuto correttamente")
			return redirect(url_for('getVHosts'))
	else:
		error = 'Non funzica' 
	return render_template('apache.html', error=error)

@app.route('/reloadApache', methods=['POST'])
def reloadApache():
	error = None
	if request.form['b-reload-a'] == 'Reload':
		log = apachereload()
		if(log['returncode'] != 0):
			error = log['stderr']
		else:
			flash("Reload Apache avvenuto correttamente")
			return redirect(url_for('getVHosts'))
	else:
		error = 'Non funzica' 
	return render_template('apache.html', error=error)

@app.route('/statusApache', methods=['POST'])
def statusApache():
	error = None
	if request.form['b-status-a'] == 'Status':
		logStatus = apachestatus()
		if(logStatus['returncode'] != 0):
			error = logStatus['stderr']
		else:
			return render_template('apache.html', logStatus=logStatus)
	else:
		error = 'Non funzica' 
	return render_template('apache.html', error=error)

@app.route('/getVHosts')
def getVHosts():
	error=None
	vhost=getvhosts()
	if(vhost['returncode'] != 0):
		flash(vhost['stderr'])
		flash(vhost['command'])
	else:
		return render_template('apache.html', vhost=vhost)

#creating a view function without returning a response in Flask
# return HTTP/1.1" 204
@app.route('/activateVHost', methods=['POST'])
def activateVHost():
	filename = request.form['clickActiv']
	if filename:
		logAVHost=activatevhost(filename)
		if(logAVHost['returncode'] != 0):
			flash(logAVHost['stderr'])
			flash(logAVHost['command'])
			#return redirect(url_for('getVHosts'))
			return '',204
	#return redirect(url_for('getVHosts'))
	return '',204 #ritorno senza reindirizzamento con flask

@app.route('/deactivateVHost', methods=['POST'])
def deactivateVHost():
	filename = request.form['clickDeactiv']
	if filename:
		logDAVHost=deactivatevhost(filename)
		if(logDAVHost['returncode'] != 0):
			flash(logDAVHost['stderr'])
			flash(logDAVHost['command'])
			#return redirect(url_for('getVHosts'))
			return '',204
	#return redirect(url_for('getVHosts'))
	return '',204 #ritorno senza reindirizzamento con flask



if __name__ == '__main__':
	app.run(debug = True)
