"""Conway's Game of Life simulator using PyTorch convolutions.

This module implements a customizable variant of Conway's Game of Life where
birth and survival rules can be specified as lists of neighbor counts.
"""

import torch
import torch.nn.functional as F
from coordinates import Coordinate


class GameInstance:
    """
    A configurable implementation of Conway's Game of Life using PyTorch.
    
    Uses 2D convolution to efficiently compute neighbor counts for all cells,
    then applies custom birth and survival rules to evolve the game state.
    """
    def __init__(
        self,
        allow_birth: list[int] = None,
        allow_survival: list[int] = None,
        grid_height: int = 10,
        grid_width: int = 10,
        starting_cells: list[tuple[int, int]] = None,
    ):
        """
        Initialize a Game of Life instance with custom rules and starting state.
        
        Args:
            allow_birth: List of neighbor counts that allow dead cells to be born.
                        Defaults to [3] (standard Game of Life).
            allow_survival: List of neighbor counts that allow live cells to survive.
                           Defaults to [2, 3] (standard Game of Life).
            grid_height: Height of the game board. Defaults to 10.
            grid_width: Width of the game board. Defaults to 10.
            starting_cells: List of (x, y) tuples for initially live cells.
        
        Raises:
            ValueError: If starting cells are out of bounds or if any neighbor count > 8.
        """
        
        # 3x3 convolution kernel for counting neighbors (center cell excluded)
        self.kernel = torch.tensor(
            [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
            dtype=torch.int32,
            requires_grad=False,
        ).unsqueeze(0).unsqueeze(0)

        self.grid_height = grid_height
        self.grid_width = grid_width

        # Validate starting cells are within bounds
        for coord in starting_cells:
            if coord[0] < 0 or coord[0] >= self.grid_width:
                raise ValueError(
                    f"Invalid starting cell, x coordinate: {coord[0]} "
                    f"is not in range [0, {self.grid_width - 1}]"
                )
            if coord[1] < 0 or coord[1] >= self.grid_width:
                raise ValueError(
                    f"Invalid starting cell, y coordinate: {coord[1]} "
                    f"is not in range [0, {self.grid_width - 1}]"
                )

        # Initialize game board with zeros and set starting cells to 1
        self.game_board = torch.tensor(
            torch.zeros(grid_height, grid_width),
            dtype=torch.int32,
            requires_grad=False,
        )
        for x, y in starting_cells:
            self.game_board[x, y] = 1

        # Set default birth rule or validate user-provided rule
        if allow_birth is None:
            self.allow_birth = [3]
        else:
            for i in allow_birth:
                if i > 8:
                    raise ValueError("Cannot have more than 8 neighbours")
            self.allow_birth = allow_birth

        # Create boolean tensor mapping neighbor count to birth permission
        self.birth_rule = torch.zeros(9, dtype=torch.bool)
        self.birth_rule[self.allow_birth] = True

        # Set default survival rule or validate user-provided rule
        if allow_survival is None:
            self.allow_survival = [2, 3]
        else:
            for i in allow_survival:
                if i > 8:
                    raise ValueError("Cannot have more than 8 neighbours")
            self.allow_survival = allow_survival

        # Create boolean tensor mapping neighbor count to survival permission
        self.survival_rule = torch.zeros(9, dtype=torch.bool)
        self.survival_rule[self.allow_survival] = True

    def step(self):
        """
        Execute one iteration of the game by applying birth and survival rules.
        
        Uses 2D convolution to compute neighbor counts for each cell, then applies
        the birth and survival rules to determine the next generation state.
        """
        # Add batch and channel dimensions for conv2d: (1, 1, height, width)
        board_4d = self.game_board.unsqueeze(0).unsqueeze(0)
        
        # Convolve with kernel to get neighbor counts for each cell
        neighbor_counts = F.conv2d(board_4d, self.kernel, padding=1).squeeze(0).squeeze(0)
        
        # Dead cells become alive if neighbor count is in birth_rule
        born = self.birth_rule[neighbor_counts]
        
        # Live cells survive if neighbor count is in survival_rule
        survive = self.game_board & (self.survival_rule[neighbor_counts])
        
        # Update board: cells that are born OR survive remain alive
        self.game_board = (born | survive)

    def get_game_board(self):
        """
        Retrieve the current state of the game board.
        
        Returns:
            torch.Tensor: A 2D tensor of shape (grid_height, grid_width) with values
                         1 for live cells and 0 for dead cells.
        """
        return self.game_board.squeeze()