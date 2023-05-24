import io
import os

from google.cloud import speech

credential_path = ""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def stt():
    client = speech.SpeechClient()

    wav_path = ""

    with io.open(wav_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000,
        language_code = "ko-KR",
        audio_channel_count = 1
    )

    response = client.recognize(config=config, audio=audio)

    stt_result = ""

    for result in response.results:
        stt_result += result.alternatives[0].transcript

    return stt_result