import random
from moviepy.editor import VideoFileClip, AudioFileClip
import os

def create_video(uuid_process):
    """
    Combines a static video with generated TTS audio,
    randomly cutting the video to fit the audio length.
    """
    # Paths
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/videos/sample.mp4"))
    audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../temp/{uuid_process}_final.wav"))
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../output/{uuid_process}.mp4"))

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    # Load video and audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    try:
        # Ensure audio fits inside video
        if audio.duration > video.duration:
            raise ValueError("Audio is longer than video, can't fit.")

        # Pick a random start time
        max_start = video.duration - audio.duration
        start_time = random.uniform(0, max_start) if max_start > 0 else 0

        # Cut the video segment
        video_clip = video.subclip(start_time, start_time + audio.duration)

        # Set the audio
        final_clip = video_clip.set_audio(audio)

        # Write the final video
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    finally:
        # Close clips to free resources
        video.close()
        audio.close()
        if 'video_clip' in locals():
            video_clip.close()
        if 'final_clip' in locals():
            final_clip.close()
    return output_path
