import random
import os

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'

class MineSweeperGame:
    def __init__(self, size=10, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mines = set()
        self.revealed = set()
        self.place_mines()

    def place_mines(self):
        while len(self.mines) < self.num_mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (x + dx, y + dy) in self.mines:
                    count += 1
        return count

    def reveal(self, x, y):
        if (x, y) in self.revealed:
            return True

        self.revealed.add((x, y))

        if (x, y) in self.mines:
            return False

        if self.count_adjacent_mines(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal(nx, ny)

        return True

    def display_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(f"{i} ", end="")
            for j in range(self.size):
                if (i, j) in self.revealed:
                    if (i, j) in self.mines:
                        print(f"{Colors.RED}* {Colors.RESET}", end="")
                    else:
                        count = self.count_adjacent_mines(i, j)
                        if count == 0:
                            print(f"{Colors.GREEN}  {Colors.RESET}", end="")
                        else:
                            print(f"{Colors.BLUE}{count} {Colors.RESET}", end="")
                else:
                    print(f"{Colors.YELLOW}- {Colors.RESET}", end="")
            print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game():
    game = MineSweeperGame()
    game_over = False

    while not game_over:
        clear_screen()
        print(f"{Colors.GREEN}Mine Sweeper{Colors.RESET}")
        print(f"Mines: {game.num_mines}")
        print(f"Revealed: {len(game.revealed)} / {game.size * game.size - game.num_mines}")
        print()
        game.display_board()
        print("\nEnter 'q' to quit the game.")
        try:
            move = input("Enter row and column (e.g., '3 4'): ")
            if move.lower() == 'q':
                print("Thanks for playing!")
                return

            x, y = map(int, move.split())
            if not (0 <= x < game.size and 0 <= y < game.size):
                raise ValueError
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter two numbers between 0 and 9, separated by a space.{Colors.RESET}")
            input("Press Enter to continue...")
            continue

        if not game.reveal(x, y):
            clear_screen()
            game.display_board()
            print(f"\n{Colors.RED}Game Over! You hit a mine.{Colors.RESET}")
            game_over = True
        elif len(game.revealed) + len(game.mines) == game.size * game.size:
            clear_screen()
            game.display_board()
            print(f"\n{Colors.GREEN}Congratulations! You've won!{Colors.RESET}")
            game_over = True

    play_again = input("Do you want to play again? (y/n): ")
    if play_again.lower() == 'y':
        play_game()

if __name__ == "__main__":
    clear_screen()
    print(f"{Colors.GREEN}Welcome to Mine Sweeper!{Colors.RESET}")
    print("\nInstructions:")
    print("1. Enter the row and column numbers to reveal a cell.")
    print("2. Numbers indicate the count of adjacent mines.")
    print("3. Avoid revealing mines to win the game.")
    print("\nGood luck!")
    input("\nPress Enter to start the game...")
    play_game()
