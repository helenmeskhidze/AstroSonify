from midiutil import MIDIFile
import config
import numpy as np
from midi2audio import FluidSynth
import fluidsynth

def midify_image(image_data): 
    MyMIDI = MIDIFile(1, file_format=1)
    track = 0 # Track numbers are zero-origined
    channel = 0 # MIDI channel number
    pitch = 60 # MIDI note number (0 to 127) 
    time = 0 # In beats
    duration = 1 # In beats
    volume = 100 # 0-127, 127 being full volume
    program = 42 # A Cello
    MyMIDI.addProgramChange(track, channel, time, program)

    i = 0
    while i < len(image_data) - config.merge_frames: 
        time += duration
        tmp = []
        # store the average of each slice in tmp
        for j in range(config.merge_frames):
            tmp.append(np.average(image_data[i+j]))
        # average all slice averages for chunk of height merge_frames
        pitch = int(np.average(tmp)*127)
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        i+=config.merge_frames

    with open(config.location+"results/"+config.obj+".midi", 'wb') as output_file:
        print("saved",output_file)
        MyMIDI.writeFile(output_file)


    fs = FluidSynth(sound_font="default.sf2")
    fs.midi_to_audio(config.location+"results/"+config.obj+".midi", config.location+"results/"+config.obj+".wav") 
