import openai
import gradio as gr

# Importamos los módulos que implementamos
from config import settings
from core import conversation, openai_client
from utils import exporter

# Leer la API key desde el archivo y configurarla
with open("openai_api_key.txt", "r") as f:
    api_key = f.read().strip()
openai.api_key = api_key

# Función que se encarga de procesar el mensaje del usuario y llamar al cliente de OpenAI
def generate_response(user_input, model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    # Agregamos el mensaje del usuario al historial
    conversation.add_message("user", user_input)
    
    # Llamamos a la función que gestiona la llamada a la API usando el historial actual
    reply = openai_client.call_openai(
        model, temperature, max_tokens, top_p, frequency_penalty, presence_penalty
    )
    
    # Agregamos la respuesta del asistente al historial
    conversation.add_message("assistant", reply)
    return reply

# Función para exportar el historial de conversación en texto
def export_conversation_text():
    return exporter.export_as_text()

def main():
    # Configuramos la interfaz con Gradio
    with gr.Blocks() as demo:
        gr.Markdown("# 🤖 Chat con OpenAI")
        
        # Fila para elegir el modelo
        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=settings.AVAILABLE_MODELS,
                value=settings.AVAILABLE_MODELS[0],
                label="Selecciona el modelo"
            )
        
        # Fila para ajustar los parámetros del modelo
        with gr.Row():
            temperature_slider = gr.Slider(
                0.0, 1.0, value=settings.DEFAULT_PARAMS["temperature"],
                step=0.1, label="Temperatura"
            )
            max_tokens_slider = gr.Slider(
                16, 2048, value=settings.DEFAULT_PARAMS["max_tokens"],
                step=16, label="Máx Tokens"
            )
            top_p_slider = gr.Slider(
                0.0, 1.0, value=settings.DEFAULT_PARAMS["top_p"],
                step=0.1, label="Top P"
            )
            frequency_penalty_slider = gr.Slider(
                0.0, 2.0, value=settings.DEFAULT_PARAMS["frequency_penalty"],
                step=0.1, label="Penalización por Frecuencia"
            )
            presence_penalty_slider = gr.Slider(
                0.0, 2.0, value=settings.DEFAULT_PARAMS["presence_penalty"],
                step=0.1, label="Penalización por Presencia"
            )

        # Chatbot y caja de texto para ingresar mensajes
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(placeholder="Escribe tu mensaje aquí...", label="Tu mensaje")

        # Botones de acción
        with gr.Row():
            send_button = gr.Button("Enviar")
            reset_button = gr.Button("Resetear Conversación")
            export_button = gr.Button("Exportar Conversación")
        
        # Caja de salida para mostrar el historial exportado
        output_export = gr.Textbox(label="Historial de Conversación", interactive=False)

        # Función para enviar un mensaje y actualizar el chat
        def send_message(message, chat_history):
            reply = generate_response(
                message,
                model_dropdown.value,
                temperature_slider.value,
                max_tokens_slider.value,
                top_p_slider.value,
                frequency_penalty_slider.value,
                presence_penalty_slider.value
            )
            # Agregamos el mensaje del usuario y la respuesta al historial visual
            chat_history.append(("Usuario", message))
            chat_history.append(("Asistente", reply))
            return "", chat_history

        send_button.click(
            fn=send_message,
            inputs=[user_input, chatbot],
            outputs=[user_input, chatbot]
        )
        
        # Función para resetear el historial de conversación
        def reset_history():
            conversation.reset_history()
            return []

        reset_button.click(
            fn=reset_history,
            inputs=None,
            outputs=chatbot
        )
        
        # Botón para exportar el historial
        export_button.click(
            fn=export_conversation_text,
            inputs=None,
            outputs=output_export
        )
    
    demo.launch(share=True)

if __name__ == "__main__":
    main()