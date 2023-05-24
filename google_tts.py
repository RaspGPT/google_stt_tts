from google.cloud import texttospeech
import requests

import os

request_url = ""
response_path = ""

def tts(data):
    byte_data = data.encode("utf-8")

    response = requests.post(request_url, data=byte_data)

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=response.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code = "ko-KR",
        ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input = synthesis_input,
        voice = voice,
        audio_config = audio_config
    )

    with open(response_path, "wb") as out:
        out.write(response.audio_content)
    
    os.system('aplay '+response_path)