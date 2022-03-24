import os
from flask import Flask, flash, render_template , redirect, url_for , request
from flask_pymongo import PyMongo
from itsdangerous import exc
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
dirname = os.path.dirname(__file__)
filenamepath = os.path.join(dirname, '\res')
app.config['UPLOAD_FOLDER'] = filenamepath
app.secret_key = 'super67sEcret459!!key@s'
mongo = PyMongo(app)
print('---LOG: best debug method: WEBSITE: OK')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['pass']

      email_found = mongo.db.users.find_one({"email": email})
      if(email_found):
          print("---LOG: memory loss!")
          #print user already exists message
          return redirect(url_for('fail',name = email))
      else:
        #create user inside mongo
        user_data = {'email': email, 'password': password}
        mongo.db.users.insert_one(user_data)
        print('---LOG: great success')
        return redirect(url_for('success',name = email))
    else: #get method
      return render_template("signup.html")

@app.route('/success/<name>')
#signup sucess
def success(name):
   return 'welcome %s' % name

@app.route('/fail/<name>')
#signup fail
def fail(name):
    return 'User %s already exists.' % name

@app.route('/auth',methods = ['POST', 'GET'])
def auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        #auth check

        user = mongo.db.users.find_one({"email": email, "password": password})
        try:
            db_email=str(user.get('email'))
            db_password=str(user.get('password'))
            if(db_email==email and db_password==password):
                #secret
                return render_template("secret.html")
            else:
                flash("Wrong username or password!")
                return render_template('index.html')
        except:
            flash("Wrong username or password!")
            return render_template('index.html')
    else: #get method
        return render_template("login.html")

@app.route('/upload',methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
                flash('No file in post.')
                return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    else: # GET
        return render_template("upload.html")

VALID_FILE_TYPES = {'png','jpg','jpeg','pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in VALID_FILE_TYPES

app.run(host='localhost', port=5000)