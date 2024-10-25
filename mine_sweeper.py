import random
import os

# 定义终端输出的颜色代码
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'

class MineSweeperGame:
    def __init__(self, size=10, num_mines=10):
        """
        初始化扫雷游戏。
        :param size: 游戏板的大小（默认：10x10）
        :param num_mines: 要放置在游戏板上的地雷数量（默认：10）
        """
        self.size = size
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mines = set()
        self.revealed = set()
        self.place_mines()

    def place_mines(self):
        """随机在游戏板上放置地雷。"""
        while len(self.mines) < self.num_mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))

    def count_adjacent_mines(self, x, y):
        """
        计算给定单元格周围的地雷数量。
        :param x: 行索引
        :param y: 列索引
        :return: 相邻地雷的数量
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (x + dx, y + dy) in self.mines:
                    count += 1
        return count

    def reveal(self, x, y):
        """
        揭示一个单元格，如果它是空的，则揭示其邻居。
        :param x: 行索引
        :param y: 列索引
        :return: 如果揭示成功则返回True，如果揭示了地雷则返回False
        """
        if (x, y) in self.revealed:
            return True

        self.revealed.add((x, y))

        if (x, y) in self.mines:
            return False

        # 如果单元格周围没有地雷，揭示其邻居
        if self.count_adjacent_mines(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal(nx, ny)

        return True

    def display_board(self):
        """显示游戏板的当前状态。"""
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
    """清除终端屏幕。"""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game():
    """扫雷游戏的主循环。"""
    game = MineSweeperGame()
    game_over = False

    while not game_over:
        clear_screen()
        print(f"{Colors.GREEN}扫雷游戏{Colors.RESET}")
        print(f"地雷数量: {game.num_mines}")
        print(f"已揭示: {len(game.revealed)} / {game.size * game.size - game.num_mines}")
        print()
        game.display_board()
        print("\n输入'q'退出游戏。")
        try:
            move = input("输入行和列（例如，'3 4'）: ")
            if move.lower() == 'q':
                print("感谢您的游戏！")
                return

            x, y = map(int, move.split())
            if not (0 <= x < game.size and 0 <= y < game.size):
                raise ValueError
        except ValueError:
            print(f"{Colors.RED}无效输入。请输入两个0到9之间的数字，用空格分隔。{Colors.RESET}")
            input("按回车键继续...")
            continue

        if not game.reveal(x, y):
            clear_screen()
            game.display_board()
            print(f"\n{Colors.RED}游戏结束！您踩到了地雷。{Colors.RESET}")
            game_over = True
        elif len(game.revealed) + len(game.mines) == game.size * game.size:
            clear_screen()
            game.display_board()
            print(f"\n{Colors.GREEN}恭喜！您赢了！{Colors.RESET}")
            game_over = True

    play_again = input("您想再玩一次吗？(y/n): ")
    if play_again.lower() == 'y':
        play_game()

if __name__ == "__main__":
    clear_screen()
    print(f"{Colors.GREEN}欢迎来到扫雷游戏！{Colors.RESET}")
    print("\n游戏说明:")
    print("1. 输入行和列的数字来揭示一个单元格。")
    print("2. 数字表示相邻地雷的数量。")
    print("3. 避免揭示地雷以赢得游戏。")
    print("\n祝您好运！")
    input("\n按回车键开始游戏...")
    play_game()
