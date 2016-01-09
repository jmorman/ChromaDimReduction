import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def display_chroma(pitches, length=30, strictness=0.5):
    pitchmod = np.array(pitches).T
    
    plt.close()

    fig, ax = plt.subplots(figsize=(20,6), facecolor='white', edgecolor='white')

    map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])

    colors = LinearSegmentedColormap.from_list('greyscale', 
                                               colors=[(0,'#ffffff'), (strictness, '#ffffff'),
                                                       (1,'#000000')], gamma=.2)
    
    ax.get_yaxis().set_ticks(range(12))   
    ax.set_yticklabels(['B ', 'A#', 'A ', 'G#', 'G ', 'F#', 'F ', 'E ', 'D#', 'D ', 'C#', 'C '])

    #Reverse note order so notes are ascending in plot
    plt.imshow(pitchmod[::-1, :length], interpolation='nearest', cmap=colors)
