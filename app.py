from flask import Flask, request, render_template
import os

app = Flask(__name__)

data = {
    "mq2": "N/A",
    "door": "N/A"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=data)

@app.route("/update", methods=["POST"])
def update():
    mq2 = request.form.get("mq2")
    door = request.form.get("door")

    if mq2 is not None and door is not None:
        data["mq2"] = mq2
        data["door"] = "ABIERTA" if door == "1" else "CERRADA"
        return "OK", 200
    return "ERROR", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
