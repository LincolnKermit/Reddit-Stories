#!/usr/bin/env python3

import os
import argparse
import platform
import subprocess
import sys
from datetime import timedelta

try:
    import whisper
    import yt_dlp
    from moviepy.editor import *
    from moviepy.video.tools.subtitles import SubtitlesClip
    from moviepy.video.VideoClip import TextClip
except ImportError:
    print("trying to install dependencies")

    def install_libraries():
        required_libraries = ['openai-whisper', 'yt_dlp', 'moviepy']
        
        # Use the same Python interpreter that's running this script
        python_executable = sys.executable
        
        for library in required_libraries:
            try:
                subprocess.check_call([python_executable, '-m', 'pip', 'install', library, '--break-system-packages'])
                print(f"{library} installed successfully")
            except subprocess.CalledProcessError:
                print(f"failed to install {library}")
                sys.exit(1)
        
        print("\nAll dependencies installed. Please run the script again.")
        sys.exit(0)

    install_libraries()

YT_ATTACH = "youtube-a"
YT_GENERATE = "youtube-g"
VALID_MODES = ("attach", "generate", YT_ATTACH, YT_GENERATE)
YT_MODES = (YT_ATTACH, YT_GENERATE)
TEMP_FILE = "temp.mp3"
OUTPUT_SRT = "output.srt"
OUTPUT_VID = "output.mp4"
YT_VID = "yt.mp4"


class VideoManager:
    def __init__(self, path: str, youtube: bool) -> None:
        self.path = path
        self.youtube = youtube
        if not self.youtube:
            self.video = VideoFileClip(path)

        self.extract_audio()

    def download(self) -> None:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": "yt",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as dl:
            dl.download([self.path])

        self.video = VideoFileClip(YT_VID)

    def extract_audio(self) -> None:
        if self.youtube:
            self.download()

        if self.video.audio is not None:
            self.video.audio.write_audiofile("temp.mp3", codec="mp3")
        else:
            print("video has no audio, quitting")


class Utility:
    def __init__(self, path: str, youtube: bool) -> None:
        self.path = path
        self.youtube = youtube

    def file_exists(self) -> bool:
        if self.youtube:
            return True
        return len(self.path) > 0 and os.path.exists(path=self.path)


class SubtitleGenerator:
    def __init__(self, videomanager: VideoManager) -> None:
        self.videomanager = videomanager

    def generate(self) -> None:
        # Credit goes to
        # https://github.com/openai/whisper/discussions/98#discussioncomment-3725983
        # github.com/lectair

        model = whisper.load_model("base")
        transcribe = model.transcribe(audio=TEMP_FILE, fp16=False)
        segments = transcribe["segments"]

        for seg in segments:
            start = str(0) + str(timedelta(seconds=int(seg["start"]))) + ",000"
            end = str(0) + str(timedelta(seconds=int(seg["end"]))) + ",000"
            text = seg["text"]
            segment_id = seg["id"] + 1
            segment = f"{segment_id}\n{start} --> {end}\n{text[1:] if text[0] == ' ' else text}\n\n"
            with open(OUTPUT_SRT, "a", encoding="utf-8") as f:
                f.write(segment)

        print("subtitles generated")

    def attach(self) -> None:
        self.generate()
        if os.path.exists(OUTPUT_SRT):
            # Use ffmpeg to burn subtitles into the video
            # Get absolute paths
            srt_path = os.path.abspath(OUTPUT_SRT)
            input_video = self.videomanager.path
            
            # Create output path - replace original video
            output_dir = os.path.dirname(input_video)
            uuid_name = os.path.basename(input_video)
            temp_output = os.path.join(output_dir, f"temp_sub_{uuid_name}")
            
            # Escape the SRT path for ffmpeg subtitles filter
            srt_path_escaped = srt_path.replace('\\', '/').replace(':', '\\:')
            
            cmd = [
                'ffmpeg',
                '-i', input_video,
                '-vf', f"subtitles='{srt_path_escaped}'",
                '-c:v', 'libx264',
                '-c:a', 'copy',
                '-y',
                temp_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Replace original video with subtitled version
                os.replace(temp_output, input_video)
                print(f"Subtitles added to {input_video}")
            else:
                print(f"Error adding subtitles: {result.stderr}")
                if os.path.exists(temp_output):
                    os.remove(temp_output)

def check_ffmpeg() -> bool:
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0 and 'ffmpeg' in result.stdout
    except FileNotFoundError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="auto caption generator v1.0")
    parser.add_argument(
        "mode", metavar="mode", type=str, help="operation mode (attach|generate)"
    )
    parser.add_argument("path", metavar="path", type=str, help="filepath of the video")
    args = parser.parse_args()
    mode = args.mode
    path = args.path

    if not check_ffmpeg():
        print("ffmpeg must be installed to run this script, quitting")
        exit()

    if len(mode) > 0 and len(path) > 0:
        yt_mode = True if mode in YT_MODES else False
        utility = Utility(path, yt_mode)

        if mode in VALID_MODES and utility.file_exists():
            videomanager = VideoManager(utility.path, yt_mode)
            subtitle_generator = SubtitleGenerator(videomanager)

            if mode == VALID_MODES[0] or mode == VALID_MODES[2]:
                subtitle_generator.attach()
            elif mode == VALID_MODES[1] or mode == VALID_MODES[3]:
                subtitle_generator.generate()
        else:
            print("invalid mode or file path, quitting")


if __name__ == "__main__":
    main()