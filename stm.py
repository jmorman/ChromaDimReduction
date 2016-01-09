#http://www.emergentmusics.org/midiutil
from midiutil.MidiFile import MIDIFile

def segments_to_midi(title, pitches, onsets=None, volumes=None, volume_cutoff=15, song_duration=None):
    #TODO fix up duration
    #TODO use shepherd tones to mask octavality, like Ellis dude from labrosa
    #TODO fix clicking arising from notes that span multiple segments being split up
    #Maybe never play more than 4 notes at a time since that's rare in music
    if(onsets == None):
	    onsets = [float(x)/2 for x in range(len(pitches))]
    if(volumes == None):
	    volumes = [-15 for i in range(len(pitches))]
    if(song_duration == None):
	    song_duration = len(pitches)/2
    #Tempo should be 60 since our times come in seconds, not beats

    tempo = 60
    chords = [list(enumerate(chord)) for chord in pitches]

    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    midi.addTrackName(track, time, "Main Track")
    midi.addTempo(track, time, tempo)

    #1 second delay
    for i in range(len(chords)):
        #Conversion inspired by IGWright https://www.sweetwater.com/forums/archive/index.php/t-41785.html
        base_volume = min(1.67 * (volumes[i]+76.3), 127)
        chord_sum = sum([note[1] for note in chords[i]])
        time = 1 + onsets[i]
        duration = 1.2 * song_duration / len(chords)
        for note in chords[i]:
            pitch = 60 + note[0]
            volume = base_volume * note[1] / chord_sum
            if(volume > volume_cutoff):
                volume = (2*volume+127)/3 #Boost volume of significant notes
                midi.addNote(track, channel, pitch, time, duration, volume)
                midi.addNote(track, channel, pitch-12, time, duration, volume+10)
                midi.addNote(track, channel, pitch+12, time, duration, volume+10)


    binfile = open('ChromaMIDIs/' + title +'.mid', 'wb')
    midi.writeFile(binfile)
    binfile.close()

if __name__== '__main__':
	segments_to_midi('testmidi', [[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0,0.1], [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0,0.9], [0.1,0.2,0.3,0.4,0.9,0.6,0.7,0.8,0.9,0,0.1]])
