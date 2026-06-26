"""
Game grid widget implementation.
"""

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QBrush

from Game.GameInstance import GameInstance


class GameGrid(QWidget):
    """A game grid widget with a black border outline."""
    
    def __init__(self, parent=None):
        """Initialize the game grid widget."""
        super().__init__(parent)
        self.game_instance = GameInstance(starting_cells = [(5, 5), (5, 4), (5, 3)])
        self.cell_rects = []
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components."""
        self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def hasHeightForWidth(self):
        """Tell Qt this widget should keep a square aspect ratio."""
        return True

    def heightForWidth(self, width):
        """Match height to width so the widget stays square in layouts."""
        return width

    def sizeHint(self):
        """Preferred square size."""
        return QSize(500, 500)

    def step_game(self):
        self.game_instance.step()
        self.update()

    def paintEvent(self, event):
        """Paint the grid as per-cell rectangles and cache those rectangles."""
        super().paintEvent(event)

        painter = QPainter(self)
        grid_size = max(1, int(self.game_instance.grid_size))

        # Use the largest centered square that fits in the current widget bounds.
        side = min(self.width(), self.height()) - 2
        if side <= 0:
            self.cell_rects = []
            return

        offset_x = (self.width() - side) // 2
        offset_y = (self.height() - side) // 2
        left = offset_x
        top = offset_y

        painter.setPen(QPen(QColor("white"), 2))
        self.cell_rects = []
        game_state = self.game_instance.get_game_board()

        # Build exact cell rectangles that tile the square area.
        for row in range(grid_size):
            row_rects = []
            y0 = top + int(round(row * side / grid_size))
            y1 = top + int(round((row + 1) * side / grid_size))

            for col in range(grid_size):
                x0 = left + int(round(col * side / grid_size))
                x1 = left + int(round((col + 1) * side / grid_size))

                rect = QRect(x0, y0, max(1, x1 - x0), max(1, y1 - y0))
                row_rects.append(rect)
                painter.drawRect(rect)
                if game_state[row][col]:
                    painter.fillRect(rect, QBrush(QColor("black")))
            self.cell_rects.append(row_rects)


        for idx in range(grid_size + 1):
            x0 = left + int(round(idx * side / grid_size))
            y0 = top + int(round(idx * side / grid_size))
            painter.setPen(QPen(QColor("grey"), 2))
            painter.drawLine(0, y0, side, y0)
            painter.drawLine(x0, 0,  x0, side)
