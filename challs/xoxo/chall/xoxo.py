import random
import string

from secret import flag
import re

re_sanitize = re.compile(r'(?:globals|__|import|locals|exec|eval|join|format|replace|translate|try|except|with|content|frame|back|open|write|read)').sub
alphabet = string.ascii_letters + string.digits + "([,])"


def sanitize(text):
    text = text.strip()
    text = text[:17] if len(text) > 17 else text
    text = ''.join([c for c in text if c in alphabet])

    assert text[0] in '([' and text[-1] in '])'
    assert text.count(',') == 1

    text = re_sanitize('', text)
    return text


del re, string


def clear_builtins():
    __builtins__.__dict__.clear()


class Game:

    def __init__(self, dim=3, computer_begins=True):
        assert 3 <= dim <= 100
        self.dim = dim
        self.n_moves = 0
        self.n_wins = 0

        self.computer = 'X'
        self.player = 'O'

        self.computer_win = self.dim * self.computer
        self.player_win = self.dim * self.player

        self.computer_turn = computer_begins

        self.positions = [[' ' for _ in range(self.dim)] for _ in range(self.dim)]
        self.empty = [(x, y) for x in range(self.dim) for y in range(self.dim)]

        self.win = ''

    def draw(self):
        print()
        line = (2 * self.dim + 1) * "-"
        print(line)
        for i in range(self.dim):
            print('|' + " ".join(self.positions[i]) + '|')
        print(line)

    def current_symbol(self):
        if self.computer_turn:
            return self.computer
        else:
            return self.player

    def move(self, x, y):
        assert self.is_empty(x, y)

        self.positions[x][y] = self.computer if self.computer_turn else self.player
        self.empty.remove((x, y))
        self.computer_turn = not self.computer_turn

        self.n_moves += 1
        self.draw()

    def is_empty(self, x, y):
        return not self.positions[x][y].strip()

    def check_line(self, line):
        if line == self.computer_win:
            return self.computer
        elif line == self.player_win:
            return self.player
        else:
            return ''

    def is_win(self, positions):
        # rows
        for line in positions:
            line_check = self.check_line(''.join(line))
            if line_check:
                return line_check

        # columns
        for i in range(self.dim):
            line = [line[i] for line in positions]
            line_check = self.check_line(''.join(line))
            if line_check:
                return line_check

        # downward diagonal
        line = [positions[j][j] for j in range(self.dim)]
        line_check = self.check_line(''.join(line))
        if line_check:
            return line_check

        # upward diagonal
        line = [positions[self.dim - 1 - j][j] for j in range(self.dim)]
        line_check = self.check_line(''.join(line))
        if line_check:
            return line_check

    def find_winning(self, player):
        for x, y in self.empty:
            pos = [line[:] for line in self.positions]
            pos[x][y] = player

            if self.is_win(pos):
                return x, y

        return -1, -1

    def auto_move(self):
        # check for winning moves
        x, y = self.find_winning(self.computer)
        if (x, y) != (-1, -1):
            return self.move(x, y)

        # check to block opponent's winning move
        x, y = self.find_winning(self.player)
        if (x, y) != (-1, -1):
            return self.move(x, y)

        # if there is no winning move, do it randomly
        while True:
            x, y = random.choice(self.empty)
            return self.move(x, y)

    def get_coordinates(self):
        print("Input coordinates as tuple or a list, ex. [row, column]:")
        x, y = eval(sanitize(input(">>>")))
        assert 1 <= x <= self.dim, f"Row must be between 1 and {self.dim}. Your input: {x}"
        assert 1 <= y <= self.dim, f"Column must be between 1 and {self.dim}. Your input: {y}"
        x -= 1
        y -= 1
        return x, y

    def request_move(self):
        while True:
            try:
                x, y = self.get_coordinates()
            except Exception as e:
                print(e)
                print("Invalid input! Don't you try anything funny! For this you lose at this round!")
                self.n_wins = 0
                return False

            if self.is_empty(x, y):
                self.move(x, y)
                return True
            else:
                print("Invalid move! Please choose empty field.")

    def turn(self):
        if self.computer_turn:
            if self.n_moves == 0:
                print(f"I will have first move as {self.computer}.")
            else:
                print("My turn!")
            self.auto_move()
        else:
            if self.n_moves == 0:
                print(f"You have the first move as {self.player}.")
            else:
                print("Your turn!")

            valid = self.request_move()

            # if move is invalid computer auto-wins the round
            if not valid:
                self.win = self.computer
                return

        self.win = self.is_win(self.positions)

    def play(self):
        while not self.win:
            if self.n_moves == self.dim * self.dim:
                return
            self.turn()

        if self.win == self.computer:
            self.n_wins = 0
            print("I won! I reset your win streak to 0, take that!\n")
        elif self.win == self.player:
            self.n_wins += 1
            print(f"You actually won, congrats! Your current win streak is: {self.n_wins}\n")
        else:
            print("It's a draw!\n")


def main(n=100):

    print(f"Welcome to tic-tac-toe game! I have the flag and it might be yours if you beat me {n} times in a row.")
    print("Let's randomly determine who begins!")

    for _ in range(n):
        computer_begins = bool(random.randint(0, 1))
        dim = random.randint(3, 30)
        game = Game(computer_begins=computer_begins, dim=dim)
        game.play()

    if game.n_wins < n:
        print(f"You did not succeed in getting {n} wins.")
    elif game.n_wins == n:
        print("You won, so what! Did you expect me to just give you the flag?")
    else:
        print("Wow how did you do that? I'm kinda scared. Here's your flag, please leave me alone.")
        print(flag)


if __name__ == '__main__':
    main()

