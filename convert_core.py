import io
import os
import requests
import pygame
import json

from google.cloud import texttospeech
from google.cloud import speech

with open("./config.json", 'r') as f: conf = json.load(f)

class GoogleConvert:
    def __init__(self):
        self._set_credential()
        self.stt_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        self.language_code = conf.LANGUAGE_CODE
        self.encode_type = conf.ENCODE_TYPE
        self.wav_path = conf.WAV_PATH
        self.mp3_path = conf.MP3_PATH

        self.gpt_server_ip = conf.SERVER_IP
        self.gpt_server_port = ":"+conf.SERVER_PORT
        self.gpt_q_api = conf.GPT_API

    def _set_credential(self):
        credential_path = ""
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    def stt(self):
        with io.open(self.wav_path, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        
        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = conf.SAMPLE_RATE_HERTZ,
            language_code = self.language_code,
            audio_channel_count = conf.AUDIO_CHANNEL_COUNT
        )

        response = self.stt_client.recognize(config=config, audio=audio)

        for result in response.results:
            stt_result += result.alternatives[0].transcript

        return stt_result

    def tts(self, data):
        byte_data = data.encode(self.encode_type)

        request_url = self.gpt_server_ip+self.gpt_server_port+self.gpt_q_api
        response = requests.post(request_url, data=byte_data)

        synthesis_input = texttospeech.SynthesisInput(text=response.text)

        voice = texttospeech.VoiceSelectionParams(
            language_code = self.language_code,
            ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding = texttospeech.AudioEncoding.MP3
        )

        response = self.tts_client.synthesize_speech(
            input = synthesis_input,
            voice = voice,
            audio_config = audio_config
        )

        with open(self.mp3_path, "wb") as f:
            f.write(response.audio_content)
        
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.mp3_path)
            pygame.mixer.music.set_volume(conf.VOLUME)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy(): continue
        except pygame.error as e: print(str(e))