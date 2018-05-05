import sys
sys.path.append('systemcalls')
from system import getsysteminfo
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from collections import defaultdict

app = Flask(__name__, template_folder = "templates", static_folder = "static", static_url_path = "/static")
app.secret_key = 'random string'
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	tpl = getsysteminfo(getall=False,getproc=True)
	#(cpu,mem,proc) = tpl['data']
	proc = tpl['data']
	#return render_template('scheduler.html', cpu = cpu, mem = mem, proc = proc)
	return render_template('scheduler.html', proc = proc)


if __name__ == '__main__':
	app.run(debug = True)
