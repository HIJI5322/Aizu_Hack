import os
from flask import Blueprint, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが設定されていません。環境変数 'GEMINI_API_KEY' を設定してください。")

genai.configure(api_key=api_key)

AIsupport_bp = Blueprint(
    'AIsupport',
    __name__,
    template_folder='templates/AIsupport'
)

@AIsupport_bp.route('/', methods=['GET', 'POST'])
def index():
    suggestion = None
    goal = ""
    if request.method == 'POST':
        goal = request.form['goal']
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"「{goal}」という目標を達成するための、今日すぐに実行できる具体的なタスクを一つだけ、簡潔に命令形で提案してください。例えば「腕立て伏せを10回する」のように答えてください。"
            response = model.generate_content(prompt)
            suggestion = response.text
        except Exception as e:
            suggestion = f"AIとの通信中にエラーが発生しました: {e}"
    return render_template('AIsupport/index.html', goal=goal, suggestion=suggestion)