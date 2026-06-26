"""Game grid widget for rendering and interacting with the simulation board."""

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QMouseEvent

from Game.GameInstance import GameInstance


class GameGrid(QWidget):
    """Interactive square grid widget backed by a :class:`GameInstance`.

    The widget maintains square geometry in layouts, renders one rectangle per
    simulation cell, and exposes a click callback hook for cell interactions.
    """
    
    def __init__(self, parent=None):
        """Initialize the game grid widget.

        Args:
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self.game_instance = GameInstance(starting_cells=[(5, 5), (5, 4), (5, 3)])
        self.cell_rects = []
        self.setup_ui()

    def setup_ui(self):
        """Configure base visual behavior and layout policy."""
        self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def hasHeightForWidth(self):
        """Tell Qt this widget should keep a square aspect ratio.

        Returns:
            bool: Always ``True`` so layout height follows width.
        """
        return True

    def heightForWidth(self, width):
        """Return a height matching the provided width.

        Args:
            width: Proposed widget width from the layout system.

        Returns:
            int: Height that keeps the widget square.
        """
        return width

    def sizeHint(self):
        """Provide a preferred starting size for the widget.

        Returns:
            QSize: Preferred square size.
        """
        return QSize(500, 500)

    def step_game(self):
        """Advance the simulation by one generation and repaint the widget."""
        self.game_instance.step()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse clicks and map them to a grid cell.

        Args:
            event: Mouse press event containing click coordinates.
        """
        click_pos = event.position().toPoint()
        # Resolve the clicked board cell from cached paint rectangles.
        for row_index, row_rects in enumerate(self.cell_rects):
            for col_index, cell_rect in enumerate(row_rects):
                if cell_rect.contains(click_pos):
                    self.on_grid_clicked(row_index, col_index)
                    return
        super().mousePressEvent(event)

    def on_grid_clicked(self, row: int, col: int):
        """Placeholder click handler for custom interaction behavior.

        Args:
            row: Zero-based row index of the clicked cell.
            col: Zero-based column index of the clicked cell.
        """
        self.game_instance.flip_cell(row, col)
        self.update()

    def paintEvent(self, event):
        """Paint a square board using one rectangle per simulation cell.

        Args:
            event: Qt paint event.
        """
        super().paintEvent(event)

        painter = QPainter(self)
        grid_size = max(1, int(self.game_instance.grid_size))

        # Use the largest centered square that fits inside the widget.
        side = min(self.width(), self.height()) - 2
        if side <= 0:
            self.cell_rects = []
            return

        offset_x = (self.width() - side) // 2
        offset_y = (self.height() - side) // 2
        left = offset_x
        top = offset_y

        # Cell borders are drawn as rectangles so each cell can be reused/fillable.
        painter.setPen(QPen(QColor("white"), 2))
        self.cell_rects = []
        game_state = self.game_instance.get_game_board()

        # Build exact cell rectangles that tile the square drawing area.
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
                # Fill live cells from the current game state tensor.
                if game_state[row][col]:
                    painter.fillRect(rect, QBrush(QColor("black")))
            self.cell_rects.append(row_rects)

        # Draw board guidelines on top for clearer cell boundaries.
        for idx in range(grid_size + 1):
            x0 = left + int(round(idx * side / grid_size))
            y0 = top + int(round(idx * side / grid_size))
            painter.setPen(QPen(QColor("grey"), 2))
            painter.drawLine(0, y0, side, y0)
            painter.drawLine(x0, 0,  x0, side)
