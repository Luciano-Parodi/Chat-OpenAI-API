from core.conversation import get_history
import json

def export_as_text():
    output = ""
    for msg in get_history():
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        output += f"{role}: {msg['content']}\n"
    return output

def export_as_json(filename="historial.json"):
    with open(filename, "w") as f:
        json.dump(get_history(), f, indent=4)