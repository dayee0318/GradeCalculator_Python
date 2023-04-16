from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, \
    QGridLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ScoreCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.tasks = []
        self.total_weight = 0

        self.init_ui()

        self.show()

    def init_ui(self):
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.grid = QGridLayout()

        self.grid.addWidget(QLabel("TASK"), 0, 0)
        self.grid.addWidget(QLabel("Weight (%)"), 0, 1)
        self.grid.addWidget(QLabel("Score Received"), 0, 2)
        self.grid.addWidget(QLabel("Full Score"), 0, 3)
        self.grid.addWidget(QLabel("Task Percentage"), 0, 4)

        self.add_task_button = QPushButton("+ Add Task")
        self.add_task_button.clicked.connect(self.add_task)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_score)

        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 20, QFont.Bold))

        self.setLayout(self.grid)

        self.setGeometry(500, 500, 600, 200)
        self.setWindowTitle("Score Calculator")

        self.add_task()

    def add_task(self):
        task_num = len(self.tasks) + 1

        task_label = QLabel(f"Task {task_num}:")
        weight_edit = QLineEdit()
        score_edit = QLineEdit()
        max_score_edit = QLineEdit()
        task_percentage_label = QLabel()
        task_percentage_label.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(12)
        task_percentage_label.setFont(font)

        self.grid.addWidget(task_label, task_num, 0)
        self.grid.addWidget(weight_edit, task_num, 1)
        self.grid.addWidget(score_edit, task_num, 2)
        self.grid.addWidget(max_score_edit, task_num, 3)
        self.grid.addWidget(task_percentage_label, task_num, 4)

        self.tasks.append({
            "weight_edit": weight_edit,
            "score_edit": score_edit,
            "max_score_edit": max_score_edit,
            "task_percentage_label": task_percentage_label
        })

        task_row = task_num + 1
        self.grid.addWidget(self.add_task_button, task_row, 1, 1, 3)
        self.grid.addWidget(self.calculate_button, task_row + 1, 1)
        self.grid.addWidget(self.result_label, task_row + 1, 2)
        self.grid.addWidget(self.clear_all_button, task_row + 1, 3)

    def calculate_score(self):
        self.total_weight = 0
        total_score = 0

        for i, task in enumerate(self.tasks):
            weight_str = task["weight_edit"].text()
            score_str = task["score_edit"].text()
            max_score_str = task["max_score_edit"].text()

            if weight_str == "" or score_str == "" or max_score_str == "":
                self.result_label.setText("Error: Input required")
                self.result_label.setStyleSheet("color: red")
                return

            try:
                weight = float(weight_str)
                score = float(score_str)
                max_score = float(max_score_str)
            except ValueError:
                self.result_label.setText("Error: Invalid input")
                self.result_label.setStyleSheet("color: red")
                return

            self.total_weight += weight
            task_percentage = (score / max_score) * 100
            task["task_percentage_label"].setText(f"{task_percentage:.2f}%")
            task["task_percentage_label"].setStyleSheet("color: blue")

            total_score += weight * (score / max_score)

        if self.total_weight != 100:
            self.result_label.setText("Error: Total weight must be 100")
            self.result_label.setStyleSheet("color: red")
            return

        self.result_label.setText(f"{total_score:.2f}")
        self.result_label.setStyleSheet("color: red")

    def clear_all(self):
        for task in self.tasks:
            task["weight_edit"].clear()
            task["score_edit"].clear()
            task["max_score_edit"].clear()
            task["task_percentage_label"].clear()

        self.result_label.clear()

if __name__ == "__main__":
    app = QApplication([])
    calculator = ScoreCalculator()
    app.exec_()

