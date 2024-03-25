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

@app.route('/AnimeChatApp', methods=['GET'])
def serveAnimeChatApp():
    response = make_response(render_template('loggedin.html'))
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

# ===========
# Register
# ===========
@app.route('/register', methods=['POST'])
def serveRegister():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    # print testing
    # accounts in db
    # for account in account_collection.find():
    #     data = {"username": account["username"], "password": account["password"], "salt": account["salt"], "auth": account["auth"]}
    #     flash(str(data))

    # grab username, password, and confirm password. Make sure to html injection protect.
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

    # display success message and redirect
    flash("Account Created!")
    response = redirect("/", code=302)
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

# ===========
# Login
# ===========
@app.route('/login', methods=['POST'])
def serveLogin():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    # get login credentials
    username = request.form["username_login"]
    password = request.form["password_login"]

    # check if user exists
    for account in account_collection.find():
        data = {"username": account["username"], "password": account["password"], "salt": account["salt"]}
        salted_password = password + data["salt"]

        # if account exists
        if data["username"] == username and data["password"] == str(sha256(salted_password.encode('utf-8')).hexdigest()):
            # update auth in database to hashed auth token
            auth_token = token_gen()
            hashed_auth_token = sha256(auth_token.encode('utf-8')).hexdigest()
            my_query = {"username": username}
            new_values = {"$set": {"auth": str(hashed_auth_token)}}
            account_collection.update_one(my_query, new_values)

            # set cookie in response to auth token plain text
            response = redirect("/AnimeChatApp", code=302)
            response.set_cookie("AnimeApp_Auth", str(auth_token), max_age=3600, httponly=True)

            # redirect to new page
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            return response

    # redirect to the login page if password incorrect
    flash("Username or password is incorrect", "error")
    response = redirect("/", code=302)
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

# ===========
# Post Message
# ===========
@app.route('/chat_messages', methods=['POST'])
def postMessage():
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    chat_collection = db["chat"]
    account_collection = db["accounts"]
    id_counter = db["id"]

    # Checking for the auth token to determine users from guests
    if "AnimeApp_Auth" in request.cookies:
        username = account_collection.find_one({"auth": request.cookies["AnimeApp_Auth"]})
    else:
        username = "Guest"

    # Create a unique id for the message by using a database.
    # count_documents does not work, since deleting a message could cause duplicate ids.
    if id_counter.find_one({}) is None:
        message_id = "0"
        id_counter.insert_one({'last_used': 0})
    else:
        last_id = id_counter.find_one({})['last_used']
        x = int(last_id) + 1
        message_id = str(x)
        id_counter.update_one({}, {'$set': {'last_used': x}})

    # Get the message here
    message = request.form["message_post"]

    # Add the message to the database, along with its id and the sender's username
    chat_collection.insert_one({"username": username, "id": message_id, "message": message})

# ===========
# Get Chat
# ===========
@app.route('/chat_messages', methods=['GET'])
def getMessage():
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    chat_collection = db["chat"]

    all_data = list(chat_collection.find({}, {'_id': 0}))
    response = make_response(all_data, 200)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host='0.0.0.0',port=8080)
