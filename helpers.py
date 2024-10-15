from moviepy.editor import *
import config

def normalize_frames(image_data):
    max_intensity = max(map(max, image_data))
    min_intensity = min(map(min, image_data))
    d_intensity = max_intensity - min_intensity
    norm_frames = (image_data - min_intensity) / d_intensity
    return norm_frames

def combine():
    videoclip = VideoFileClip(config.location+"results/"+config.obj+".mp4")
    audioclip = AudioFileClip(config.location+"results/"+config.obj+".wav")

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(config.location+"results/"+config.obj+"Final.mp4")


def combine():
    videoclip = VideoFileClip(config.location+"results/"+config.obj+".mp4")
    audioclip = AudioFileClip(config.location+"results/"+config.obj+".wav")

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile(config.location+"results/"+config.obj+"Final.mp4")