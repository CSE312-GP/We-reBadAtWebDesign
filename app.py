#Backend Python for our server
import json
import sys
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
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    # check if auth cookie exists
    if "AnimeApp_Auth" not in request.cookies:
        response = make_response(render_template('index.html'))
        response.headers.add('Content-Type', 'text/html; charset=utf-8')
        return response
    
    # check if auth token is legit
    user_auth = request.cookies["AnimeApp_Auth"]
    for account in account_collection.find():
        account_data = {"username": account["username"], "auth": account["auth"]}
        # if user is legit then redirect to /AnimeChatApp
        if account_data["auth"] == sha256(user_auth.encode()).hexdigest():
            response = redirect("/AnimeChatApp", code=302)
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            return response
    # if user is not legit send normal html
    response = make_response(render_template('index.html'))
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

@app.route('/AnimeChatApp', methods=['GET'])
def serveAnimeChatApp():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    user_auth = request.cookies["AnimeApp_Auth"]
    user_username = ""
    for account in account_collection.find():
        account_data = {"username": account["username"], "auth": account["auth"]}
        if account_data["auth"] == sha256(user_auth.encode('utf-8')).hexdigest():
            user_username = account_data["username"]
            # replace {{username}}
            response = make_response(render_template('loggedin.html', username=user_username))
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            return response
    
    response = redirect("/", code=302)
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
@app.route('/submit-post', methods=['POST'])
def postMessage():
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]
    chat_collection = db["chat"]

    # Checking for the auth token to determine users from guests
    if "AnimeApp_Auth" not in request.cookies:
        # send to login
        response = redirect("/", code=302)
        response.headers.add('Content-Type', 'text/html; charset=utf-8')
        return response
    
    
    # check if auth is valid
    user_auth = request.cookies["AnimeApp_Auth"]
    for account in account_collection.find():
        accout_data = {"username": account["username"], "auth": account["auth"]}
        if accout_data["auth"] == sha256(user_auth.encode('utf-8')).hexdigest():
            # add post to chat collection
            message = request.json
            # for debugging
            print(message, file=sys.stderr)
            chat_collection.insert_one({"username": accout_data["username"], "anime": message["anime"], 
                                        "review": message["review"], "id": message["id"], "likes": []})
            response = make_response("Valid Post", 200)
            return response
        
    # if not valid auth
    response = make_response("Not allowed", 403)
    return response


# ===========
# Get Chat
# ===========
@app.route('/feed', methods=['GET'])
def getMessage():
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    chat_collection = db["chat"]

    all_data = list(chat_collection.find({}, {'_id': 0}))
    all_data = json.dumps(all_data)
    response = make_response(all_data, 200)
    return response

# ==============
# Like_Button
# ==============
@app.route('/like', methods=['POST'])
def serveLike():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]
    chat_collection = db["chat"]

    # match account with the message in body from auth token
    for account in account_collection.find():
        account_data = {"username": account["username"], "auth": account["auth"]}
        if "AnimeApp_Auth" not in request.cookies:
            response = redirect("/", code=302)
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            return response
        user_auth = request.cookies["AnimeApp_Auth"]
        liked_message_info = request.json
        # if auth tokens match and user is not in the liked list already
        if account_data["auth"] != sha256(user_auth.encode('utf-8')).hexdigest():
            # send 403 response
            response = make_response("Not allowed", 403)
            return response
        else:
            # Look for if message exists
            for chat in chat_collection.find():
                chat_data = {"username": chat["username"], "anime": chat["anime"], "review": chat["review"], 
                        "id": chat["id"], "likes": chat["likes"]}
                # make sure message id matches the liked message
                if chat_data["id"] == liked_message_info["id"]:
                    user_liked_message = False
                    for liked_user in chat_data["likes"]:
                        if liked_user == chat_data["username"]:
                            user_liked_message = True
                    # if user has already liked message send 403
                    if user_liked_message:
                        response = redirect("/", code=302)
                        response.headers.add('Content-Type', 'text/html; charset=utf-8')
                        return response
                    # if user hasn't liked message then add user to the likes array
                    else:
                        chat_data["likes"].append(chat_data["username"])
                        response = make_response("Valid Like", 200)
                        return response
# ===========
# Logout
# ===========
@app.route('/logout', methods=['POST'])
def serveLogout():
    # database connection
    mongo_client = MongoClient("mongo")
    db = mongo_client["BadAtWebDesign"]
    account_collection = db["accounts"]

    # check if auth cookie exists
    if "AnimeApp_Auth" not in request.cookies:
        response = redirect("/", code=302)
        response.headers.add('Content-Type', 'text/html; charset=utf-8')
        return response
    
    # check if auth token is legit
    user_auth = request.cookies["AnimeApp_Auth"]
    for account in account_collection.find():
        account_data = {"username": account["username"], "auth": account["auth"]}
        # if legit user then set auth in db to null and remove cookie
        if account_data["auth"] == sha256(user_auth.encode()).hexdigest():
            # delete auth token in database
            my_query = {"auth": str(sha256(user_auth.encode()).hexdigest())}
            new_values = {"$set": {"auth": ""}}
            account_collection.update_one(my_query, new_values)
            # delete auth cookie
            response = redirect("/", code=302)
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            response.set_cookie("AnimeApp_Auth", "", max_age=0, httponly=True)
            return response
        else:
            # if not a legit user then just delete the cookie
            response = redirect("/", code=302)
            response.headers.add('Content-Type', 'text/html; charset=utf-8')
            response.set_cookie("AnimeApp_Auth", "", max_age=0, httponly=True)
            return response


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host='0.0.0.0',port=8080)
