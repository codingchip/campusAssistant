import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# ====== 配置 ======
BOT_ID = os.environ.get("BOT_ID","")
API_TOKEN = os.environ.get("API_TOKEN","")
BASE_URL = "https://api.coze.cn/v3"

# ====== 发送聊天请求 ======
def send_chat_request(question, user_id):
    url = f"{BASE_URL}/chat"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "bot_id": BOT_ID,
        "user_id": user_id,
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": question,
                "content_type": "text"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("🔥 chat响应：", result)

    return result


# ====== 获取聊天结果 ======
def get_chat_messages(chat_id, conversation_id):
    url = f"{BASE_URL}/chat/message/list?chat_id={chat_id}&conversation_id={conversation_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    print("⏳ 查询消息：", result)

    return result


# ====== 核心函数 ======
def send_to_coze(question, user_id):

    chat_response = send_chat_request(question, user_id)

    # ✅ 基本校验
    if chat_response.get("code") != 0 or "data" not in chat_response:
        return "❌ 创建对话失败：" + str(chat_response)

    chat_id = chat_response["data"].get("id")
    conversation_id = chat_response["data"].get("conversation_id")

    if not chat_id or not conversation_id:
        return "❌ 未获取到 chat_id 或 conversation_id"

    # ✅ 轮询获取结果
    for attempt in range(30):
        time.sleep(2)

        messages = get_chat_messages(chat_id, conversation_id)

        # 防御
        if messages.get("code") != 0 or "data" not in messages:
            print("❌ 获取失败，重试中...")
            continue

        for msg in messages["data"]:
            if msg.get("role") == "assistant" and msg.get("type") == "answer":
                return msg.get("content", "（无内容）")

        print(f"⚠️ 第{attempt+1}次未获取到答案，继续重试...")

    return "❌ 超时未获取到AI回复"


# ====== 接口 ======
@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "")
    user_id = data.get("user_id", "default_user")

    if not question:
        return jsonify({"answer": "❌ 问题不能为空"})

    answer = send_to_coze(question, user_id)

    return jsonify({"answer": answer})


# ====== 启动 ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)