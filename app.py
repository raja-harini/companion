from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/run/english", methods=["GET"])
def run_english():
    subprocess.Popen(["python", r"C:\\Users\\admin\\Desktop\\companio\\navinenglish.py"])
    return "English assistant started."

@app.route("/run/tamil", methods=["GET"])
def run_tamil():
    subprocess.Popen(["python", r"C:\\Users\\admin\\Desktop\\companio\\navintamil.py"])
    return "Tamil assistant started."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Make sure host is 0.0.0.0
