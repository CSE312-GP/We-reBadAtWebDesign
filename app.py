#Backend Python for our server
from flask import Flask, Response, render_template, make_response, send_file

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

@app.route('/public/style_index.css')
def serveCSS():
    response = send_file('public/style_index.css',mimetype='text/css')
    return response

@app.route('/public/javascript.js')
def serveJS():
    response = send_file('public/javascript.js',mimetype='text/javascript')
    return response

@app.route('/public/images/loginpage.jpg')
def serveAnimeImage():
    response = send_file('public/images/loginpage.jpg',mimetype='image/jpeg')
    return response

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)