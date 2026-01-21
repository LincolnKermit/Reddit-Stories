from reddit_scraper import *
from reddit_story import *
from audio_editor import *
from video_editor import *
from subtitles import VideoManager, SubtitleGenerator
import os, uuid, time


# REQUIREMENTS : Python 3.9.0 to <3.12.0
# Make sure sox is installed : brew install sox

dev_mode=False

# main file to orchestrate the process !


def setup():
    if os.system("sox --version") != 0:
        print("SoX is not installed. Installing...")
        if os.system("brew install sox") != 0:
            print("Failed to install SoX. Please install it manually.")
        else:
            print("SoX installed successfully.")
    print("Setup done.")
    exit(0)


audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/audio"))
ding_path = os.path.join(audio_dir, "ding.wav")

temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../temp"))
os.makedirs(temp_dir, exist_ok=True)  # create folder if not exists
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
os.makedirs(output_dir, exist_ok=True)


def run(dev_mode=dev_mode, theme="confession"):
    # delete also temp files from previous runs
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    # Clean up leftover files from previous runs
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Recursively find and delete all output.srt and temp.mp3 files
    for root, dirs, files in os.walk(repo_root):
        for file in files:
            if file in ["output.srt", "temp.mp3"]:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Cleaned up old {file} from {root}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
    
    for item in pick(theme):  # pick stories
        timewatch_start = time.time()
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
        print("Creating video...")
        video_path = create_video(uuid_process)
        
        # Generate and attach subtitles
        print("Generating subtitles...")
        videomanager = VideoManager(video_path, youtube=False)
        subtitle_generator = SubtitleGenerator(videomanager)
        subtitle_generator.attach()
        print("Subtitles attached successfully")
        
        # Clean up temporary files after processing
        cleanup_files = ["output.srt", "temp.mp3"]
        for filename in cleanup_files:
            file_path = os.path.join(repo_root, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Cleaned up {filename}")
                except Exception as e:
                    print(f"Failed to delete {filename}: {e}")
        
        # Clean up temp directory files for this story
        temp_files = [raw_title, raw_text, sped_title, sped_text, final_audio, with_ding]
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"Cleaned up {os.path.basename(temp_file)}")
                except Exception as e:
                    print(f"Failed to delete {temp_file}: {e}")
        
        print("End - Time elapsed:", time.time() - timewatch_start)

print("Starting... \nDev mode:", dev_mode)
run(dev_mode=dev_mode, theme="confession")