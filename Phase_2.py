import os
import json
import syllables
import random
import re
from midiutil import MIDIFile
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configuration
GROK_API_KEY = os.getenv('GROK_API_KEY')  # Required: Grok API key from .env
OUTPUT_DIR = "output_music"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def read_lyrics(file_path):
    """Read lyrics from a .txt file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lyrics = file.read().strip()
        if not lyrics:
            raise ValueError("Lyrics file is empty.")
        # Optionally clean structural markers (e.g., (Verse 1), (Chorus))
        lyrics = re.sub(r'\(\w+\s*\d*\)', '', lyrics).strip()
        return lyrics
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading lyrics file: {e}")
        return None

def call_grok_api(genre):
    """Placeholder for Grok API call (URL removed as requested)."""
    if not GROK_API_KEY:
        print("Error: GROK_API_KEY not set in .env file.")
        return None
    print("Error: Grok API call skipped (URL not provided). Using fallback config.")
    return None

def get_fallback_config(genre):
    """Provide fallback genre config."""
    fallback_configs = {
        "bhangra": {
            "tempo": "random.randint(130, 150)",
            "scale": ["C", "D", "E", "F", "G", "A", "B"],
            "chords": ["C", "F", "G", "Am"],
            "mood": "dance",
            "instruments": "dhol, tumbi, synth",
            "tempo_value": random.randint(130, 150)
        },
        "pop": {
            "tempo": "random.randint(100, 120)",
            "scale": ["C", "D", "E", "F", "G", "A", "B"],
            "chords": ["C", "G", "Am", "F"],
            "mood": "upbeat",
            "instruments": "guitar, drums, synth",
            "tempo_value": random.randint(100, 120)
        },
        "jazz": {
            "tempo": "random.randint(90, 110)",
            "scale": ["C", "D", "E", "F", "G", "A", "Bb"],
            "chords": ["Cmaj7", "Am7", "Dm7", "G7"],
            "mood": "smooth",
            "instruments": "piano, saxophone, double bass",
            "tempo_value": random.randint(90, 110)
        },
        "rock": {
            "tempo": "random.randint(120, 140)",
            "scale": ["C", "D", "E", "G", "A"],  # C minor pentatonic for rock
            "chords": ["C5", "G5", "A5", "F5"],  # Power chords
            "mood": "energetic",
            "instruments": "electric guitar, bass, drums",
            "tempo_value": random.randint(120, 140)
        }
    }
    return fallback_configs.get(genre.lower(), {
        "tempo": "random.randint(100, 120)",
        "scale": ["C", "D", "E", "F", "G", "A", "B"],
        "chords": ["C", "G", "Am", "F"],
        "mood": "generic",
        "instruments": "piano, drums, bass",
        "tempo_value": random.randint(100, 120)
    })

def get_syllables(lyrics):
    """Break English lyrics into syllables."""
    words = lyrics.split()
    syllable_list = []
    for word in words:
        syllable_count = syllables.estimate(word)
        for i in range(syllable_count):
            syllable_list.append((word, i, syllable_count))
    return syllable_list

def assign_notes_to_syllables(syllables_list, genre_config):
    """Assign notes and durations to syllables based on genre config."""
    scale = genre_config["scale"]
    chords = genre_config["chords"]
    note_sequence = []
    chord_idx = 0
    time = 0  # Absolute time, no reset

    # Chord-to-notes mapping
    chord_notes = {
        "Cmaj7": ["C", "E", "G", "B"],
        "Am7": ["A", "C", "E", "G"],
        "Fmaj7": ["F", "A", "C", "E"],
        "G7": ["G", "B", "D", "F"],
        "Dm7": ["D", "F", "A", "C"],
        "C": scale[:],
        "G": ["G", "B", "D"],
        "Am": ["A", "C", "E"],
        "F": ["F", "A", "C"],
        "G5": ["G", "D"],
        "D5": ["D", "A"],
        "A5": ["A", "E"],
        "C5": ["C", "G"],
        "F5": ["F", "C"],
        "Cm": ["C", "Eb", "G"],
        "Ab": ["Ab", "C", "Eb"],
        "Fm": ["F", "Ab", "C"]
    }

    for word, syl_idx, syl_count in syllables_list:
        current_chord = chords[chord_idx % len(chords)]
        note_pool = chord_notes.get(current_chord, scale)
        note = random.choice(note_pool)

        duration = 1 if syl_idx == syl_count - 1 else 0.5

        try:
            note_idx = scale.index(note) + (4 * 12)  # Octave 4
        except ValueError:
            note_idx = scale.index(scale[0]) + (4 * 12)

        note_sequence.append({
            "note": note,
            "midi_note": note_idx,
            "duration": duration,
            "time": time,
            "syllable": f"{word}-{syl_idx+1}"
        })

        time += duration
        # Change chord every 4 beats, but don't reset time
        if time >= (chord_idx + 1) * 4:
            chord_idx += 1

    return note_sequence

def generate_midi(note_sequence, genre_config, genre, filename="output.mid"):
    """Generate MIDI file with validation."""
    midi = MIDIFile(1)
    midi.addTempo(0, 0, genre_config["tempo_value"])

    # Validate note sequence to avoid overlaps
    active_notes = {}  # Track active notes by pitch
    for note in note_sequence:
        pitch = note["midi_note"]
        start_time = note["time"]
        duration = note["duration"]

        # Check for overlapping notes on same pitch
        if pitch in active_notes and start_time < active_notes[pitch]:
            print(f"Warning: Overlapping note detected for pitch {pitch} at time {start_time}. Adjusting duration.")
            duration = min(duration, active_notes[pitch] - start_time)
            if duration <= 0:
                continue  # Skip invalid note

        midi.addNote(
            track=0,
            channel=0,
            pitch=pitch,
            time=start_time,
            duration=duration,
            volume=100
        )

        # Update active notes
        active_notes[pitch] = start_time + duration

    with open(os.path.join(OUTPUT_DIR, filename), "wb") as output_file:
        midi.writeFile(output_file)
    return filename

def main():
    # Get user inputs
    lyrics_file = input("Enter the path to your lyrics .txt file (e.g., lyrics.txt): ").strip()
    genre = input("Enter the music genre (e.g., bhangra, pop, jazz, rock): ").strip()

    # Read lyrics from .txt file
    lyrics = read_lyrics(lyrics_file)
    if not lyrics:
        print("Failed to read lyrics. Exiting.")
        return

    print(f"Lyrics: {lyrics}")

    # Get genre config from Grok API
    genre_config = call_grok_api(genre)
    if not genre_config:
        print(f"Using fallback config for genre: {genre}")
        genre_config = get_fallback_config(genre)

    print(f"Genre config for {genre}:", genre_config)

    # Break into syllables
    syllable_list = get_syllables(lyrics)
    print("Syllables:", syllable_list)

    # Assign notes
    note_sequence = assign_notes_to_syllables(syllable_list, genre_config)
    print("Note Sequence:", note_sequence)

    # Generate MIDI
    midi_file = generate_midi(note_sequence, genre_config, genre, f"{genre}_melody.mid")
    print(f"MIDI file generated: {midi_file}")

if __name__ == "__main__":
    main()