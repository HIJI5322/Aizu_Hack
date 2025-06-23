from flask import Blueprint,request,render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()

standard_bp = Blueprint(
    'standard',
    __name__,
    template_folder='templates/standard',
    static_folder='static/standard'
)

#AIモデルのセットアップ
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("環境変数 'GEMINI_API_KEY' が設定されていません。")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@standard_bp.route("/",methods=["GET"])
def show_input_page():
    return render_template("standard/Input.html")

@standard_bp.route("/result",methods=["POST"])
def show_result_page():
    user_input = request.form.get('goal_text')
    difficulty = request.form.get('difficulty')

    if difficulty == "easy":
        difficulty_instruction = "簡単な難易度"
    elif difficulty == "hard":
        difficulty_instruction = "難しい難易度"
    else: 
        difficulty_instruction = "普通の難易度"
    try:
        prompt = f"""
        # 指示
        クライアントの目標は「{user_input}」です。
        この目標を達成するための、「{difficulty_instruction}」という条件に合うような、楽しいタスクを３つ提供して。
        # ルール
        - 提案は必ず3つにすること。
        - 短く簡潔な一行の文章にすること。
        - 提案の最後には難易度を書いて。
        - 各ライフハックは、必ず新しい行から始め、行頭にアスタリスク(*)を1つだけ付けること。
        - 余計な挨拶や説明は一切不要です。3つのライフハックだけを出力してください。
        """
        response = model.generate_content(prompt)
        ai_text = response.text
        todo_list = []
        lines = ai_text.strip().split('\n')
        for line in lines:
            if re.match(r'^\s*[\*\-]\s*|\d+\.\s*', line):
                perfect_text = re.sub(r'^\s*[\*\-]\s*|\d+\.\s*', '', line).strip()
                todo_list.append(perfect_text)
        if not todo_list:
            todo_list = [ai_text]
    except Exception as e:
        print(f"AIの呼び出し中にエラーが発生しましたぜBaby: {e}")
        todo_list = ["申し訳ありません、AIとの通信中にエラーが発生しました。"]
    return render_template("Output.html",todo_list=todo_list)