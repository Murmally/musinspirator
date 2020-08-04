from midiutil.MidiFile import MIDIFile
import json
import os

# reads options from config file, returns dictionary
def load_config_data(filename = "config.json"):
	config_file = open(filename)
	data = json.load(config_file)
	config_file.close()
	return data


# returns integer of appropriate root key in MIDI
def compute_base_pitch(key):
	# C4 = 60 (middle C)
	base_pitch = 60 + int(key["root_key_offset"])
	root_key = key["root_key"].upper()
	offset = 2 * (ord(key["root_key"]) - ord("C"))
	if root_key in ['A', 'B']:
		offset += 1
	elif root_key in ['F', 'G', 'H']:
		offset -= 1

	base_pitch += offset + 12 * int(key["octave_offset"])
	return base_pitch


# returns tons shifts appropriate for given scale
def define_tone_shifts(scale):
	if scale.lower() == "major":
		tone_shifts = [2, 2, 1, 2, 2, 2, 1]
	elif scale.lower() == "minor":
		tone_shifts = [2, 1, 2, 2, 1, 2, 2]
	return tone_shifts


# generates pitches for all corresponding notes
def get_all_tones(base_pitch, tone_shifts, key):
	current_note = base_pitch + int(key["octave_lower_reach"]) * 12
	notes = [current_note]
	for _ in range(int(key["octave_lower_reach"]), int(key["octave_higher_reach"]) + 1):
		for shift in tone_shifts:
			current_note += shift
			# 26 is the minimum pitch (MIDI limitation)
			if current_note < 26:
				continue
			notes.append(current_note)
	return notes

# returns array of ints appropriate to the key
def get_notes_in_octave(key):
	base_pitch = compute_base_pitch(key)
	tone_shifts = define_tone_shifts(key["scale"])
	tones = get_all_tones(base_pitch, tone_shifts, key)
	return tones


# generates sequence of chords, eg. 2-4-5-1
def generate_chord_progression(key, num_of_chords = 4, repeat = True):
	return


def generate_scale(notes, filename = "scale.mid"):
	file = MIDIFile(1)
	track, time, channel, duration, volume = 0, 0, 0, 1, 100
	tempo = 120 # BPM - beats per minute

	file.addTrackName(track, time, "Scale")
	file.addTempo(track, time, tempo)

	for note in notes:
		file.addNote(track, channel, note, time, duration, volume)
		print(note)
		time += 1
	
	if os.path.exists(filename):
		os.remove(filename)
	with open(filename, 'wb') as out:
		file.writeFile(out)


config_data = load_config_data()
notes = get_notes_in_octave(config_data["key"])
generate_scale(notes)
