"""
AI Music Melody Generator
Uses Markov Chains to generate simple melodies based on musical patterns
"""

import random
from midiutil import MIDIFile


class MusicGenerator:
    def __init__(self):
        # Musical scale: C major scale (MIDI note numbers)
        self.scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5

        # Note names for reference
        self.note_names = ["C", "D", "E", "F", "G", "A", "B", "C"]

        # Training data: simple melodic patterns
        self.training_patterns = [
            [0, 2, 4, 2, 0],  # C-E-G-E-C
            [0, 0, 4, 4, 5, 5, 4],  # Twinkle pattern
            [4, 4, 5, 7, 7, 5, 4, 2],  # Rising and falling
            [0, 2, 4, 5, 4, 2, 0],  # Up and down scale
            [4, 2, 0, 2, 4, 4, 4],  # Simple melody
        ]

        # Markov chain transition matrix
        self.transitions = {}
        self._build_markov_chain()

    def _build_markov_chain(self):
        """Build a Markov chain from training patterns"""
        for pattern in self.training_patterns:
            for i in range(len(pattern) - 1):
                current = pattern[i]
                next_note = pattern[i + 1]

                if current not in self.transitions:
                    self.transitions[current] = []

                self.transitions[current].append(next_note)

    def generate_melody(self, length=16):
        """Generate a melody using the Markov chain"""
        if not self.transitions:
            return []

        current = random.choice(list(self.transitions.keys()))
        melody = [current]

        for _ in range(length - 1):
            if current in self.transitions and self.transitions[current]:

                next_note = random.choice(self.transitions[current])
                melody.append(next_note)
                current = next_note
            else:

                current = random.choice(list(self.transitions.keys()))
                melody.append(current)

        return melody

    def melody_to_midi_notes(self, melody):
        """Convert scale indices to actual MIDI notes"""
        return [self.scale[note % len(self.scale)] for note in melody]

    def save_as_midi(self, melody, filename="generated_music.mid", tempo=120):
        """Save the generated melody as a MIDI file"""
        midi_notes = self.melody_to_midi_notes(melody)

        # Create MIDI file with 1 track
        midi = MIDIFile(1)
        track = 0
        channel = 0
        time = 0

        midi.addTrackName(track, time, "AI Generated Melody")
        midi.addTempo(track, time, tempo)

        # Add notes to the track
        duration = 1  # Each note lasts 1 beat
        volume = 100  # 0-127, as per MIDI standard

        for i, pitch in enumerate(midi_notes):
            midi.addNote(track, channel, pitch, time + i, duration, volume)

        with open(filename, "wb") as output_file:
            midi.writeFile(output_file)

        print(f"✓ MIDI file saved as: {filename}")
        return filename

    def print_melody(self, melody):
        """Print the melody in a readable format"""
        print("\nGenerated Melody:")
        print("=" * 50)

        notes = [self.note_names[note % len(self.note_names)] for note in melody]
        print("Notes: ", " - ".join(notes))
        print("Pattern:", melody)
        print("=" * 50)


def main():
    print("=" * 50)
    print("AI MUSIC GENERATOR - AMG")
    print("Using Markov Chains for Melody Generation")
    print("=" * 50)
    print()

    generator = MusicGenerator()

    try:
        length = int(input("Enter melody length (8-32 notes): "))
        if length < 8 or length > 32:
            print("Using default length of 16 notes")
            length = 16
    except ValueError:
        print("Invalid input. Using default length of 16 notes")
        length = 16

    try:
        tempo = int(input("Enter tempo (60-180 BPM): "))
        if tempo < 60 or tempo > 180:
            print("Using default tempo of 120 BPM")
            tempo = 120
    except ValueError:
        print("Invalid input. Using default tempo of 120 BPM")
        tempo = 120

    print("\nGenerating melody...")
    melody = generator.generate_melody(length)
    generator.print_melody(melody)
    filename = f"ai_melody_{random.randint(1000, 9999)}.mid"
    generator.save_as_midi(melody, filename, tempo)
    print("Done")
    print("\nTip: Try importing it into GarageBand, FL Studio, or MuseScore")


if __name__ == "__main__":
    main()
