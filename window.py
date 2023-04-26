import tkinter as tk
from midi import *


# Callback functions for buttons
def on_sine_wave_button_click():
    change_waveform(1)


def on_square_wave_button_click():
    change_waveform(2)


def on_triangle_wave_button_click():
    change_waveform(3)


def on_sawtooth_wave_button_click():
    change_waveform(4)


# Create the main window
def start_window():
    root = tk.Tk()
    root.title("Waveform Synthesizer")

    # Create buttons for each waveform
    sine_wave_button = tk.Button(root, text="Sine Wave", command=on_sine_wave_button_click)
    square_wave_button = tk.Button(root, text="Square Wave", command=on_square_wave_button_click)
    triangle_wave_button = tk.Button(root, text="Triangle Wave", command=on_triangle_wave_button_click)
    sawtooth_wave_button = tk.Button(root, text="Sawtooth Wave", command=on_sawtooth_wave_button_click)

    # Add buttons to the window
    sine_wave_button.pack()
    square_wave_button.pack()
    triangle_wave_button.pack()
    sawtooth_wave_button.pack()

    # Start the main event loop
    start_midi_thread()
    root.mainloop()
