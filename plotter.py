import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.animation
import config, helpers


# basic plotting script 
def plot_image(image_data): 
    fig = plt.figure()
    ax=fig.add_subplot(111, label="bg")
    image_height = len(image_data)
    image_width = len(image_data[0])
    fig_size_inches=4
    ax.set_xlim([0, image_width])
    ax.set_ylim([0, image_height])
    fig.set_size_inches(fig_size_inches, fig_size_inches)
    ax.axis("off")
    ax.imshow(image_data, origin = 'lower', cmap='gist_heat', alpha=1)
    return(fig)

# animation; produces movie with intensity plot over of background image as it scans
def visual(image_data):
    plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams['animation.ffmpeg_path'] = '/opt/homebrew/bin/ffmpeg'
    
    axis = range(len(image_data[0]))
    norm_frames = helpers.normalize_frames(image_data)

    plt.ioff()
    fig = plot_image(image_data)
    ax = fig.add_subplot(111, label="data")

    def plot_frame(t, y):
        ax.cla()
        ax.set_title(config.obj)
        ax.axis("off")
        ax.set_xlim([0, len(y)])
        ax.set_ylim([0, 1])
        ax.set_xmargin(0)
        ax.set_ymargin(0)
        
        # white line is the intensity, red is the "scanning" line
        ax.plot(axis, 0.5 * y, color = "w", linewidth=0.5)
        ax.axhline(y = t, color = 'r', linewidth=1)
    
    # call the above plotter with the value from the normalized data  (p_frame)
    def animate(t):
        plot_frame(t/len(norm_frames), norm_frames[t])

    # config.merge_frames will be used to set the audio freq too
    writermp4 = matplotlib.animation.FFMpegWriter(fps=config.merge_frames * 2)     
    anim = matplotlib.animation.FuncAnimation(fig, animate, len(norm_frames))
    #plt.show()
    print("saving video")
    anim.save(config.location+"results/"+config.obj+".mp4", writer=writermp4, dpi=150)
    del fig