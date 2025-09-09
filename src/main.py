from reddit_scraper import *
from reddit_story import *
from audio_editor import *
from video_editor import *
import os, uuid

# main file to orchestrate the process !

audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/audio"))
ding_path = os.path.join(audio_dir, "ding.mp3")

temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../temp"))
os.makedirs(temp_dir, exist_ok=True)  # create folder if not exists
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
os.makedirs(output_dir, exist_ok=True)

for item in pick("relationship_advice"):  # pick stories
    text = scrap(item["url"])
    uuid_process = uuid.uuid4()
    raw_title = os.path.join(temp_dir, f"{uuid_process}_title_raw.wav")
    raw_text = os.path.join(temp_dir, f"{uuid_process}_raw.wav")
    sped_title = os.path.join(temp_dir, f"{uuid_process}_title.wav")
    sped_text = os.path.join(temp_dir, f"{uuid_process}.wav")
    final_audio = os.path.join(temp_dir, f"{uuid_process}_final.wav")
    print(f"Processing {item['title']}...")
    generate_tts(item["title"], raw_title)
    generate_tts(text, raw_text)
    speed_up_wav(raw_title, sped_title)
    speed_up_wav(raw_text, sped_text)
    with_ding = os.path.join(temp_dir, f"{uuid_process}_withding.wav")
    print("sped_title:", sped_title)
    print("ding_path:", ding_path)
    print("with_ding:", with_ding)
    print("sped_text:", sped_text)
    print("final_audio:", final_audio)
    combine_audio(sped_title, ding_path, with_ding)
    combine_audio(with_ding, sped_text, final_audio)
    create_video(uuid_process)
