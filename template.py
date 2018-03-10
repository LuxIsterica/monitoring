import sys
sys.path.append('systemcalls')
from user import getusers, getuser
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app=Flask(__name__, template_folder="templates", static_folder = "static", static_url_path="/static")
bootstrap=Bootstrap(app)

#http://localhost:5000/
# definizione base index con componente fissa navbar
@app.route('/')
def index():
	return render_template('index.html')

# http://localhost:5000/listUser/
@app.route('/listUser')
def listUser():
	users=getusers()
	return render_template('users.html',users=users)

# http://localhost:5000/getInfoUser/<clicca valore uname>
@app.route('/getInfoUser/<string:uname>')
def getInfoUser(uname):
	infouser=getuser(uname)
	return render_template('info-user.html',infouser=infouser)

if __name__ == '__main__':
	app.run(debug=True)