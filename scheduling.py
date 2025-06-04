from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QPushButton, QComboBox, QLabel, QTableWidget,
    QTableWidgetItem, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont
from PyQt5.QtCore import Qt, QTimer
import sys
from math import ceil
from collections import deque

class gantt_chart_widget(QWidget):
    def __init__(self):
        super().__init__()
        # grantt data stores process id , start time and end time
        self.gantt_data = [] 
        self.max_time = 0
        self.current_time = 0
        self.animation_running = False
        self.setMinimumHeight(150)  

        # anim timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.animation_speed = 100  # ms per update, feels snappy

       
        self.chart_font = QFont("impact", 14)
        self.chart_font.setBold(True)

    def set_gantt_data(self, gantt_data, max_time):
        # reset for new chart
        self.gantt_data = gantt_data
        self.max_time = max_time
        self.current_time = 0
        self.animation_running = False
        self.timer.stop()
        self.update()

    def start_animation(self):
        
        if self.max_time == 0 or not self.gantt_data:
            return
        self.current_time = 0
        self.animation_running = True
        self.timer.start(self.animation_speed)
        self.update()

    # anim
    def update_animation(self):
        
        if self.current_time >= self.max_time:
            self.timer.stop()
            self.animation_running = False
            self.current_time = self.max_time
        else:
            self.current_time += 0.1  
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
         # handle nothing to draw yet case
        if self.max_time == 0:
            return 

        # chat styling
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor(0, 0, 0))
        gradient.setColorAt(1, QColor(100, 0, 0))
        painter.setBrush(gradient)
        painter.drawRect(0, 0, width, height)



        #timeline



        # set timeline
        timeline_length = ceil(self.max_time)
        unit_width = width / timeline_length

        # draw empty timeline
        timeline_gradient = QLinearGradient(0, 50, width, 50)
        timeline_gradient.setColorAt(0, QColor(50, 0, 0))
        timeline_gradient.setColorAt(1, QColor(200, 0, 0))
        painter.setBrush(timeline_gradient)
        painter.drawRect(0, 50, int(width), 30)

        # fill in the timeline (chat)
        filled_width = min(self.current_time, self.max_time) * unit_width
        filled_gradient = QLinearGradient(0, 50, filled_width, 50)
        filled_gradient.setColorAt(0, QColor(150, 0, 0))
        filled_gradient.setColorAt(1, QColor(255, 50, 50))
        painter.setBrush(filled_gradient)
        painter.drawRect(0, 50, int(filled_width), 30)

      
        painter.setFont(self.chart_font)
        painter.setPen(QColor(255, 255, 255))  
        for i in range(timeline_length + 1):
            x = i * unit_width
            painter.drawLine(int(x), 0, int(x), height)
            painter.drawText(int(x), height - 10, str(i))

        colors = [
            (QColor(100, 0, 0), QColor(255, 100, 100)),
            (QColor(80, 0, 0), QColor(200, 80, 80)),
            (QColor(120, 0, 0), QColor(255, 120, 120)),
            (QColor(90, 0, 0), QColor(220, 90, 90))
        ]
        for idx, (pid, start, end) in enumerate(self.gantt_data):
            if start > self.current_time:
                continue 
            x_start = start * unit_width
            x_end = min(end, self.current_time) * unit_width
            start_color, end_color = colors[idx % len(colors)]
            process_gradient = QLinearGradient(x_start, 80, x_end, 80)
            process_gradient.setColorAt(0, start_color)
            process_gradient.setColorAt(1, end_color)
            painter.setBrush(process_gradient)

           
            if end > self.current_time and self.animation_running:
                pen = QPen(Qt.DashLine)
                pen.setColor(QColor(255, 255, 255))
                pen.setWidth(2)
                painter.setPen(pen)
            else:
                painter.setPen(QColor(255, 255, 255))

            painter.drawRect(int(x_start), 80, int(x_end - x_start), 30)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(int(x_start + 5), 100, pid)

