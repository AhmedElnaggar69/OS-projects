import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QMessageBox, QSpinBox
)
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class RequestDialog(QDialog):
    def __init__(self, num_resources, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make a Resource Request")
        self.num_resources = num_resources
        self.request = []
        self.process_id = None
        self.parent_gui = parent  # optional: for error dialog

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter Process ID (e.g., P0, P1):"))
        self.process_input = QLineEdit()
        layout.addWidget(self.process_input)

        layout.addWidget(QLabel("Enter requested resources:"))
        self.resource_inputs = []
        for i in range(self.num_resources):
            le = QLineEdit()
            le.setPlaceholderText(f"R{i}")
            layout.addWidget(le)
            self.resource_inputs.append(le)

        submit_btn = QPushButton("Submit Request")
        submit_btn.clicked.connect(self.submit)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit(self):
        try:
            process_str = self.process_input.text().strip()
            if not process_str.startswith("P") or not process_str[1:].isdigit():
                raise ValueError("Invalid process ID format.")

            self.process_id = int(process_str[1:])
            self.request = [int(le.text()) for le in self.resource_inputs]

            if any(r < 0 for r in self.request):
                raise ValueError("Resource values must be non-negative.")

            self.accept()

        except ValueError as e:
            if self.parent_gui:
                self.parent_gui.show_error(str(e))
            else:
                print("Input Error:", e)




    


def BankerLogic(self,Allocation, Max, Available):
    Allocation = np.array(Allocation)
    Max = np.array(Max)
    Available = np.array(Available)
    Need = Max - Allocation
    Finish = [False] * len(Allocation)
    SafeSeq = []
    # we need to check if the input is valid
    if Allocation.shape[0] != Max.shape[0]:
        message = "Error: Allocation and Max matrices must have the same number of processes" # different number of processes
        return SafeSeq,[], message
    
    if np.any(Need > Max):
        message = "Error: Need matrix cannot be greater than Max matrix (Unsafe state) " # neede matrix is greater than max matrix (Unsafe state)
        return SafeSeq,[], message
    
    if np.any(Allocation < 0) or np.any(Max < 0)  or np.any(Available < 0):
        message = "Error: Allocation , Max  and Available matrices cannot have negative values" # enterd negative values
        return SafeSeq,[], message
    
    if not np.issubdtype(Allocation.dtype, np.number) or not np.issubdtype(Max.dtype, np.number): # entered non number values (characters)
        message = "Error: Allocation and Max matrices must contain only numbers"
        return SafeSeq,[], message  
   
    
    AvailableList = Available.reshape(1, -1).copy()
    flag_to_check_unsafe_sequence=0
    while True :
        for i in range(len(Need)):
            if Finish[i] ==True:
                continue
            else:
                ct=0
                for j in range(len(Need[i])):
                    if (Need[i][j] <= Available[len(Available)-1][j]) and (Need[i][j]<=Max[i][j]):
                        ct+=1
                        
                if ct == len(Need[i]):
                    for j in range(len(Need[i])):
                        Available[len(Available)-1][j] += Allocation[i][j]
                        
                    flag_to_check_unsafe_sequence=1
                    AvailableList = np.vstack([AvailableList, Available.reshape(1, -1).copy()])
                    Finish[i]=True
                    SafeSeq.append("P"+str(i))
            #print("Available",Available)
            #print("Finish",Finish)
            #print("SafeSeq",SafeSeq)
        if len(SafeSeq) == len(Finish):
            return SafeSeq,AvailableList,"done"
        if flag_to_check_unsafe_sequence==0:
            return SafeSeq,AvailableList,"No Safe Sequence Found. Deadlock possible."
        flag_to_check_unsafe_sequence=0







# GUIself.Available
class BankersAlgoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banker's Algorithm")
        self.setGeometry(100, 100, 1100, 600)

        self.num_resources = 0
        self.Allocation = []
        self.Max = []
        self.Available = []
        self.Need = []
        self.initUI()


    def initUI(self):
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()


        # this part is for the left side of the GUI

        resource_layout = QHBoxLayout()
        font=QLabel("Number of Resources:")
        font.setStyleSheet("font-size: 20px; font-weight: bold; color: black;") # Set font size and color
        resource_layout.addWidget(font)
        
        self.num_resources_spin = QSpinBox()   # SpinBox for number of resources make the number of resources dynamic
        self.num_resources_spin.setMinimum(1)
        self.num_resources_spin.setMaximum(10)
        self.num_resources_spin.setStyleSheet("font-size: 20px; font-weight: bold; color: black;") # Set font size and color
        self.num_resources_spin.valueChanged.connect(self.update_resource_inputs)
        resource_layout.addWidget(self.num_resources_spin)
        left_layout.addLayout(resource_layout)
        
        self.allocation_group = QGroupBox("Allocation")
        self.allocation_layout = QGridLayout()
        self.allocation_group.setLayout(self.allocation_layout)
        self.allocation_group.setStyleSheet("background-color: white; font-size: 20px; font-weight: bold; color: black;")
        left_layout.addWidget(self.allocation_group)

        self.max_group = QGroupBox("Max Matrix",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.max_layout = QGridLayout()
        self.max_group.setLayout(self.max_layout)
        left_layout.addWidget(self.max_group)

        self.available_group = QGroupBox("Available",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.available_layout = QGridLayout()
        self.available_group.setLayout(self.available_layout)
        left_layout.addWidget(self.available_group)

        self.alloc_add_btn = QPushButton("Add Allocation Process",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.alloc_add_btn.clicked.connect(self.add_allocation)
        left_layout.addWidget(self.alloc_add_btn)

        self.max_add_btn = QPushButton("Add Max Process",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.max_add_btn.clicked.connect(self.add_max)
        left_layout.addWidget(self.max_add_btn)

        self.calc_btn = QPushButton("Add to Available Process",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.calc_btn.clicked.connect(self.add_available)
        left_layout.addWidget(self.calc_btn)

        self.calc_btn = QPushButton("Calculate Safe Sequence",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.calc_btn.clicked.connect(self.calculate)
        left_layout.addWidget(self.calc_btn)

        

        self.clear_btn = QPushButton("Clear All",styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.clear_btn.clicked.connect(self.clear_all)
        left_layout.addWidget(self.clear_btn)

        self.request_btn = QPushButton("Make Request", styleSheet="font-size: 20px; font-weight: bold; color: black;")
        self.request_btn.clicked.connect(self.make_request)
        left_layout.addWidget(self.request_btn)















        # this part is for the right side of the GUI



        main_layout.addLayout(left_layout, 4)


        right_layout = QGridLayout()

        self.allocation_table = QTableWidget(0, 0)
        right_layout.addWidget(QLabel("Allocation Table",styleSheet="font-size: 20px; font-weight: bold; color: black;"), 0, 0)
        right_layout.addWidget(self.allocation_table, 1, 0)

        self.max_table = QTableWidget(0, 0)
        right_layout.addWidget(QLabel("Max Table",styleSheet="font-size: 20px; font-weight: bold; color: black;"), 0, 1)
        right_layout.addWidget(self.max_table, 1, 1)

        self.need_table = QTableWidget(0, 0)
        right_layout.addWidget(QLabel("Need Matrix",styleSheet="font-size: 20px; font-weight: bold; color: black;"), 2, 0)
        right_layout.addWidget(self.need_table, 3, 0)

        self.available_table = QTableWidget(1, 0)
        right_layout.addWidget(QLabel("Available",styleSheet="font-size: 20px; font-weight: bold; color: black;"), 2, 1)
        right_layout.addWidget(self.available_table, 3, 1)


        right_layout.addWidget(QLabel("Safe Sequence",styleSheet="font-size: 20px; font-weight: bold; color: black;"), 0, 2)
        self.safe_seq_text = QTextEdit()
        self.safe_seq_text.setReadOnly(True)
        right_layout.addWidget(self.safe_seq_text, 1, 2, 2, 1)

        self.status_label = QLabel("Status: Not Calculated",styleSheet="font-size: 20px; font-weight: bold; color: black;") # Set font size and color
        right_layout.addWidget(self.status_label, 3, 2)

        main_layout.addLayout(right_layout, 6)
        self.update_resource_inputs()

        main_layout.addLayout(right_layout, 4)

    # this part to update the resource inputs dynamically
    def update_resource_inputs(self):

        self.num_resources = self.num_resources_spin.value()

        def clear_layout(layout):
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

        clear_layout(self.allocation_layout)
        self.alloc_process_name = QLineEdit("P0")
        self.allocation_layout.addWidget(QLabel("Process"), 0, 0)
        self.allocation_layout.addWidget(self.alloc_process_name, 0, 1, 1, self.num_resources)

        self.alloc_resource_inputs = []
        for i in range(self.num_resources):
            self.allocation_layout.addWidget(QLabel(f"R{i+1}"), 1, i)
            le = QLineEdit()
            self.allocation_layout.addWidget(le, 2, i)
            self.alloc_resource_inputs.append(le)

        clear_layout(self.max_layout)
        self.max_resource_inputs = []
        for i in range(self.num_resources):
            self.max_layout.addWidget(QLabel(f"R{i+1}"), 0, i)
            le = QLineEdit()
            self.max_layout.addWidget(le, 1, i)
            self.max_resource_inputs.append(le)

        clear_layout(self.available_layout)
        self.available_resource_inputs = []
        for i in range(self.num_resources):
            self.available_layout.addWidget(QLabel(f"R{i+1}"), 0, i)
            le = QLineEdit()
            self.available_layout.addWidget(le, 1, i)
            self.available_resource_inputs.append(le)

        self.allocation_table.setColumnCount(self.num_resources + 1)
        self.allocation_table.setHorizontalHeaderLabels(["Process"] + [f"R{i+1}" for i in range(self.num_resources)])

        self.max_table.setColumnCount(self.num_resources)
        self.max_table.setHorizontalHeaderLabels([f"R{i+1}" for i in range(self.num_resources)])

        self.need_table.setColumnCount(self.num_resources)
        self.need_table.setHorizontalHeaderLabels([f"R{i+1}" for i in range(self.num_resources)])

        self.available_table.setColumnCount(self.num_resources)
        self.available_table.setHorizontalHeaderLabels([f"R{i+1}" for i in range(self.num_resources)])





        ## Buttons Finctionality


    def add_allocation(self):
        
        values = []
        for le in self.alloc_resource_inputs:
            try:
                val = int(le.text())
            except ValueError:
                self.show_error("Enter valid integers for Allocation resources.")
                return
            if val < 0:
                self.show_error("Enter valid non-negative integers for Allocation resources.")
                return
            else:
                values.append(val)
                
        process_name = self.alloc_process_name.text().strip()
        if not process_name:
            self.show_error("Process name cannot be empty.")
            return


        self.Allocation.append(values)

        row_pos = self.allocation_table.rowCount()
        self.allocation_table.insertRow(row_pos)
        self.allocation_table.setItem(row_pos, 0, QTableWidgetItem(process_name))
        for i, val in enumerate(values):
            self.allocation_table.setItem(row_pos, i + 1, QTableWidgetItem(str(val)))

        try:
            idx = int(process_name.strip("P"))
            self.alloc_process_name.setText(f"P{idx + 1}")
        except:
            self.alloc_process_name.setText(f"P{row_pos + 1}")

        for le in self.alloc_resource_inputs:
            le.clear()

    def add_max(self):
       
        values = []
            
        for le in self.max_resource_inputs:
            
            try:
                val = int(le.text())
            except ValueError:
                self.show_error("Enter valid non-negative integers for Max resources.")
                return

            if val < 0:
                self.show_error("Enter valid non-negative integers for Max resources.")
                return

            values.append(val)

        self.Max.append(values)
        row_pos = self.max_table.rowCount()
        self.max_table.insertRow(row_pos)
        for i, val in enumerate(values):
            self.max_table.setItem(row_pos, i, QTableWidgetItem(str(val)))

        for le in self.max_resource_inputs:
            le.clear()

    def add_available(self):
        values = []
        for le in self.available_resource_inputs:
            try:
                val = int(le.text())
            except ValueError:
                self.show_error("Enter valid non-negative integers for Available resources.")
                return
            if val < 0:
                self.show_error("Enter valid non-negative integers for Available resources.")
                return
            else:
                values.append(val)

        self.Available.append(values)
        row_pos = self.available_table.rowCount()
        self.available_table.insertRow(row_pos)
        for i, val in enumerate(values):
            self.available_table.setItem(row_pos, i, QTableWidgetItem(str(val)))

       
    

    def calculate(self):
        avaliablelist = []
        self.Need = [
            [self.Max[i][j] - self.Allocation[i][j] for j in range(len(self.Max[0]))]
             for i in range(len(self.Max))
        ]

        result,AvailableList,text = BankerLogic(self,self.Allocation, self.Max, self.Available.copy())
        if text == "No Safe Sequence Found. Deadlock possible.":
            self.safe_seq_text.setText(text)
            self.status_label.setText("Status: Not Safe")
            return
        if isinstance(result, str):
            self.safe_seq_text.setText(result)
            self.status_label.setText("Status: Not Safe")
        else:
            self.safe_seq_text.setText(" -> ".join(result))
            self.status_label.setText("Status: Safe")
            # Show Need matrix
            need = np.array(self.Max) - np.array(self.Allocation)
            self.need_table.setRowCount(len(need))
            for i in range(len(need)):
                for j in range(self.num_resources):
                    self.need_table.setItem(i, j, QTableWidgetItem(str(need[i][j])))
            # Show updated Available
            for j in range(self.num_resources):
                self.available_table.setItem(0, j, QTableWidgetItem(str(self.Available[0][j])))
                #self.add2_available(availablelist=avaliablelist)
        num_rows, num_cols = AvailableList.shape
        self.available_table.setRowCount(num_rows)
        self.available_table.setColumnCount(num_cols)

        for i in range(num_rows):
            for j in range(num_cols):
                item = QTableWidgetItem(str(AvailableList[i][j]))
                self.available_table.setItem(i, j, item)
    
    def append_available_to_table(self, available_row):
        row_pos = self.available_table.rowCount()
        self.available_table.insertRow(row_pos)
        for i, val in enumerate(available_row):
            self.available_table.setItem(row_pos, i, QTableWidgetItem(str(val)))


    def make_request(self):
        dialog = RequestDialog(self.num_resources, self)
        if dialog.exec_() == QDialog.Accepted:
            process_index = dialog.process_id
            request = dialog.request
            need = np.array(self.Max[process_index]) - np.array(self.Allocation[process_index])

            
            if np.any(request > need):
                message = "Error: Request exceeds the process's remaining Need"
            else:
                
                message = "Request can be granted"
                # Update Allocation and Available matrices
                #message ="process index"+str(process_index)+"request"+str(request)
                self.Allocation[process_index] = [self.Allocation[process_index][i] + request[i] for i in range(self.num_resources)]
                
                for i in range(self.num_resources):
                        self.Available[0][i] -= request[i]
                        #essage ="Before calculation Need= "+str(self.Need[i])+"Allocation= "+str(self.Allocation[i])+"Available= "+str(self.Available[0])
                self.Need[process_index] = [self.Need[process_index][i] - request[i] for i in range(self.num_resources)]
                # Update tables
                #self.allocation_table.setRowCount(0)
                #self.max_table.setRowCount(0)
                #self.need_table.setRowCount(0)
                #self.available_table.setRowCount(0) 
                #BankerLogic(self,self.Allocation, self.Max, self.Available.copy())
                #message ="Before calculation Need= "+str(self.Need[process_index])+"Allocation= "+str(self.Allocation[process_index])+"Available= "+str(self.Available[0])
                
                self.calculate()
                
                

        
        

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)   
        msg.setText("Request Result")
        
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
            

    
        

        


    def clear_all(self):
        # Example logic to clear fields, tables, etc.
        self.alloc_process_name.clear()
        for le in self.alloc_resource_inputs:
            le.clear()
        for le in self.max_resource_inputs:
            le.clear()
        for le in self.available_resource_inputs:
            le.clear()

        self.allocation_table.setRowCount(0)
        self.max_table.setRowCount(0)
        self.Allocation.clear()
        self.Max.clear()
        self.available_table.setRowCount(0)
        self.Available.clear()
        self.need_table.setRowCount(0)
        self.need_table.clear()
        self.safe_seq_text.clear()




    def show_error(self, message):
        QMessageBox.critical(self, "Input Error", message)
        self.status_label.setText("Status: Not Calculated")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankersAlgoGUI()
    window.show()
    sys.exit(app.exec_())





