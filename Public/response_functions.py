# ==================================
# Functions for message creation
# ==================================
def addokresponse():
    message = " 200 OK\r\n"
    return message


def add302response():
    message = " 302 Found\r\n"
    return message


def add302mainsiteredirect():
    message = "Location: localhost:8080"
    return message


def add302registerredirect():
    message = " 302 Found\r\nX-Content-Type-Options: nosniff\r\nLocation: localhost:8080"
    return message


def setauthtokencookie(auth_token):
    message = "Set-Cookie: auth_token_312=" + auth_token + "; Max-Age=3600; HttpOnly\r\n"
    return message

def setxsrftokencookie(xsrf_token):
    message = "Set-Cookie: xsrf_token_312=" + xsrf_token + "; Max-Age=3600; HttpOnly\r\n"
    return message


def deleteauthcookie():
    message = "Set-Cookie: auth_token_312=; Max-Age=0; HttpOnly\r\n"
    return message


def postchatresponse(request):
    message = request.http_version + " 200 OK\r\nContent-Type: text/plain\r\n" \
                                     "Content-Length: 19\r\nX-Content-Type-Options: nosniff\r\n\r\n" \
                                     "Nice Message There!"
    return message

def deletechatsucessresponse(request):
    message = request.http_version + (" 200 OK\r\nContent-Type: text/plain\r\n"
                                      "Content-Length: 16\r\nX-Content-Type-Options: nosniff\r\n\r\n"
                                      "Message deleted.")
    return message

def noSniff():
    message = "X-Content-Type-Options: nosniff\r\n"
    return message

    # add Content-Type of index.html


def addContentTypeForIndex():
    message = "Content-Type: text/html; charset=utf-8\r\n"
    return message

    # add Content-Length of index.html


def addContentLengthForIndex(body):
    # ask about getting the index.html
    body_size = len(body)
    message = "Content-Length: " + str(body_size) + "\r\n"
    return message


def error404Message(request):
    message = request.http_version + " 404 Not Found\r\nContent-Type: text/plain\r\n" \
                                     "Content-Length: 36\r\nX-Content-Type-Options: nosniff\r\n\r\n" \
                                     "The requested content does not exist"
    return message


def add403response(request):
    message = request.http_version + (" 403 Forbidden\r\nContent-Type: text/html\r\n"
                                      "X-Content-Type-Options: nosniff\r\n")
    body = open("./public/403 Response.html", "rb").read().decode("utf-8")
    message += "Content-Length: " + str(len(body)) + "\r\n\r\n"
    message += body
    return message


def addHeaders(request):
    message = ""
    for header in request.headers:
        message += header + ": " + request.headers[header] + "\r\n"
    return message


def addContentTypeGen(request):
    message = ""
    if "txt" in request.path:
        message += "Content-Type: text/plain;charset=UTF-8\r\n"
    elif "js" in request.path:
        message += "Content-Type: text/javascript;charset=UTF-8\r\n"
    elif "html" in request.path:
        message += "Content-Type: text/html;charset=UTF-8\r\n"
    elif "css" in request.path:
        message += "Content-Type: text/css\r\n"
    elif "png" in request.path:
        message += "Content-Type: image/png\r\n"
    elif "jpg" in request.path:
        message += "Content-Type: image/jpeg\r\n"
    elif "mp4" in request.path:
        message += "Content-Type: video/mp4\r\n"
    elif "json" in request.path:
        message += "Content-Type: application/json\r\n"
    elif "chat-messages" in request.path:
        message += "Content-Type: application/json\r\n"
    elif ".ico" in request.path:
        message += "Content-Type: image/x-icon\r\n"
    return message


def addContentLengthGen(response):
    file_name = "." + response.path
    file_stats = len(open(file_name, "rb").read())
    message = "Content-Length: " + str(file_stats) + "\r\n"
    return message


def addContentLengthChat(data):
    data_size = len(data)
    message = "Content-Length: " + str(data_size) + "\r\n"
    return message


def addCookieOnSiteVisit(request):
    message = ""
    # Check for if cookies exist
    cookies_header_exists = False
    for key in request.headers:
        # if cookies exist
        if key == "Cookie":
            cookies_header_exists = True

    # Add cookie for site visited
    if cookies_header_exists == False:
        message += "Set-Cookie: visits=1; Max-Age=3600\r\n"
    else:
        visits_cookie_exists = False
        for cookie in request.cookies:
            if cookie == "visits":
                visits_cookie_exists = True
        if visits_cookie_exists:
            request.cookies["visits"] = int(request.cookies["visits"]) + 1
            message += "Set-Cookie: visits=" + str(request.cookies["visits"]) + "; Max-Age=3600\r\n"
        else:
            message += "Set-Cookie: visits=1; Max-Age=3600\r\n"
    return message


def token_gen():
    token_string = ""
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    token = []
    alphabet_length = len(alphabet) - 1
    for c in range(0, 20):
        token.append(alphabet[random.randint(0, alphabet_length)])
    return token_string.join(token)
