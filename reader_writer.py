import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont

number_of_readers = 4
number_of_writers = 2
window_wid = 1000
window_hig = 1000
states_colors = {
    'idle': {
        'reader': QColor(0, 0, 255, 160),   
        'writer': QColor(128, 0, 128, 160)  
    },
    'waiting': {
        'reader': QColor(0, 180, 180, 160)
, 
        'writer': QColor(255, 165, 0, 160)   
    },
    'reading': {
        'reader': QColor(0, 255, 0, 160)     
    },
    'writing': {
        'writer': QColor(255, 0, 0, 160)     
    }
}


states_labels = {
    'idle': "no need for resources",
    'waiting': "looking for Resources",
    'reading': "using Resources",
    'writing': "using Resources"
}

class Actor:
    def __init__(self, index, role):
        self.index = index
        self.role = role  # 'reader' or 'writer'
        self.state = 'idle'

class Database:
    def __init__(self):
        self.active_readers = 0  # active reader
        self.active_writer = False  # are we writing anything into the database

class ReadersWriters(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("readers/writers")
        self.setGeometry(100, 100, window_wid, window_hig)
        self.database = Database()
        self.readers = [Actor(i, "reader") for i in range(number_of_readers)]
        self.writers = [Actor(i, "writer") for i in range(number_of_writers)]

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sim)
        self.timer.start(1000)  

    def update_sim(self):
        for r in self.readers:
            if r.state == 'idle' and random.random() < 0.4:
                r.state = 'waiting'
            elif r.state == 'waiting' and not self.database.active_writer:
                self.database.active_readers += 1
                r.state = 'reading'
            elif r.state == 'reading' and random.random() < 0.6:
                self.database.active_readers -= 1
                r.state = 'idle'

        for w in self.writers:
            if w.state == 'idle' and random.random() < 0.4:
                w.state = 'waiting'
            elif w.state == 'waiting' and not self.database.active_writer and self.database.active_readers == 0:
                self.database.active_writer = True
                w.state = 'writing'
            elif w.state == 'writing' and random.random() < 0.6:
                self.database.active_writer = False
                w.state = 'idle'

        self.update()

    def draw_agent(self, qp, agent, x, y):
        radius = 40
        color = states_colors.get(agent.state, {}).get(agent.role, QColor('gray'))
        label = states_labels.get(agent.state, "")

        gradient = QLinearGradient(x - radius, y - radius, x + radius, y + radius)
        gradient.setColorAt(0, QColor('black'))
        gradient.setColorAt(1, color)

        qp.setBrush(gradient)
        qp.setPen(QPen(QColor('black'), 2))
        qp.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)

        qp.setPen(QPen(color))
        qp.setFont(QFont('Arial', 12))
        prefix = 'R' if agent.role == 'reader' else 'W'
        qp.drawText(x - 10, y + 5, f"{prefix}{agent.index}")
        qp.setFont(QFont('Arial', 16))
        qp.drawText(x - 80, y + 60, label)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        center_x = self.width() // 2
        db_y = self.height() // 2
        reader_spacing = 250
        start_x_r = center_x - ((len(self.readers) - 1) * reader_spacing) // 2
        y_r = db_y - 200

        for i, r in enumerate(self.readers):
            x = start_x_r + i * reader_spacing
            self.draw_agent(qp, r, x, y_r)
            qp.setPen(QPen(QColor('black'), 2))
            qp.drawLine(x, y_r + 40, center_x, db_y - 50)

        writer_spacing = 250
        start_x_w = center_x - ((len(self.writers) - 1) * writer_spacing) // 2
        y_w = db_y + 200

        for i, w in enumerate(self.writers):
            x = start_x_w + i * writer_spacing
            self.draw_agent(qp, w, x, y_w)
            qp.setPen(QPen(QColor('black'), 2))
            qp.drawLine(x, y_w - 40, center_x, db_y + 50)

        db_width = 300
        db_height = 100
        qp.setPen(QPen(QColor('black'), 2))
        qp.setBrush(QColor(220, 220, 220))
        qp.drawRect(center_x - db_width // 2, db_y - db_height // 2, db_width, db_height)
        qp.setFont(QFont('Arial', 14))
        qp.drawText(center_x - 40, db_y - db_height // 2 - 10, "Database")

        indicator_x = center_x + db_width // 2 - 30
        indicator_y = db_y - 20
        gradient = QLinearGradient(indicator_x - 15, indicator_y - 15, indicator_x + 15, indicator_y + 15)
        if self.database.active_writer:
            gradient.setColorAt(0, QColor('black'))
            gradient.setColorAt(1, QColor('red'))
            state_text = "writing"
        elif self.database.active_readers > 0:
            gradient.setColorAt(0, QColor('black'))
            gradient.setColorAt(1, QColor('green'))
            state_text = f"reading ({self.database.active_readers})"
        else:
            gradient.setColorAt(0, QColor('black'))
            gradient.setColorAt(1, QColor('gray'))
            state_text = "idle"

        qp.setBrush(gradient)
        qp.setPen(QPen(QColor('black'), 1))
        qp.drawEllipse(indicator_x - 15, indicator_y - 15, 30, 30)
        qp.setFont(QFont('Arial', 10))
        qp.drawText(indicator_x - 40, indicator_y + 40, state_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReadersWriters()
    window.show()
    sys.exit(app.exec_())
