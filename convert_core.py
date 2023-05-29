import io
import os
import requests
import pygame

from google.cloud import texttospeech
from google.cloud import speech

class GoogleConvert:
    def __init__(self):
        self._set_credential()
        self.stt_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        self.language_code = "ko-KR"
        self.encode_type = "utf-8"
        self.wav_path = "output.wav"
        self.mp3_path = "output.mp3"

        self.gpt_server_ip = ""
        self.gpt_server_port = ":8080"
        self.gpt_q_api = "/gpt"

    def _set_credential(self):
        credential_path = ""
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    def stt(self):
        with io.open(self.wav_path, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        
        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = 16000,
            language_code = self.language_code,
            audio_channel_count = 1
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
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy(): continue
        except pygame.error as e: print(str(e))