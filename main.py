from Game.GameInstance import GameInstance

def main():
    game_board = GameInstance(starting_cells = [(5, 5), (5, 4), (5, 3)])
    while True:
        print(game_board.get_game_board())
        input("Press enter to step")
        game_board.step()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

