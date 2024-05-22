
from mido import MidiFile
from threading import Thread, Event
from piano import pitch_to_note, play_note, NoteOutOfRangeError

class FilePlayer():
    def __init__(self, path):
        self.path = path
        self.file = MidiFile(path)
        self.playing = False
        self.octave_shift = 0
        self.note_range_error = True
        self.stop_event = Event()
    def _run_thread(self):
        self.stop_event.clear()
        for message in self.file.play():
            if self.stop_event.is_set():
                return
            elif message.type == "note_on":
                if message.velocity <= 0:
                    continue
                note_name = pitch_to_note(message.note+(12*self.octave_shift))
                if note_name:
                    try:
                        play_note(note_name)
                    except NoteOutOfRangeError:
                        if self.note_range_error:
                            raise NoteOutOfRangeError
    def play(self):
        self.playing = True
        play_thread = Thread(target=self._run_thread)
        play_thread.start()
    def stop(self):
        self.playing = False
        self.stop_event.set()