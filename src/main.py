from reddit_scraper import *
from reddit_story import *
from tts_generator import *
import os, uuid

# main file to orchestrate the process !

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../temp"))
os.makedirs(base_dir, exist_ok=True)  # create folder if not exists

for item in pick("relationship_advice"): # pick stories
    text = scrap(item["url"])
    uuid_process = uuid.uuid4()
    output_path = os.path.join(base_dir, f"{uuid_process}.wav")
    generate_tts(text, output_path)  # generate TTS