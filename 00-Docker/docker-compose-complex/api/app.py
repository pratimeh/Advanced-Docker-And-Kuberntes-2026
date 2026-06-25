from flask import Flask

app = Flask(__name__)

@app.route("/message")
def message():
    with open("/data/message.txt") as f:
        return f.read()

app.run(host="0.0.0.0", port=5000)
