from flask import Blueprint,request,render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()

Extreme_bp = Blueprint(
    'Extreme', 
    __name__,
    template_folder='templates/Extreme',
    static_folder='static/Extreme'
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("環境変数 'GEMINI_API_KEY' が設定されていません。")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@Extreme_bp.route("/")
def show_input_page():
    return render_template("Extreme/input.html")

@Extreme_bp.route("/result",methods=["POST"])
def show_result_page():
    user_input = request.form.get('goal_text')
    difficulty = request.form.get('difficulty')
    if difficulty == "extreme":
        difficulty_instruction = "極限の難易度。達成することはかなり難しいが、達成した場合圧倒的な成長を感じられるレベル"
        difficulty_tag = "Extreme"
        task_count_instruction = "提案は必ず1つだけにすること。"
    else:
        difficulty_instruction = "難しい難易度。達成感のある挑戦的なレベル"
        difficulty_tag = "Hard"
        task_count_instruction = "提案は必ず3つにすること。"
    try:
        prompt = f"""
        # 指示
        クライアントの目標は「{user_input}」です。
        この目標を達成するための、「{difficulty_instruction}」という条件に合う、ユニークで面白いタスクを提供してください。
        # ルール
        - {task_count_instruction}
        - 短く簡潔な一行の文章にすること。
        - 提案の最後に、指定された難易度タグ「({difficulty_tag})」を必ず付けること。
        - 各タスクは、必ず新しい行から始め、行頭にアスタリスク(*)を1つだけ付けること。
        - 余計な挨拶や説明は一切不要です。タスクだけを出力してください。
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
        print(f"AIの呼び出し中にエラーが発生しました: {e}")
        todo_list = ["エラーが発生しました。時間をおいて再度お試しください。"]
    return render_template("Extreme/output.html", todo_list=todo_list, difficulty=difficulty)


@Extreme_bp.route("/reject", methods=["POST"])
def reject_task():
    try:
        prompt = """
        ユーザーがタスクを拒否しました。
        「やる気がないのか？」「その程度で目標を達成できるとでも思ったか？」
        といったニュアンスで、ユーザーを強く叱咤するような、短く威圧的な一言を生成してください。
        挨拶や前置きは一切不要です。
        """
        response = model.generate_content(prompt)
        message = response.text.strip()
    except Exception as e:
        print(f"AIの呼び出し中にエラーが発生しました: {e}")
        message = "エラーが発生しました。時間をおいて再度お試しください。"
    return render_template("reject.html", message=message)