# This is a simple program to try and develop a simple Synthesizer and midi interface

from midi import *
from midi import _thread_init

if __name__ == "__main__":
    waveform_listener_thread = threading.Thread(target=waveform_listener)
    waveform_listener_thread.start()
    listen_midi_input()