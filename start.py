import threading
import os
from flask import Flask

flask_app = flask(__name__)

@flask_app.route('/')
def hello_world():
    return 'Hello from render'

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

flask_thread =
threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

os.system("python main.py")
