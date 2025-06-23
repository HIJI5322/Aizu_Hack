from flask import Flask, render_template
from flask_cors import CORS

from AIsupport import AIsupport_bp
from standard import standard_bp
from chatlike import chat_like_bp
from Extreme import Extreme_bp

app = Flask(__name__)
CORS(app) 

app.register_blueprint(AIsupport_bp, url_prefix='/AIsupport')
app.register_blueprint(chat_like_bp, url_prefix='/chatlike')
app.register_blueprint(standard_bp, url_prefix='/standard')
app.register_blueprint(Extreme_bp, url_prefix='/Extreme')


@app.route("/")
def hub():
    """アプリ選択画面（ハブページ）を表示します"""
    return render_template("hub.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)