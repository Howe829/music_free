from flask import Flask
from flask import request
from flask import send_file
import os
app = Flask(__name__)

error = None


@app.route('/<filename>')
def hello_world(filename):
    path = '/home/alexhowe/upload/'+filename
    print(filename)
    if os.path.exists(path):
       return send_file(path)
    else:
        return 'File Not Found!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'], request.form['password'])
        return 'Login Success!'
    else:
       return "Where do you find this link?"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form['username'], request.form['password'])
        return 'Login Success!'
    else:
       return 'Where do you find this link?'
@app.route('/upload/<filename>',methods=['POST','GET'])
def upload(filename):
    path = '/home/alexhowe/upload/'+filename
    if request.method == 'POST':
        f = request.files['file']
        f.save(path)
        return path
    else:
        return 'Upload failed!'



if __name__ == '__main__':
    app.run()
