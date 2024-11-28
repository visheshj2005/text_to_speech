from flask import Flask, request, send_file, jsonify, render_template
from google.cloud import texttospeech
import os
import io

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\\My Drive\\Programming Backup\\Python tutorials course\\Python Projects\\Text to Speech Google API\\text-to-speech-419013-d6505f83ff18.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
@app.route('/synthesize', methods=['POST'])
@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text')
    language_code = data.get('languageCode')
    voice_name = data.get('voiceName')

    if not text or not language_code or not voice_name:
        return jsonify({'error': 'Invalid input, missing text, language code, or voice name'}), 400

    try:
        client = texttospeech.TextToSpeechClient()

        print(f"Received text: {text}, Language Code: {language_code}, Voice Name: {voice_name}")

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return send_file(
            io.BytesIO(response.audio_content),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='output.mp3'  
        )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
