import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont
import math

number_of_philos = 6

class philo:
    def __init__(self, index):
        self.index = index
        self.state = 'thinking'

class fork:
    def __init__(self):
        self.in_use = False

class DiningPhilosophers(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Dining Philosophers Problem")
        self.setGeometry(100, 100, 1000, 1000)  
        self.philosophers = [philo(i) for i in range(number_of_philos)]
        self.forks = [fork() for _ in range(number_of_philos)]

        # timer for sim
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sim)
        self.timer.start(1000)  

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing) 
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 500  

        # Draw table
        qp.setPen(QPen(QColor('black'), 2))
        qp.setBrush(QColor(200, 200, 200))
        qp.drawEllipse(center_x - 125, center_y - 125, 250, 250)
        qp.setFont(QFont('Arial', 14))
        qp.drawText(center_x - 35, center_y, "dinnig table")

        # Draw philosophers with gradient
        for i, p in enumerate(self.philosophers):
            angle = (2 * math.pi / number_of_philos) * i
            x = center_x + int(math.cos(angle) * radius)
            y = center_y + int(math.sin(angle) * radius)

            # Set gradient based on state
            gradient = QLinearGradient(x - 35, y - 35, x + 35, y + 35)
            if p.state == 'thinking':
                gradient.setColorAt(0, QColor('green'))
               
                state_text = "thinking -> we dont need resources 😊"
                text_color = QColor('green')
            elif p.state == 'hungry':
                gradient.setColorAt(0, QColor('black'))
                gradient.setColorAt(1, QColor('black'))
                state_text = "hungry -> wait and look for resources"
                text_color = QColor('black')
            else:  # Eating
                gradient.setColorAt(0, QColor('black'))
                gradient.setColorAt(1, QColor('red'))
                state_text = "eating -> using resources "
                text_color = QColor('red')

            qp.setBrush(gradient)
            qp.setPen(QPen(QColor('black'), 2))
            qp.drawEllipse(x - 35, y - 35, 70, 70)
            qp.setPen(QPen(text_color, 1))
            qp.setFont(QFont('Arial', 12))
            qp.drawText(x - 18, y - 40, f"P{i}")
            qp.drawText(x - 30, y + 60, state_text)

        # irrelevant drawing logic of recs for forks
        for i, fork in enumerate(self.forks):
            angle = (2 * math.pi / number_of_philos) * (i + 0.5)
            x = center_x + int(math.cos(angle) * (radius - 125))
            y = center_y + int(math.sin(angle) * (radius - 125))
            gradient = QLinearGradient(x, y, x + 15, y + 15)
            gradient.setColorAt(0, QColor('black'))
            gradient.setColorAt(1, QColor('red' if fork.in_use else 'black'))
            qp.setBrush(gradient)
            qp.setPen(QPen(QColor('black'), 1))
            qp.drawRect(x, y, 15, 15)  
            qp.setPen(QPen(QColor('black'), 1))
            qp.setFont(QFont('Arial', 14))
            qp.drawText(x + 20, y + 20, f"fork {i} {'is being used right now' if fork.in_use else ''}")

    def update_sim(self):
        
        for i in range(number_of_philos):
            p = self.philosophers[i]
            left = i
            right = (i + 1) % number_of_philos

            if p.state == 'thinking':
                if random.random() < 0.4:
                    p.state = 'hungry'
            elif p.state == 'hungry':
                if not self.forks[left].in_use and not self.forks[right].in_use:
                    self.forks[left].in_use = True
                    self.forks[right].in_use = True
                    p.state = 'eating'
            elif p.state == 'eating':
                if random.random() < 0.5:
                    p.state = 'thinking'
                    self.forks[left].in_use = False
                    self.forks[right].in_use = False

        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiningPhilosophers()
    window.show()
    sys.exit(app.exec_())