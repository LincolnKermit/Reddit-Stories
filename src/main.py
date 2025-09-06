from reddit_scraper import *
from reddit_story import *
from audio_editor import *
from video_editor import *
import os, uuid

# main file to orchestrate the process !

temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../temp"))
os.makedirs(temp_dir, exist_ok=True)  # create folder if not exists
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
os.makedirs(output_dir, exist_ok=True)

for item in pick("relationship_advice"): # pick stories
    text = scrap(item["url"])
    uuid_process = uuid.uuid4()
    tts_path = os.path.join(temp_dir, f"{uuid_process}_raw.wav")
    generate_tts(text, tts_path)
    sped_path = os.path.join(temp_dir, f"{uuid_process}.wav")
    speed_up_wav(tts_path, sped_path)
    create_video(uuid_process)