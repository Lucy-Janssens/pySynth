import mido

def process_midi_message(msg):
    if msg.type == "note_on":
        print(f"Note on: {msg.note}, Velocity: {msg.velocity}")
        # Add code here to play a sound based on the received MIDI note
    elif msg.type == "note_off":
        print(f"Note off: {msg.note}, Velocity: {msg.velocity}")
        # Add code here to stop playing the sound based on the received MIDI note
    else:
        print(f"Unhandled message type: {msg.type}")

def listen_midi_input():
    input_name = mido.get_input_names()[0]  # Get the name of the first available MIDI input device
    print(f"Using MIDI input device: {input_name}")

    with mido.open_input(input_name) as inport:
        for msg in inport:
            process_midi_message(msg)

if __name__ == "__main__":
    listen_midi_input()
