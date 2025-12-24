import os
import speech_recognition as sr
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import uuid
# En la parte superior de app.py
from ai_prompts import ai_query
from ai_time import time_prompt
from datetime import datetime
import time


app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyDNVowMdpOtcnSIgRHQPhqx6nC1sFsESF0"))

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
# 




}

available_models = genai.list_models()
flash_models = [model.name for model in available_models]
print("Available Flash Models:")
for model_name in flash_models:
    print(model_name)
    
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

def get_current_datetime():
    """
    Returns the current date and time in a human-readable format.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    current_datetime = get_current_datetime()
    return render_template('index.html', current_datetime=current_datetime)

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query', '')
    
    try:
        # Generate response using Gemini
        query = ai_query + user_query + time_prompt
        print(f"Received query: {query}")

        try:
            # Attempt to generate content
            response = model.generate_content(query)
            
            # Debug print the entire response object
            print(f"Full response object type: {type(response)}")
            print(f"Response dir(): {dir(response)}")

            # Check if response has text attribute
            if hasattr(response, 'text'):
                print(f"Received response text: {response.text}")
            else:
                print("Response does not have 'text' attribute")
                print(f"Response attributes: {vars(response) if hasattr(response, '__dict__') else 'No vars available'}")

            # Validate response
            if not response or not hasattr(response, 'text') or not response.text:
                return jsonify({
                    'error': 'No se generó respuesta válida',
                    'details': 'La IA no pudo procesar la consulta'
                }), 500

            # Text to Speech
            tts = gTTS(text=response.text, lang='es')
            audio_filename = f'static/audio_{uuid.uuid4()}.mp3'
            tts.save(audio_filename)
            
            return jsonify({
                'text': response.text,
                'audio_path': audio_filename
            })

        except Exception as generation_error:
            print(f"Error generating content: {generation_error}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Error al generar contenido',
                'details': str(generation_error)
            }), 500

    except Exception as e:
        print(f"Unexpected error in query route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e)
        }), 500

def listen_for_keyword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando... Di 'Rosi' para activar el asistente.")
        recognizer.adjust_for_ambient_noise(source)
        
        while True:  # Escucha continuamente
            try:
                print("Escuchando...")
                audio = recognizer.listen(source, timeout=5)  # Escucha por 5 segundos
                
                # Transcribe directly without saving audio file
                query = recognizer.recognize_google(audio, language="es-ES").lower()
                print(f"Has dicho: {query}")

                # Verificar si la palabra clave 'rosi' está presente
                if 'rosi' in query:
                    print("¡Palabra clave 'Rosi' detectada! Activando asistente...")
                    # Llamar a la función para procesar la consulta
                    return process_query(query)

            except sr.UnknownValueError:
                print("No se entendió lo que dijiste. Intenta de nuevo.")
            except sr.RequestError:
                print("No hay conexión con el servicio de Google. Intenta más tarde.")
            time.sleep(0.5)  # Pausa breve para evitar sobrecargar el CPU

def process_query(query):
    # Aquí va el código que ejecuta la lógica de la consulta con la respuesta
    print(f"Procesando la consulta: {query}")
    # Llama a tu código para responder la consulta
    return jsonify({'message': 'Consulta procesada correctamente'})

@app.route('/voice-query', methods=['GET'])
def voice_query():
    listen_for_keyword()
    return jsonify({'message': 'Esperando palabra clave...'})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                               'logo.png', mimetype='image/png')

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 5000))  # Default to port 5000
        app.run(host='0.0.0.0', debug=True, port=port)
    except Exception as e:
        print(f"Error starting the server: {e}")
