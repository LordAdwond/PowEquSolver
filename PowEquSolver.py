import sys
import pyqtgraph as pq
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QComboBox, QApplication
from solver import solver
from processing import processing


class MainWidget(QWidget):
    def __init__(self):
        super().__init__(None)

        # widgets
        self.b_line = QLineEdit()
        self.c_line = QLineEdit()
        self.d_line = QLineEdit()
        self.e_line = QLineEdit()

        self.real_roots_text = QTextEdit()
        self.complex_roots_text = QTextEdit()
        self.graph = pq.PlotWidget()
        self.line = self.graph.plot()

        self.equation_power_combo = QComboBox()

        # main layout
        main_layout = QGridLayout()
        solve_layout = QGridLayout()
        main_layout.cellRect(4, 10)
        solve_layout.cellRect(2, 2)

        main_layout.addWidget(QLabel("Equation's power"), 0, 0)
        main_layout.addWidget(self.equation_power_combo, 0, 1)

        main_layout.addWidget(QLabel("x^4+"), 1, 0)
        main_layout.addWidget(self.b_line, 1, 1)
        main_layout.addWidget(QLabel("x^3+"), 1, 2)
        main_layout.addWidget(self.c_line, 1, 3)
        main_layout.addWidget(QLabel("x^2+"), 1, 4)
        main_layout.addWidget(self.d_line, 1, 5)
        main_layout.addWidget(QLabel("x+"), 1, 6)
        main_layout.addWidget(self.e_line, 1, 7)
        main_layout.addWidget(QLabel("=0"), 1, 8)

        solve_layout.addWidget(QLabel("Real roots"), 0, 0)
        solve_layout.addWidget(self.real_roots_text, 1, 0)
        solve_layout.addWidget(QLabel("Complex roots"), 0, 1)
        solve_layout.addWidget(self.complex_roots_text, 1, 1)
        main_layout.addLayout(solve_layout, 2, 0, 2, 9)

        main_layout.addWidget(self.graph, 0, 9, 3, 1)

        self.setLayout(main_layout)

        # connections
        self.equation_power_combo.currentIndexChanged.connect(self.update_ui)
        self.b_line.textChanged.connect(self.plot_it)
        self.b_line.textChanged.connect(self.solve_equation)
        self.c_line.textChanged.connect(self.plot_it)
        self.c_line.textChanged.connect(self.solve_equation)
        self.d_line.textChanged.connect(self.plot_it)
        self.d_line.textChanged.connect(self.solve_equation)
        self.e_line.textChanged.connect(self.plot_it)
        self.e_line.textChanged.connect(self.solve_equation)

        # settings
        self.equation_power_combo.addItems([str(p) for p in range(1, 5)])
        self.equation_power_combo.setCurrentIndex(0)

        self.real_roots_text.setStyleSheet("background-color: #209950; color : #250060; font-weight: bold; font-size: 15px;")
        self.complex_roots_text.setStyleSheet("background-color: #209950; color : #250060; font-weight: bold; font-size: 15px;")
        self.real_roots_text.setReadOnly(True)
        self.complex_roots_text.setReadOnly(True)

        self.graph.setFixedSize(self.size().height(), self.size().height())
        self.setWindowTitle("PowEquSolver - Power Equations solver")
        self.setFixedSize(int(1.1*(self.size().width()+self.size().height())), int(1.1*self.size().height()))

    def update_ui(self):
        if self.equation_power_combo.currentIndex() == 0 or self.equation_power_combo.currentIndex() == 1:
            self.b_line.setDisabled(True)
            self.c_line.setDisabled(True)
            self.d_line.setEnabled(True)
            self.e_line.setEnabled(True)
        elif self.equation_power_combo.currentIndex() == 2:
            self.b_line.setDisabled(True)
            self.c_line.setEnabled(True)
            self.d_line.setEnabled(True)
            self.e_line.setEnabled(True)
        elif self.equation_power_combo.currentIndex() == 3:
            self.b_line.setEnabled(True)
            self.c_line.setEnabled(True)
            self.d_line.setEnabled(True)
            self.e_line.setEnabled(True)

        self.b_line.setText("")
        self.c_line.setText("")
        self.d_line.setText("")
        self.e_line.setText("")

    def solve_equation(self):
        try:
            a, b, c, d, e = self.form_coefs()

            res = {"real":[], "complex":[]}
            if self.equation_power_combo.currentIndex() == 0:
                res["real"] = res["real"] + solver.solve_linear(d, e)
            elif self.equation_power_combo.currentIndex() == 1:
                res["real"] = res["real"] + solver.solve_quadratic(d, e)["real"]
                res["complex"] = res["complex"] + solver.solve_quadratic(d, e)["complex"]
            elif self.equation_power_combo.currentIndex() == 2:
                res["real"] = res["real"] + solver.solve_cubic(c, d, e)["real"]
                res["complex"] = res["complex"] + solver.solve_cubic(c, d, e)["complex"]
            elif self.equation_power_combo.currentIndex() == 3:
                res["real"] = res["real"] + solver.solve_forth(b, c, d, e)["real"]
                res["complex"] = res["complex"] + solver.solve_forth(b, c, d, e)["complex"]

            real_res_str = ""
            complex_res_str = ""
            for root in res["real"]:
                real_res_str += str(root) + '\n'
            for root in res["complex"]:
                complex_res_str += str(root) + '\n'

            self.real_roots_text.setText(real_res_str)
            self.complex_roots_text.setText(complex_res_str)


        except Exception:
            self.real_roots_text.setText("Invalid input")
            self.complex_roots_text.setText("Invalid input")

    def plot_it(self):
        try:
            self.line.clear()
            a, b, c, d, e = self.form_coefs()

            x = np.linspace(-20, 20, 500)
            y = a * np.power(x, 4) + b * np.power(x, 3) + c * np.power(x, 2) + d * x + e
            self.line = self.graph.plot(x, y)

        except Exception:
            self.real_roots_text.setText("Invalid input")
            self.complex_roots_text.setText("Invalid input")

    def form_coefs(self):
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0

        # a
        if self.equation_power_combo.currentIndex() == 3:
            a = 1.0
        else:
            a = 0
        # b
        if self.equation_power_combo.currentIndex() == 2:
            b = 1
        if self.equation_power_combo.currentIndex() < 2:
            b = 0
        if self.equation_power_combo.currentIndex() > 2:
            if self.b_line.text().isnumeric():
                # b = float(self.b_line.text())
                b = processing.from_string(self.b_line.text())
            else:
                b = 0

        # c
        if self.equation_power_combo.currentIndex() == 1:
            c = 1
        if self.equation_power_combo.currentIndex() < 1:
            c = 0
        if self.equation_power_combo.currentIndex() > 1:
            if self.c_line.text().isnumeric():
                # c = float(self.c_line.text())
                c = processing.from_string(self.c_line.text())
            else:
                c = 0

        # d and e
        # d = 0 if len(self.d_line.text()) == 0 else float(self.d_line.text())
        # e = 0 if len(self.e_line.text()) == 0 else float(self.e_line.text())
        d = 0 if len(self.d_line.text()) == 0 else processing.from_string(self.d_line.text())
        e = 0 if len(self.e_line.text()) == 0 else processing.from_string(self.e_line.text())

        return a, b, c, d, e


app = QApplication(sys.argv)
win = MainWidget()
win.show()
app.exec()
