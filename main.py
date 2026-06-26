from GameInstance import GameInstance
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    game_board = GameInstance(starting_cells = [(5, 5), (5, 4), (5, 3)])
    while True:
        print(game_board.get_game_board())
        input("Press enter to step")
        game_board.step()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

