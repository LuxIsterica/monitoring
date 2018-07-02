@app.route('/addCron', methods=['POST'])
	try:
		error = None
		command=request.form["command"] 
		name=request.form["nameCron"] 
		user=request.form["user"] 
		minute=request.form["minute"] 
		hour=request.form["hour"] 
		dom=request.form["dayOfMounth"] 
		month=request.form["mounth"] 
		dow=request.form["dayOfWeek"]
		if not command:
			error = "Command cannot be empty"
		else:
			log = addcron(command, name, user, minute, hour, dom, month, dow)
			if log['returncode'] != 0:
				error = "Add cron failed"
			else:
				flash("Cron added correctly")
		return render_template("jobs.html",error=error)	
	except Exception:
		return internal_server_error(500)

@app.route('/addCustomCron', methods=['POST'])
	try:
		error = None
		command=request.form["command"] 
		name=request.form["nameCron"]
		typeOption = request.form["typeOption"]
		if not command:
			error = "Command cannot be empty"
		else:
			if typeOption == 'ogni ora':
				log = addhourlycron(command, name)
			elif typeOption == 'ogni giorno':
				log = adddailycron(command, name)
			elif typeOption == 'ogni settimana':
				log = addweeklycron(command, name)
			elif typeOption == 'ogni mese':
				log = addmonthlyycron(command, name)
				
			if log['returncode'] != 0:
				error = "Add cron failed"
			else:
				flash("Cron added correctly")
		return render_template("jobs.html",error=error)	
	except Exception:
		return internal_server_error(500)



