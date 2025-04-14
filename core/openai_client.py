import openai
from core.conversation import get_history

def call_openai(model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    messages = get_history()
    if model.startswith("gpt"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].message["content"]
    else:
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].text.strip()