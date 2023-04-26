import mido
from waves import *
import sounddevice as sd
import threading
import time
import keyboard
from thread import AudioThread


SAMPLE_RATE = 44100
NUM_CHANNELS = 1
BYTES_PER_SAMPLE = 2


# Dictionary to store active note streams
active_notes = {}
# Waveform selection
selected_waveform = 4  # Default to sine wave

def play_audio_loop(audio, sample_rate):
    global active_notes
    audio_int16 = (audio * (2**15 - 1)).astype(np.int16)
    while not threading.current_thread().killed:
        with sd.OutputStream(samplerate=sample_rate, channels=NUM_CHANNELS, dtype='int16') as stream:
            stream.write(audio_int16)

def process_midi_message(msg):
    global active_notes, selected_waveform

    if msg.type == "note_on":
        print(f"Note on: {msg.note}, Velocity: {msg.velocity}")
        frequency = note_to_frequency(msg.note)
        audio = generate_waveform(frequency, SAMPLE_RATE, selected_waveform)

        # Create and start a new thread to play the audio in a loop
        audio_thread = AudioThread(target=play_audio_loop, args=(audio, SAMPLE_RATE))
        audio_thread.start()

        # Store the thread in the active_notes dictionary
        active_notes[msg.note] = audio_thread

    elif msg.type == "note_off":
        print(f"Note off: {msg.note}, Velocity: {msg.velocity}")
        if msg.note in active_notes:
            # Stop the audio playback for the specific note
            active_notes[msg.note].kill()  # Send a kill signal to the thread
            del active_notes[msg.note]  # Remove the note from the active_notes dictionary

    else:
        print(f"Unhandled message type: {msg.type}")



def note_to_frequency(note):
    return 440 * 2 ** ((note - 69) / 12)

def listen_midi_input():
    input_name = mido.get_input_names()[0]  # Get the name of the first available MIDI input device
    print(f"Using MIDI input device: {input_name}")

    with mido.open_input(input_name) as inport:
        for msg in inport:
            process_midi_message(msg)

def waveform_listener():
    global selected_waveform
    while True:
        if keyboard.is_pressed('1'):
            print("Selected waveform: 1 (Sine wave)")
            selected_waveform = 1
        elif keyboard.is_pressed('2'):
            print("Selected waveform: 2 (Square wave)")
            selected_waveform = 2
        elif keyboard.is_pressed('3'):
            print("Selected waveform: 3 (Sawtooth wave)")
            selected_waveform = 3
        elif keyboard.is_pressed('4'):
            print("Selected waveform: 4 (Triangle wave)")
            selected_waveform = 4
        # Add more conditions if needed

if __name__ == "__main__":
    waveform_listener_thread = threading.Thread(target=waveform_listener)
    waveform_listener_thread.start()
    listen_midi_input()
