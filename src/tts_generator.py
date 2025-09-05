from TTS.api import TTS
import time


def generate_tts(text, output_path):
    start_time = time.time()
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=text, file_path=output_path)
    print(f"TTS audio saved to {output_path} in {round(time.time() - start_time, 2)} seconds")
    return output_path