class cpu_scheduler_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cpu scheduling visualizer")
        self.setGeometry(200, 200, 800, 600)

       
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        #styling
        self.setStyleSheet("""
            qmainwindow, qwidget {
                background-color: black;
            }
            qlineedit {
                background-color: #300000;
                color: #ff5050;
                border: 2px solid #ff0000;
                font-family: impact;
                font-size: 16px;
                padding: 5px;
            }
            qpushbutton {
                background-color: #500000;
                color: #ffffff;
                border: 2px solid #ff0000;
                border-radius: 10px;
                font-family: impact;
                font-size: 22px;
                padding: 12px 20px;
                min-width: 200px;
                margin: 2px;
            }
            qpushbutton:hover {
                background-color: #800000;
                border: 2px solid #ff5050;
            }
            qpushbutton:pressed {
                background-color: #a00000;
                border: 2px solid #ffffff;
            }
            qpushbutton#animatebutton {
                font-style: italic;  /* making the animate button stand out */
            }
            qcombobox {
                background-color: #300000;
                color: #ff5050;
                border: 2px solid #ff0000;
                font-family: impact;
                font-size: 16px;
                padding: 5px;
            }
            qcombobox qabstractitemview {
                background-color: #300000;
                color: #ff5050;
                selection-background-color: #500000;
            }
            qlabel {
                color: #ff5050;
                font-family: impact;
                font-size: 20px;
            }
            qtablewidget {
                background-color: #200000;
                color: #ff5050;
                border: 2px solid #ff0000;
                font-family: impact;
                font-size: 16px;
            }
            qheaderview::section {
                background-color: #500000;
                color: #ffffff;
                font-family: impact;
                font-size: 18px;
                border: 1px solid #ff0000;
            }
        """)

        # input fields for process details
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("process id")
        input_layout.addWidget(self.pid_input)

        self.arrival_input = QLineEdit()
        self.arrival_input.setPlaceholderText("arrival time")
        input_layout.addWidget(self.arrival_input)

        self.burst_input = QLineEdit()
        self.burst_input.setPlaceholderText("burst time")
        input_layout.addWidget(self.burst_input)

        self.priority_input = QLineEdit()
        self.priority_input.setPlaceholderText("priority")
        input_layout.addWidget(self.priority_input)

        add_button = QPushButton("add process")
        add_button.clicked.connect(self.add_process)
        input_layout.addWidget(add_button)

        # table to show all processes
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["process id", "arrival time", "burst time", "priority"])
        self.process_table.setRowCount(0)
        main_layout.addWidget(self.process_table)

        # algorithm selection stuff
        algo_layout = QHBoxLayout()
        main_layout.addLayout(algo_layout)
        algo_label = QLabel("select algorithm:")
        algo_layout.addWidget(algo_label)
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "fcfs",
            "sjf (non-preemptive)",
            "sjf (preemptive)",
            "round robin",
            "priority (non-preemptive)",
            "priority (preemptive)",
            "multilevel queue",
            "multilevel feedback queue"
        ])
        algo_layout.addWidget(self.algo_combo)
        self.quantum_input = QLineEdit()
        self.quantum_input.setPlaceholderText("time quantum (only for rr, mlq, mlfq)")
        self.quantum_input.setEnabled(False)
        algo_layout.addWidget(self.quantum_input)
        self.algo_combo.currentTextChanged.connect(self.toggle_quantum_input)

        # buttons 
        button_widget = QWidget()
        button_widget.setFixedHeight(120)
        button_layout = QGridLayout()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)

        run_button = QPushButton("compute schedule")
        run_button.setObjectName("runbutton")
        run_button.clicked.connect(self.run_simulation)
        button_layout.addWidget(run_button, 0, 0, 1, 2) 

        animate_button = QPushButton("start animation")
        animate_button.setObjectName("animatebutton")
        animate_button.clicked.connect(self.start_animation)
        button_layout.addWidget(animate_button, 1, 1, 1, 1)

        clear_button = QPushButton("clear all")
        clear_button.setObjectName("clearbutton")
        clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_button, 1, 0, 1, 1)

        button_layout.setHorizontalSpacing(10)
        button_layout.setVerticalSpacing(10)

        self.gantt_widget = gantt_chart_widget()
        main_layout.addWidget(self.gantt_widget)

        # keep track of all processes
        self.processes = []

    def toggle_quantum_input(self, algo):
        # enable quantum input only for algorithms that need it
        self.quantum_input.setEnabled(algo in ["round robin", "multilevel queue", "multilevel feedback queue"])

    def add_process(self):
        pid = self.pid_input.text().strip()
        if not pid:
            QMessageBox.warning(self, "invalid input", "process id cannot be empty.")
            return

        try:
            arrival_text = self.arrival_input.text().strip()

            #handle and catch
            if not arrival_text:
                raise ValueError("arrival time cannot be empty.")
            arrival = float(arrival_text)
            if arrival < 0:
                raise ValueError("arrival time must be non-negative.")

            burst_text = self.burst_input.text().strip()
            if not burst_text:
                raise ValueError("burst time cannot be empty.")
            burst = float(burst_text)
            if burst <= 0:
                raise ValueError("burst time must be positive.")

            priority_text = self.priority_input.text().strip()
            priority = int(priority_text) if priority_text else 5  # default to 5 if empty
            if priority < 1:
                raise ValueError("priority must be positive.")
        except ValueError as e:
            QMessageBox.warning(self, "invalid input", str(e))
            return

        # add the process to our list and table
        self.processes.append({"pid": pid, "arrival": arrival, "burst": burst, "priority": priority})
        row = self.process_table.rowCount()
        self.process_table.setRowCount(row + 1)
        self.process_table.setItem(row, 0, QTableWidgetItem(pid))
        self.process_table.setItem(row, 1, QTableWidgetItem(str(arrival)))
        self.process_table.setItem(row, 2, QTableWidgetItem(str(burst)))
        self.process_table.setItem(row, 3, QTableWidgetItem(str(priority)))
        self.pid_input.clear()
        self.arrival_input.clear()
        self.burst_input.clear()
        self.priority_input.clear()

    def clear_all(self):
        
        self.processes = []
        self.process_table.setRowCount(0)
        self.gantt_widget.set_gantt_data([], 0)
        self.quantum_input.clear()

    def run_simulation(self):
        #handle no process case
        if not self.processes:
            QMessageBox.warning(self, "no processes", "please add at least one process.")
            return

        algo = self.algo_combo.currentText()
        quantum = None

        # algos that need quantum handle invalid
        if algo in ["round robin", "multilevel queue", "multilevel feedback queue"]:
            quantum_text = self.quantum_input.text().strip()
            if not quantum_text:
                QMessageBox.warning(self, "invalid input", "time quantum cannot be empty for this algorithm.")
                return
            try:
                quantum = float(quantum_text)
                if quantum <= 0:
                    raise ValueError("time quantum must be positive.")
            except ValueError:
                QMessageBox.warning(self, "invalid input", "time quantum must be a positive number.")
                return

        #run the scheduling and update the chart
        gantt_data, max_time = self.compute_schedule(algo, quantum)
        self.gantt_widget.set_gantt_data(gantt_data, max_time)

    def start_animation(self):
        
        self.gantt_widget.start_animation()

    def compute_schedule(self, algo, quantum):
        processes = sorted(self.processes, key=lambda x: x["arrival"])
        gantt_data = []
        current_time = 0
        max_time = 0

        try:
            if algo == "fcfs":
                # first come : first served
                for p in processes:
                    start = max(current_time, p["arrival"])
                    end = start + p["burst"]
                    gantt_data.append((p["pid"], start, end))
                    current_time = end
                    max_time = end

            elif algo == "sjf (non-preemptive)":
                # shortest job first, no interruptions
                remaining = processes.copy()
                while remaining:
                    available = [p for p in remaining if p["arrival"] <= current_time]
                    if not available:
                        current_time += 1
                        continue
                    shortest = min(available, key=lambda x: x["burst"])
                    start = max(current_time, shortest["arrival"])
                    end = start + shortest["burst"]
                    gantt_data.append((shortest["pid"], start, end))
                    current_time = end
                    max_time = end
                    remaining.remove(shortest)

            elif algo == "sjf (preemptive)":
                # shortest job first, preemptive
                remaining = [(p, p["burst"]) for p in processes]  # (process, remaining_burst)
                while remaining:
                    available = [(p, b) for p, b in remaining if p["arrival"] <= current_time]
                    if not available:
                        current_time += 1
                        continue
                    shortest = min(available, key=lambda x: x[1])
                    p, burst = shortest
                    start = current_time
                    current_time += 1
                    burst -= 1
                    gantt_data.append((p["pid"], start, current_time))
                    max_time = current_time
                    if burst <= 0:
                        remaining.remove((p, burst + 1))
                    else:
                        remaining[remaining.index((p, burst + 1))] = (p, burst)

            elif algo == "round robin":
                
                queue = deque([(p, p["burst"]) for p in processes])
                current_time = min(p["arrival"] for p in processes)
                while queue:
                    p, burst = queue.popleft()
                    start = max(current_time, p["arrival"])
                    exec_time = min(burst, quantum)
                    end = start + exec_time
                    gantt_data.append((p["pid"], start, end))
                    current_time = end
                    max_time = end
                    new_burst = burst - exec_time
                    if new_burst > 0:
                        queue.append((p, new_burst))

            elif algo == "priority (non-preemptive)":
                # high priority goes first, no interruptions
                remaining = processes.copy()
                while remaining:
                    available = [p for p in remaining if p["arrival"] <= current_time]
                    if not available:
                        current_time += 1
                        continue
                    highest = min(available, key=lambda x: x["priority"])
                    start = max(current_time, highest["arrival"])
                    end = start + highest["burst"]
                    gantt_data.append((highest["pid"], start, end))
                    current_time = end
                    max_time = end
                    remaining.remove(highest)

            elif algo == "priority (preemptive)":
                # high priority can interrupt
                remaining = [(p, p["burst"]) for p in processes]
                while remaining:
                    available = [(p, b) for p, b in remaining if p["arrival"] <= current_time]
                    if not available:
                        current_time += 1
                        continue
                    highest = min(available, key=lambda x: x[0]["priority"])
                    p, burst = highest
                    start = current_time
                    current_time += 1
                    burst -= 1
                    gantt_data.append((p["pid"], start, current_time))
                    max_time = current_time
                    if burst <= 0:
                        remaining.remove((p, burst + 1))
                    else:
                        remaining[remaining.index((p, burst + 1))] = (p, burst)

            elif algo == "multilevel queue":
                # two queues: high-priority uses rr, low-priority uses fcfs
                high_priority = [p for p in processes if p["priority"] <= 3]
                low_priority = [p for p in processes if p["priority"] > 3]
                high_queue = deque([(p, p["burst"]) for p in sorted(high_priority, key=lambda x: x["arrival"])])
                low_queue = sorted(low_priority, key=lambda x: x["arrival"])
                current_time = min(p["arrival"] for p in processes)

                while high_queue or low_queue:
                    if high_queue:
                        p, burst = high_queue.popleft()
                        start = max(current_time, p["arrival"])
                        exec_time = min(burst, quantum)
                        end = start + exec_time
                        gantt_data.append((p["pid"], start, end))
                        current_time = end
                        max_time = end
                        new_burst = burst - exec_time
                        if new_burst > 0:
                            high_queue.append((p, new_burst))
                    elif low_queue:
                        p = low_queue.pop(0)
                        start = max(current_time, p["arrival"])
                        end = start + p["burst"]
                        gantt_data.append((p["pid"], start, end))
                        current_time = end
                        max_time = end

            elif algo == "multilevel feedback queue":
                # two queues: high-priority rr, low-priority fcfs with feedback
                queue1 = deque([(p, p["burst"], 0) for p in processes])  # (process, remaining_burst, total_cpu_used)
                queue2 = deque([])
                current_time = min(p["arrival"] for p in processes)
                threshold = quantum * 2  # move to lower queue if cpu usage is too high

                while queue1 or queue2:
                    if queue1:
                        p, burst, cpu_used = queue1.popleft()
                        start = max(current_time, p["arrival"])
                        exec_time = min(burst, quantum)
                        end = start + exec_time
                        gantt_data.append((p["pid"], start, end))
                        current_time = end
                        max_time = end
                        new_burst = burst - exec_time
                        cpu_used += exec_time
                        if new_burst > 0:
                            if cpu_used > threshold:
                                queue2.append((p, new_burst, cpu_used))
                            else:
                                queue1.append((p, new_burst, cpu_used))
                    elif queue2:
                        p, burst, _ = queue2.popleft()
                        start = max(current_time, p["arrival"])
                        end = start + burst
                        gantt_data.append((p["pid"], start, end))
                        current_time = end
                        max_time = end

        except Exception as e:
           
            QMessageBox.critical(self, "error", f"an error occurred during scheduling: {str(e)}")
            return [], 0

        return gantt_data, max_time

def main():
   
    app = QApplication(sys.argv)
    window = cpu_scheduler_window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()