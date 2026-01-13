from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "✅ RenameProBot Web Alive"

@app.get("/health")
def health():
    return "OK"
