import flask

app = flask.Flask(__name__)

@app.get("/")
def hello():

    return "This microservice will be used for the team managment functionality.\n"

if __name__ == "__main__":
    
    app.run(host="localhost", port=8080, debug=True)