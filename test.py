import requests

API_KEY = "pat_tDtMgcGNgETjlQtuQIDpP1UTlSX4P8f6whCSPpIUTxEr75xsTXDsPX34Q96TgynP"
BOT_ID = "7611854049474297906"


def test_coze_api():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 简单消息测试
    payload = {
        "bot_id": BOT_ID,
        "user_id": "test_user_123",
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [{
            "role": "user",
            "content": "Hello",
            "content_type": "text"
        }]
    }

    print("🚀 发送测试请求...")
    response = requests.post("https://api.coze.cn/v3/chat",
                             headers=headers, json=payload, timeout=30)

    result = response.json()
    print("📦 响应结果:", result)

    # 检查响应类型
    if result.get("code") == 0:
        data = result.get("data", {})
        if "messages" in data:
            print("✅ 同步响应成功")
            for msg in data["messages"]:
                if msg.get("role") == "assistant":
                    print(f"🤖 助手回复: {msg.get('content')}")
        elif "conversation_id" in data:
            print(f"⚠️ 异步响应 - conversation_id: {data['conversation_id']}")
            print(f"⚠️ 状态: {data.get('status', 'unknown')}")
            return False  # 需要轮询但可能不可用
    else:
        print(f"❌ API错误: {result.get('msg')}")

    return True


if __name__ == "__main__":
    test_coze_api()
