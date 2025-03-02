import os
import speech_recognition as sr
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from gtts import gTTS
import uuid
# En la parte superior de app.py
from ai_prompts import get_ai_query
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
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query', '')
    
    try:
        # Generate response using Gemini
    

        query = ai_query + user_query

        response = model.generate_content(query)
        
        # Text to Speech
        tts = gTTS(text=response.text, lang='es')
        audio_filename = f'static/audio_{uuid.uuid4()}.mp3'
        tts.save(audio_filename)
        
        return jsonify({
            'text': response.text,
            'audio_path': audio_filename
        })
    except Exception as e:
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
            time.sleep(1)  # Pausa breve para evitar sobrecargar el CPU

def process_query(query):
    # Aquí va el código que ejecuta la lógica de la consulta con la respuesta
    print(f"Procesando la consulta: {query}")
    # Llama a tu código para responder la consulta
    return jsonify({'message': 'Consulta procesada correctamente'})

@app.route('/voice-query', methods=['GET'])
def voice_query():
    listen_for_keyword()
    return jsonify({'message': 'Esperando palabra clave...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
