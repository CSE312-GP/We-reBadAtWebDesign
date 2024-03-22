#Backend Python for our server
from flask import Flask, Response, flash, redirect, render_template, make_response, request, send_file
from hashlib import sha256

from pymongo import MongoClient

from Public.response_functions import token_gen

app = Flask(__name__)

#This decorator (the @ sign) makes the function setXContentTypeOptions run after recieve each request
@app.after_request
def setXContentTypeOptions(response: Response):
    response.headers.add('X-Content-Type-Options', 'nosnif')
    return response

@app.route('/')
def serveHTML():
    response = make_response(render_template('index.html'))
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

@app.route('/Public/style_index.css')
def serveCSS():
    response = send_file('Public/style_index.css',mimetype='text/css')
    return response

@app.route('/Public/javascript.js')
def serveJS():
    response = send_file('Public/javascript.js',mimetype='text/javascript')
    return response

@app.route('/Public/images/loginpage.jpg')
def serveAnimeImage():
    response = send_file('Public/images/loginpage.jpg',mimetype='image/jpeg')
    return response

@app.route('/Public/loggedin.html')
def serveHTML2():
    response = make_response(render_template('loggedin.html'))
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

@app.route('/Public/loggedin.css')
def serveCSS2():
    response = send_file('Public/loggedin.css',mimetype='text/css')
    return response

@app.route('/Public/feed.js')
def serveJS2():
    response = send_file('Public/feed.js',mimetype='text/javascript')
    return response

@app.route('/register', methods=['POST'])
def serveRegister():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    # grab username, password, and confirm password
    username = request.form["username_registration"]
    password = request.form["password_registration"]
    confirm_password = request.form["password_confirmation"]

    # test for if username is blank
    if username == "":
        flash("Username can't be empty", "error")
        response = redirect("/", code=302)
        return response
    
    # test for if password is blank
    if password == "":
        flash("Password can't be empty", "error")
        response = redirect("/", code=302)
        return response

    # test if username already exists
    for account in account_collection.find():
        data = {"username": account["username"]}
        if data["username"] == username:
            flash("Username already exists", "error")
            response = redirect("/", code=302)
            return response

    # test if passwords are different
    if password != confirm_password:
        flash("Passwords don't match", "error")
        response = redirect("/", code=302)
        return response

    # salt and hash password
    salt = token_gen()
    salted_password = password + salt
    hashed_salted_password = sha256(salted_password.encode()).hexdigest()

    # add credentials and salt to database
    account_collection.insert_one({"username": str(username), "password": str(hashed_salted_password), "salt": str(salt), "auth": ""})

    # print testing
    # accounts in db
    # for account in account_collection.find():
    #     data = {"username": account["username"], "password": account["password"], "salt": account["salt"], "auth": account["auth"]}
    #     flash(str(data)) 

    flash("Account Created!")
    response = redirect("/", code=302)
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host='0.0.0.0',port=8080)
