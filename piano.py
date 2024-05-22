
from keyboard import press_and_release, press, release
from pynput.keyboard import Key, Controller 

KEYBOARD = Controller()

KEYS = "1!2@34$5%6^78*9(0qqwweerttyyuiiooppassddfgghhjjkllzzxccvvbbnm"
SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
TONIC_SCALE = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTES = ['C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1',
         'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2',
         'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
         'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
         'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
         'C6']
NOTE_LENGTHS = {
    'whole': 1,
    'half': 2,
    'quarter': 4,
    'eighth': 8,
    '16th': 16,
    '32nd': 32,
    '64th': 64
}

class Key:
    @staticmethod
    def _get_accidental_map(accidentals):
        SCALE_LENGTH = len(SCALE)
        times = abs(accidentals)
        direction = accidentals >= 1 and 1 or -1
        accidental_map = {}
        last_index = 0
        for i in range(times):
            movement = 7 if direction >= 1 else 5
            accidental_movement = -1 if direction >= 1 else 5
            next_key_pos = last_index + movement
            if next_key_pos >= SCALE_LENGTH:
                next_key_pos -= SCALE_LENGTH
            accidental_pos = next_key_pos+accidental_movement
            if accidental_pos >= SCALE_LENGTH:
                accidental_pos -= SCALE_LENGTH
            accidental = SCALE[accidental_pos]
            natural = SCALE[accidental_pos-1]
            accidental_map[natural] = accidental
            last_index = next_key_pos
        return accidental_map
    def __init__(self, accidentals):
        self.accidental_map = self._get_accidental_map(accidentals)
    def map(self, note):
        return self.accidental_map.get(note, None)

class NoteOutOfRangeError(Exception):
    pass

def create_keymap():
    key_map = {}
    for t in zip(NOTES, KEYS):
        note, key = t
        key_map[note] = key
    return key_map

key_map = create_keymap()

def pitch_to_note(pitch):
    octave = (pitch // 12) - 1
    note_index = pitch % 12
    note = SCALE[note_index]
    return f"{note}{octave}"

def distance_from_note(note, distance):
    try:
        note_pos = SCALE.index(note)
        return SCALE[note_pos+distance]
    except IndexError:
        print('note not found')

def play_note(note):
    key = key_map.get(note, None)
    if key:
        if '#' in note:
            press('shift')
            press_and_release(key)
            release('shift')
        else:
            KEYBOARD.tap(key)
            #press_and_release(key)
    else:
        raise NoteOutOfRangeError(f"{note} is out of range")