from IPython.display import Audio
import math
import numpy as np
import config, helpers 

chunk_size = 20000
sample_rate = 2 * chunk_size

def clean(frame):
    f = np.copy(frame)
    # f[1:-1] = (f[1:-1] + f[:-2] + f[2:]) / 3
    f[2:-2] = (f[:-4] + f[1:-3] + f[2:-2] + f[3:-1] + f[4:]) / 5
    for i in range(len(f)):
        if (f[i]) < 0.3:
            f[i] = 0
    return f * f * f * f

def downscale(frame):
    new_frame = np.zeros(math.floor(len(frame) / 2))
    for i in range(len(new_frame)):
        new_frame[i] = (frame[2 * i] + frame[2 * i + 1]) / 2
    return new_frame

def generate_frame(frame):
    frame = clean(frame)
    target_domain_size = 400
    input_domain_size = len(frame)
    target_domain = np.arange(0, input_domain_size, input_domain_size / target_domain_size)
    input_domain = np.arange(input_domain_size)
    input = frame
    frame = np.interp(target_domain, input_domain, input)

    frequency_range = np.zeros(math.floor(chunk_size / 2))
    for i in range(len(frame)):
        frequency_range[i] = frame[i]

    re_fourier = np.concatenate(([frequency_range[0]], frequency_range[1:] / 2, np.flip(np.conjugate(frequency_range[1:]))/2))
    signal = np.fft.ifft(re_fourier)

    signal_2 = np.copy(signal)
    sl = len(signal_2)
    for i in range(sl):
        signal_2[i] *= math.sin(i * np.pi / sl)

    return signal_2

def get_frame(i,norm_frames):
    sum = norm_frames[config.merge_frames * i]
    for j in range(config.merge_frames-1):
        sum += norm_frames[i * config.merge_frames + j]
    return sum / config.merge_frames

def fourier_sonifier(image_data): 
    axis = range(len(image_data[0]))
    
    norm_frames = helpers.normalize_frames(image_data)

    fl = len(norm_frames[0])
    hfl = math.floor(fl / 2)
    cl = chunk_size
    hcl = math.floor(chunk_size / 2)
    signal = generate_frame(get_frame(0, norm_frames))

    for raw_i in range(math.floor(len(norm_frames) / config.merge_frames) - 1):
        i = raw_i

        new_signal = generate_frame(get_frame(i+1, norm_frames))
        signal = np.concatenate((signal, new_signal))

        stitch_frame = np.concatenate((get_frame(i,norm_frames)[hfl:],get_frame(i+1,norm_frames)[:hfl+1]))
        stitch_signal = generate_frame(stitch_frame)
        stitch_start_index = raw_i * cl + hcl
        for j in range(len(stitch_signal)):
            signal[stitch_start_index + j] = (signal[stitch_start_index + j] + stitch_signal[j])
    
    audio = Audio(signal, rate=sample_rate)
    print("Saving audio")
    with open(config.location+"results/"+config.obj+".wav", 'wb') as f:
        f.write(audio.data)
    #plotter.plot_image(signal)

