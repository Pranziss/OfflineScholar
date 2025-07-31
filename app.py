from flask import Flask
from routes.ask import ask_bp
from routes.journal import journal_bp
from routes.history import history_bp
from routes.meta import meta_bp

app = Flask(__name__)
app.register_blueprint(ask_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(history_bp)
app.register_blueprint(meta_bp)

if __name__ == "__main__":
    print("🚀 Nova is booting up on http://192.168.1.10:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)