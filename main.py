
import PyQt5
# import PyQt5.Qt
from keyboard import add_hotkey
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
    QCheckBox,
)
from PyQt5.QtGui import (
    QFont,
    QIcon,
    QIntValidator,
)

from player import FilePlayer

TOGGLE_KEY = 'f2'

def clamp(val, minimum, maximum):
    return max(minimum, min(val, maximum))
class QtStyle():
    @staticmethod
    def background_dark(widget):
        widget.setStyleSheet("background-color: #212121;")
    def white_text(widget):
        widget.setStyleSheet("color: #FFFFFF")
# class KeyPressSignal(QObject):
#     key_signal = pyqtSignal()
class PlayerWindow(QWidget):
    def __init__(self):
        super().__init__()

        icon = QIcon('main.ico')
        window_size = (300, 260)
        # window_size_x, window_size_y = window_size
        self.setGeometry(500, 100, *window_size)
        self.setWindowTitle("Rogrammer Player v2")
        self.setWindowIcon(icon)
        QtStyle.background_dark(self)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        title_font = QFont("Montserrat", 20)
        title_font.setBold(True)

        secondary_font = QFont("Montserrat", 12)
        song_font = QFont("Montserrat", 10)
        song_font.setBold(True)

        title = QLabel()
        title.setText('Rogrammer Player')
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title.setAlignment(Qt.AlignmentFlag.AlignTop)
        # title.setAlignment(PyQt5.QtCore.Qt.AlignmentFlag.AlignCenter)
        # title.setAlignment(PyQt5.QtCore.Qt.AlignmentFlag.AlignTop)
        QtStyle.white_text(title)
        vbox.addWidget(title)

        song_label = QLabel()
        song_label.setFont(secondary_font)
        song_label.setText('Current loaded song:')
        song_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.song_label = song_label
        QtStyle.white_text(song_label)
        vbox.addWidget(song_label)

        song_name = QLabel()
        self.song_name = song_name
        song_name.setFont(song_font)
        song_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        QtStyle.white_text(song_name)
        self.set_song("None")
        vbox.addWidget(song_name)

        octave_layout = QVBoxLayout()

        octave_label = QLabel()
        octave_label.setText("Octave Shift")
        octave_layout.addWidget(octave_label)
        QtStyle.white_text(octave_label)

        octave_line_edit = QLineEdit()
        octave_line_edit.setValidator(QIntValidator())
        octave_line_edit.setMaxLength(4)
        octave_line_edit.setText("0")
        QtStyle.white_text(octave_line_edit)
        octave_layout.addWidget(octave_line_edit)
        self.octave_line_edit = octave_line_edit

        octave_slider = QSlider(Qt.Orientation.Horizontal)
        octave_slider.setMinimum(-2)
        octave_slider.setMaximum(2)
        octave_slider.setValue(0)
        octave_layout.addWidget(octave_slider)
        self.octave_slider = octave_slider

        hbox.addLayout(octave_layout)

        error_layout = QVBoxLayout()
        
        error_label = QLabel()
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setText("Note Range Error:")
        error_layout.addWidget(error_label)
        QtStyle.white_text(error_label)

        error_check = QCheckBox()
        error_check.setChecked(True)
        error_check.setStyleSheet('margin-left: 50%; margin-right: 50%;')
        error_layout.addWidget(error_check)
        self.error_check = error_check

        hbox.addLayout(error_layout)
        
        vbox.addLayout(hbox)

        song_button = QPushButton()
        song_button.setText('Load song')
        vbox.addWidget(song_button)
        self.song_button = song_button
        song_button.setFont(song_font)
        QtStyle.white_text(song_button)

        self.setLayout(vbox)
        self.setFixedSize(self.size())
        song_button.setFocus()
    def set_song(self, name):
        self.song_name.setText(name)
        # self.song_label.setText(f" {name}")
    def choose_file(self):
        options = QFileDialog.Options()
        filter = "MIDI (*.mid)"
        default_dir = "scores"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Song", default_dir, filter, options=options)
        return file_name
    # def set_toggle_callback(self, func):
    #     self.player_toggle_callback = func
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key.Key_F2:
    #         callback = self.player_toggle_callback
    #         if callback:
    #             callback()
class PlayerController():
    def __init__(self, window):
        self.window = window
        self.player = None
        self.current_note_range_error = True
        self.current_octave_shift = 0
        window.song_button.pressed.connect(self.handle_song_button_press)
        window.octave_line_edit.textChanged.connect(self.handle_octave_line_edit_text_changed)
        window.octave_slider.valueChanged.connect(self.handle_octave_slider_value_change)
        window.error_check.stateChanged.connect(self.handle_note_state_changed)
        # window.set_toggle_callback(self.handle_player_toggle)
    @staticmethod
    def strip_filename(path):
        return path.split('/')[-1].split('.')[0]
    def handle_player_toggle(self):
        player = self.player
        if player:
            if player.playing:
                player.stop()
            else:
                player.play()
    def handle_song_button_press(self):
        name = self.window.choose_file()
        if name:
            player = FilePlayer(name)
            self.player = player
            file_name = self.strip_filename(name)
            self.window.set_song(file_name)

            if self.current_note_range_error != None:
                player.note_range_error = self.current_note_range_error
            if self.current_octave_shift != None:
                player.octave_shift = self.current_octave_shift
    def set_octave_shift(self, value):
        player = self.player
        if player:
            player.octave_shift = value
        self.current_octave_shift = value
    def set_note_range_error(self, value):
        player = self.player
        if player:
            player.note_range_error = value
        self.current_note_range_error = value
    def handle_note_state_changed(self, checked):
        self.set_note_range_error(checked == 2)
    def handle_octave_line_edit_text_changed(self):
        line_edit = self.window.octave_line_edit
        slider = self.window.octave_slider
        line_value = line_edit.text()
        try:
            line_int = int(line_value)
            line_clamped = clamp(line_int, slider.minimum(), slider.maximum())
            line_edit.setText(
                str(line_clamped)
            )
            slider.setValue(line_int)
            self.set_octave_shift(line_clamped)
        except ValueError:
            pass
            # slider.setValue(0)
   
    def handle_octave_slider_value_change(self):
        line_edit = self.window.octave_line_edit
        slider = self.window.octave_slider
        slider_value = slider.value()
        line_edit.setText(
            str(slider_value)
        )
        self.set_octave_shift(slider_value)
    
def main():
    application = QApplication([])
    player_window = PlayerWindow()
    player_window.show()
    controller = PlayerController(player_window)

    def released_event():
        controller.handle_player_toggle()
    
    add_hotkey(TOGGLE_KEY, released_event, suppress=True, trigger_on_release=True)

    application.exec()

if __name__ == "__main__":
    main()