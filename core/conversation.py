conversation_history = []

def add_message(role, content):
    conversation_history.append({"role": role, "content": content})

def get_history():
    return conversation_history

def reset_history():
    conversation_history.clear()