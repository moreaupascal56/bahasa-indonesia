import logging
import os

import google.cloud.texttospeech as tts


def text_to_wav(text: str, filename: str, voice_name: str = "id-ID-Standard-A"):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    # create dirs in path if not exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb+") as out:
        out.write(response.audio_content)
        logging.info(f'Generated speech saved to "{filename}"')


def parse_text(filepath):
    f = open(filepath, "r")
    return f.read().splitlines()


def generate_audio_files(
    pelajaran_directory="/home/pascal/Documents/github/bahasa_indonesia/pelajaran",
    audio_directory="/home/pascal/Documents/github/bahasa_indonesia/audio",
    overwrite_all=False,
):

    for pelajaran in os.listdir(pelajaran_directory):
        logging.debug(pelajaran)
        pelajaran_path = os.path.join(pelajaran_directory, pelajaran)
        for file in os.listdir(pelajaran_path):
            file_path = os.path.join(pelajaran_path, file)
            if (
                os.path.exists(os.path.join(audio_directory, f"{pelajaran}/{file}"))
                and not overwrite_all
            ):
                continue
            else:
                i = 1  # initialize incremental var to name the audio files
                for line in parse_text(file_path):
                    text_to_wav(
                        text=line,
                        filename=os.path.join(
                            audio_directory, f"{pelajaran}/{file}/{i}.wav"
                        ),
                    )
                    i += 1


generate_audio_files()
