import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient

buffer_capacity = 5
number_of_producers = 3
number_of_consumers = 3
window_wid = 1000
window_hig = 800

states_colors = {
    'idle': QColor('gray'),
    'waiting': QColor('darkGoldenrod'),
    'producing': QColor('green'),
    'consuming': QColor('red')
}

states_labels = {
    'idle': "idle",
    'waiting': "waiting",
    'producing': "producing",
    'consuming': "consuming"
}

# waiting state must be represented due to stuff like buffer full/empty 
class actor:
    def __init__(self, index, role):
        self.index = index
        self.role = role  
        self.state = 'idle'
    # the role is ethier consuming or produceing
class buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = 0

class BoundedBuffer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("the bounded Buffer Problem")
        self.setGeometry(100, 100, window_wid, window_hig)

        self.buffer = buffer(buffer_capacity)
        self.producers = [actor(i, "producer") for i in range(number_of_producers)]
        self.consumers = [actor(i, "consumer") for i in range(number_of_consumers)]

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sim)
        self.timer.start(1000)

    def update_sim(self):
        for p in self.producers:

            if p.state == 'idle' and random.random() < 0.4:
                p.state = 'waiting'
            # if we are waiting for resoures and the items already in the buffer are less then the buffer capacity add an item
            elif p.state == 'waiting' and self.buffer.items < self.buffer.capacity:
                self.buffer.items += 1
                p.state = 'producing'
                text_color = QColor('darkGoldenrod')
            elif p.state == 'producing' and random.random() < 0.6:
                p.state = 'idle'

        for c in self.consumers:
            if c.state == 'idle' and random.random() < 0.4:
                c.state = 'waiting'
            # same logic for consuming an item
            elif c.state == 'waiting' and self.buffer.items > 0:
                self.buffer.items -= 1
                c.state = 'consuming'
            elif c.state == 'consuming' and random.random() < 0.5:
                c.state = 'idle'

        self.update()

    def draw_agent(self, qp, agent, x, y):
        radius = 40
        color = states_colors.get(agent.state, QColor('gray'))
        label = states_labels.get(agent.state, "")

        gradient = QLinearGradient(x - radius, y - radius, x + radius, y + radius)
        gradient.setColorAt(0, QColor('black'))
        gradient.setColorAt(1, color)

        qp.setBrush(gradient)
        qp.setPen(QPen(QColor('black'), 2))
        qp.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)

        qp.setPen(QPen(color))
        qp.setFont(QFont('Arial', 12))
        prefix = 'P' if agent.role == 'producer' else 'C'
        qp.drawText(x - 10, y + 5, f"{prefix}{agent.index}")
        qp.setFont(QFont('Arial', 10))
        qp.drawText(x - 40, y + 50, label)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        buffer_y = self.height() // 2
        radius = 300
        producer_spacing = 120
        start_x_p = center_x - ((len(self.producers) - 1) * producer_spacing) // 2
        y_p = buffer_y - 200

        for i, p in enumerate(self.producers):
            x =     start_x_p + i * producer_spacing
            self.draw_agent(qp, p, x, y_p)

        consumer_spacing = 120
        start_x_c = center_x - ((len(self.consumers) - 1) * consumer_spacing) // 2
        y_c = buffer_y + 200

        for i, c in enumerate(self.consumers):
            x = start_x_c + i * consumer_spacing
            self.draw_agent(qp, c, x, y_c)


        # Draw buffer box
        buffer_width = 300
        buffer_height = 100
        qp.setPen(QPen(QColor('black'), 2))
        qp.setBrush(QColor(220, 220, 220))
        qp.drawRect(center_x - buffer_width // 2, buffer_y - buffer_height // 2, buffer_width, buffer_height)
        qp.setFont(QFont('Arial', 14))
        qp.drawText(center_x - 30, buffer_y - buffer_height // 2 - 10, "Buffer")

        slot_width = buffer_width // self.buffer.capacity
        for i in range(self.buffer.capacity):
            x = center_x - buffer_width // 2 + i * slot_width + 5
            y = buffer_y - buffer_height // 2 + 20
            w = slot_width - 10
            h = buffer_height - 40
            filled = i < self.buffer.items

            qp.setBrush(QColor('red') if filled else QColor('white'))
            qp.setPen(QPen(QColor('black'), 1))
            qp.drawRect(x, y, w, h)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoundedBuffer()
    window.show()
    sys.exit(app.exec_())
