import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def make_move(self, board):
        while True:
            try:
                cell_num = int(input(f"{self.name}, enter a cell number (1-9): "))
                if 1 <= cell_num <= 9:
                    if board.update_cell(cell_num, self.symbol):
                        break
                    else:
                        print("Cell already taken. Try again.")
                else:
                    print("Invalid cell number. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def setup_players(self):
        for player_number, player in enumerate(self.players, start=1):
            print(f"Player {player_number} enter your name and symbol :")
            player.player_name()
            player.player_symbol()
            clear_screen()

class Board:
    def __init__(self):
        # Initialize a 3x3 board with empty spaces
        self.cells = [" " for _ in range(9)]

    # Display the board
    def display(self):
        print("\n")
        for row in [self.cells[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
        print("\n")

    # Update a cell on the board
    def update_cell(self, cell_num, symbol):
        if self.cells[cell_num - 1] == " ":
            self.cells[cell_num - 1] = symbol
            return True
        return False

    # Check if the current player has won
    def is_winner(self, symbol):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in winning_combinations:
            if all(self.cells[i] == symbol for i in combo):
                return True
        return False

    # Check if the game is a tie
    def is_tie(self):
        return " " not in self.cells


class Menu:
    @staticmethod
    def display_welcome_message():
        print("Welcome to Tic-Tac-Toe!")

    @staticmethod
    def get_player_info(player_number, other_symbol=None):
        name = input(f"Enter the name for Player {player_number}: ").strip()
        while True:
            symbol = input(f"{name}, choose your symbol (X or O): ").strip().upper()
            if symbol in ["X", "O"]:
                if other_symbol and symbol == other_symbol:
                    print(f"Symbol '{symbol}' is already taken by the other player. Please choose a different symbol.")
                else:
                    return name, symbol
            else:
                print("Invalid symbol. Please choose 'X' or 'O'.")

    @staticmethod
    def display_winner(player):
        print(f"{player.name} ({player.symbol}) wins!")

    @staticmethod
    def display_tie():
        print("It's a tie!")

    @staticmethod
    def ask_replay():
        return input("Do you want to play again? (yes/no): ").strip().lower() == "yes"


class Game:
    def __init__(self):
        self.board = Board()
        name1, symbol1 = Menu.get_player_info(1)
        # Pass symbol1 to prevent duplicates
        name2, symbol2 = Menu.get_player_info(2, symbol1)  
        self.player1 = Player(name1, symbol1)
        self.player2 = Player(name2, symbol2)
        self.current_player = self.player1

    # Switch between players
    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play(self):
        Menu.display_welcome_message()
        self.board.display()

        while True:
            self.current_player.make_move(self.board)
            self.board.display()

            if self.board.is_winner(self.current_player.symbol):
                Menu.display_winner(self.current_player)
                break
            elif self.board.is_tie():
                Menu.display_tie()
                break

            self.switch_player()

# Main program
if __name__ == "__main__":
    while True:
        game = Game()
        game.play()
        if not Menu.ask_replay():
            print("Thanks for playing! See you soon")
            break