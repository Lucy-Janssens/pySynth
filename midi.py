import mido
import threading
import sounddevice as sd
from waves import generate_waveform
import numpy as np
import time

SAMPLE_RATE = 44100
NUM_CHANNELS = 1
BYTES_PRE_SAMPLE = 2

active_notes = {}
selected_waveform = 1
active_notes_lock = threading.Lock()


class AudioThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._kill = threading.Event()

    def run(self):
        super().run()

    def kill(self):
        self._kill.set()

    @property
    def killed(self):
        return self._kill.is_set()



def play_audio_loop(audio, sample_rate, note):
    global active_notes, active_notes_lock

    data_type = 'float32' if audio.dtype == np.float32 else 'int16'
    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype=data_type) as stream:
        index = 0
        while True:
            # Check if the note is still active
            with active_notes_lock:
                if note not in active_notes:
                    break

            # Write the audio data to the stream
            data = audio[index:index + sample_rate]
            if len(data) == 0:
                index = 0
                continue
            stream.write(data)
            index += sample_rate


def change_waveform(new_waveform):
    global selected_waveform
    selected_waveform = new_waveform


def process_midi_message(msg):
    global active_notes, selected_waveform

    if msg.type == "note_on":
        print(f"Note on: {msg.note}, Velocity: {msg.velocity}")
        frequency = note_to_frequency(msg.note)
        audio = generate_waveform(frequency, SAMPLE_RATE, selected_waveform)

        # Create and start a new thread to play the audio in a loop
        audio_thread = AudioThread(target=play_audio_loop, args=(audio, SAMPLE_RATE, msg.note))
        audio_thread.start()

        # Store the thread in the active_notes dictionary
        with active_notes_lock:
            active_notes[msg.note] = audio_thread

    elif msg.type == "note_off":
        print(f"Note off: {msg.note}, Velocity: {msg.velocity}")
        with active_notes_lock:
            if msg.note in active_notes:
                # Stop the audio playback for the specific note
                active_notes[msg.note].kill()  # Send a kill signal to the thread
                del active_notes[msg.note]  # Remove the note from the active_notes dictionary

    else:
        print(f"Unhandled message type: {msg.type}")



def note_to_frequency(note):
    return 440 * 2 ** ((note - 69) / 12)


def listen_midi_input():
    input_name = mido.get_input_names()[0]
    print(f"Using MIDI input device: {input_name}")

    with mido.open_input(input_name) as inport:
        for msg in inport:
            process_midi_message(msg)


def start_midi_thread():
    midi_thread = threading.Thread(target=listen_midi_input)
    midi_thread.start()


if __name__ == "__main__":
    start_midi_thread()
