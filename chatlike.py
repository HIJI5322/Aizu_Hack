import os
from flask import Blueprint, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

chat_like_bp = Blueprint(
    'chatlike',
    __name__,
    template_folder='templates/chatlike',
    static_folder='static/chatlike'
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが設定されていません。")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
error = "適切な入力をしてください"

@chat_like_bp.route("/")
def show_page():
    return render_template("chatlike/index.html")

@chat_like_bp.route("/index", methods=["POST"])
def input_route():
    data = request.get_json()
    goal = data.get("goal", "")
    level = data.get("level", "")
    return send_api(goal, level)
        
def send_api(goal, level):
    prompt = f"Goal:{goal} Level:{level} If goal is invalid, output {error}. Otherwise write 3 daily tasks in only Japanese, each ending with *"
    response = model.generate_content(prompt)
    response_text = response.text
    
    sentences = [s.strip() for s in response_text.split("*") if s.strip()]
    while len(sentences) < 3:
        sentences.append("")
    return jsonify({
            "sentence1": sentences[0],
            "sentence2": sentences[1],
            "sentence3": sentences[2]
        })