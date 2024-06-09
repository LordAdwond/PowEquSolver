import sys
import pyqtgraph as pq
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QComboBox, QApplication
from solver import solver


class MainWidget(QWidget):
    def __init__(self):
        super().__init__(None)

        # widgets
        self.b_line = QLineEdit()
        self.c_line = QLineEdit()
        self.d_line = QLineEdit()
        self.e_line = QLineEdit()

        self.solve_text = QTextEdit()
        self.graph = pq.PlotWidget()
        self.line = self.graph.plot()

        self.solves_types_combo = QComboBox()
        self.equation_power_combo = QComboBox()

        # main layout
        main_layout = QGridLayout()
        main_layout.cellRect(3, 10)

        main_layout.addWidget(self.solves_types_combo, 0, 0)
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

        main_layout.addWidget(self.solve_text, 2, 0, 1, 9)
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
        self.solves_types_combo.addItems([
            "only real solves",
            "only complex solves",
            "all solves"
        ])
        self.solves_types_combo.setCurrentIndex(2)

        self.solve_text.setStyleSheet("background-color: green; font-style: bold")
        self.solve_text.setReadOnly(True)

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
            self.solve_text.setText("")
            a, b, c, d, e = self.form_coefs()

            res = []
            if self.equation_power_combo.currentIndex() == 0:
                res = solver.solve_linear(d, e)
            elif self.equation_power_combo.currentIndex() == 1:
                res = solver.solve_quadratic(d, e)
            elif self.equation_power_combo.currentIndex() == 2:
                res = solver.solve_cubic(c, d, e)
            elif self.equation_power_combo.currentIndex() == 3:
                res = solver.solve_forth(b, c, d, e)

            res_str = ""
            for solve in res:
                if self.solves_types_combo.currentIndex() == 0:
                    if str(type(solve)) == "<class 'numpy.float64'>":
                        res_str += str(solve) + '\n'
                    else:
                        continue
                elif self.solves_types_combo.currentIndex() == 1:
                    if str(type(solve)) == "<class 'complex'>":
                        res_str += str(solve) + '\n'
                    else:
                        continue
                elif self.solves_types_combo.currentIndex() == 2:
                    res_str += str(solve) + '\n'

            self.solve_text.setText(res_str)

        except Exception:
            self.solve_text.setText(f"Invalid input")

    def plot_it(self):
        try:
            self.solve_text.setText("")
            self.line.clear()
            a, b, c, d, e = self.form_coefs()

            x = np.linspace(-20, 20, 500)
            y = a * np.power(x, 4) + b * np.power(x, 3) + c * np.power(x, 2) + d * x + e
            self.line = self.graph.plot(x, y)

        except Exception:
            self.solve_text.setText(f"Invalid input")

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
        else:
            b = float(self.b_line.text()) if len(self.b_line.text()) > 0 else 0

        # c
        if self.equation_power_combo.currentIndex() == 1:
            c = 1
        if self.equation_power_combo.currentIndex() < 1:
            c = 0
        else:
            c = float(self.c_line.text()) if len(self.c_line.text()) > 0 else 0

        # d and e
        d = 0 if len(self.d_line.text()) == 0 else float(self.d_line.text())
        e = 0 if len(self.e_line.text()) == 0 else float(self.e_line.text())

        return a, b, c, d, e


app = QApplication(sys.argv)
win = MainWidget()
win.show()
app.exec()
