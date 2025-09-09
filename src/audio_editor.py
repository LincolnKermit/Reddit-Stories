from TTS.api import TTS
import time, subprocess
from pydub import AudioSegment


##########################################

# 1.3x is a good speed for final ( except audio effects ), do not change

##########################################


def speed_up_wav(input_path, output_path, speed=1.3):
    # since i couldn't find a python library to do this without changing pitch, using sox command line tool
    """
    Speeds up a WAV file without changing pitch using SoX.
    """
    # Build SoX command
    # 'tempo -s' preserves pitch while changing speed
    cmd = [
        "sox", input_path, output_path,
        "tempo", "-s", str(speed)
    ]
    
    # Run command
    subprocess.run(cmd, check=True)


# male model to test: tts_models/en/multi-dataset/tortoise-v2

def generate_tts(text, output_path):
    start_time = time.time()
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=text, file_path=output_path, speed=1.4)
    print(f"TTS audio saved to {output_path} in {round(time.time() - start_time, 2)} seconds")
    return output_path


def combine_audio(input_path_1, input_path_2, output_path):
    sound1 = AudioSegment.from_file(input_path_1)
    sound2 = AudioSegment.from_file(input_path_2)
    combined = sound1 + sound2
    combined.export(output_path, format="wav")


