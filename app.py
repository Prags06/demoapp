from flask import Flask

app = Flask(__name__)

@app.route("/name")
def lwname():
         return "i am ruturaj gidde"

@app.route("/phone")
def lwphone():
         return "9309982768.."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
        