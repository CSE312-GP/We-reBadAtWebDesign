#Backend Python for our server
from flask import Flask 
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

'''def main():
    host = "0.0.0.0"
    port = 8080
    print("Listening on port " + str(port))'''


if __name__ == "__main__":
    app.run(debug=True)
