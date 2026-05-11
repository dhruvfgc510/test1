import random
import os


class Board:
    def __init__(self):
        self.grid = [" " for _ in range(9)]
        self.winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6],              # diagonals
        ]

    def display(self):
        print()
        for row in range(3):
            cells = self.grid[row * 3: row * 3 + 3]
            print(f" {cells[0]} | {cells[1]} | {cells[2]} ")
            if row < 2:
                print("---+---+---")
        print()

    def display_with_numbers(self):
        print()
        for row in range(3):
            nums = [str(row * 3 + col + 1) if self.grid[row * 3 + col] == " " else self.grid[row * 3 + col]
                    for col in range(3)]
            print(f" {nums[0]} | {nums[1]} | {nums[2]} ")
            if row < 2:
                print("---+---+---")
        print()

    def make_move(self, position, marker):
        if self.grid[position] == " ":
            self.grid[position] = marker
            return True
        return False

    def is_winner(self, marker):
        return any(
            all(self.grid[i] == marker for i in combo)
            for combo in self.winning_combos
        )

    def is_full(self):
        return " " not in self.grid

    def is_game_over(self):
        return self.is_winner("X") or self.is_winner("O") or self.is_full()

    def available_moves(self):
        return [i for i, cell in enumerate(self.grid) if cell == " "]

    def reset(self):
        self.grid = [" " for _ in range(9)]


class Player:
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker
        self.score = 0

    def get_move(self, board):
        while True:
            try:
                move = int(input(f"{self.name} ({self.marker}), enter position (1-9): ")) - 1
                if move < 0 or move > 8:
                    print("Invalid input. Choose a number between 1 and 9.")
                elif board.grid[move] != " ":
                    print("That cell is already taken. Try again.")
                else:
                    return move
            except ValueError:
                print("Please enter a valid number.")


class AIPlayer(Player):
    def __init__(self, name, marker, difficulty="hard"):
        super().__init__(name, marker)
        self.difficulty = difficulty
        self.opponent_marker = "X" if marker == "O" else "O"

    def get_move(self, board):
        print(f"{self.name} ({self.marker}) is thinking...")
        if self.difficulty == "easy":
            return self._random_move(board)
        elif self.difficulty == "medium":
            return self._medium_move(board)
        else:
            return self._best_move(board)

    def _random_move(self, board):
        return random.choice(board.available_moves())

    def _medium_move(self, board):
        win = self._find_winning_move(board, self.marker)
        if win is not None:
            return win
        block = self._find_winning_move(board, self.opponent_marker)
        if block is not None:
            return block
        return self._random_move(board)

    def _find_winning_move(self, board, marker):
        for move in board.available_moves():
            board.grid[move] = marker
            if board.is_winner(marker):
                board.grid[move] = " "
                return move
            board.grid[move] = " "
        return None

    def _best_move(self, board):
        best_score = float("-inf")
        best_move = None
        for move in board.available_moves():
            board.grid[move] = self.marker
            score = self._minimax(board, False, float("-inf"), float("inf"))
            board.grid[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _minimax(self, board, is_maximizing, alpha, beta):
        if board.is_winner(self.marker):
            return 10
        if board.is_winner(self.opponent_marker):
            return -10
        if board.is_full():
            return 0

        if is_maximizing:
            best = float("-inf")
            for move in board.available_moves():
                board.grid[move] = self.marker
                best = max(best, self._minimax(board, False, alpha, beta))
                board.grid[move] = " "
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float("inf")
            for move in board.available_moves():
                board.grid[move] = self.opponent_marker
                best = min(best, self._minimax(board, True, alpha, beta))
                board.grid[move] = " "
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_scores(players):
    print("=" * 30)
    print("         SCOREBOARD")
    print("=" * 30)
    for p in players:
        print(f"  {p.name} ({p.marker}): {p.score} wins")
    print("=" * 30)


def get_game_mode():
    print("\nSelect game mode:")
    print("  1. Player vs Player")
    print("  2. Player vs AI")
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Please enter 1 or 2.")


def get_difficulty():
    print("\nSelect AI difficulty:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard (unbeatable)")
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        print("Please enter 1, 2, or 3.")


def play_round(board, players):
    board.reset()
    current = 0
    while not board.is_game_over():
        clear_screen()
        print_scores(players)
        print("\nCurrent positions:")
        board.display_with_numbers()
        move = players[current].get_move(board)
        board.make_move(move, players[current].marker)
        if board.is_winner(players[current].marker):
            clear_screen()
            print_scores(players)
            board.display()
            print(f"  {players[current].name} wins this round!\n")
            players[current].score += 1
            return players[current]
        if board.is_full():
            clear_screen()
            print_scores(players)
            board.display()
            print("  It's a draw!\n")
            return None
        current = 1 - current
    return None


def main():
    clear_screen()
    print("=" * 30)
    print("       TIC TAC TOE")
    print("=" * 30)

    mode = get_game_mode()
    p1_name = input("\nEnter Player 1 name (X): ").strip() or "Player 1"
    player1 = Player(p1_name, "X")

    if mode == "1":
        p2_name = input("Enter Player 2 name (O): ").strip() or "Player 2"
        player2 = Player(p2_name, "O")
    else:
        difficulty = get_difficulty()
        player2 = AIPlayer("Computer", "O", difficulty)

    players = [player1, player2]
    board = Board()

    while True:
        play_round(board, players)
        again = input("Play another round? (y/n): ").strip().lower()
        if again != "y":
            break

    clear_screen()
    print("\nFinal Scores:")
    print_scores(players)
    winner = max(players, key=lambda p: p.score)
    if players[0].score == players[1].score:
        print("\nOverall result: It's a tie!")
    else:
        print(f"\nOverall winner: {winner.name}!")
    print("\nThanks for playing!\n")


if __name__ == "__main__":
    main()
