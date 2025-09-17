# from flask import Flask

# app = Flask(__name__)

# @app.route("/name")
# def lwname():
#          return "i am ruturaj gidde"

# @app.route("/phone")
# def lwphone():
#          return "9309982768.."

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
        

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"<h1>Welcome to Ruturaj's Flask App!  {os.environ['HOSTNAME']}</h1><p>Visit /name or /phone to see details.</p>"

@app.route("/name")
def lwname():
    return "I am Ruturaj Gidde"

@app.route("/phone")
def lwphone():
    return "9309982768"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
