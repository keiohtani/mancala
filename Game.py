from functools import reduce
import time


class Game:
    def __init__(self):
        self.stones = [4 for i in range(14)]
        self.stones[0] = 0
        self.stones[7] = 0
        self.turn = 0

    def _print_map(self):
        print(
            f"   {self.stones[13]} {self.stones[12]} {self.stones[11]} {self.stones[10]} {self.stones[9]} {self.stones[8]}\n"
            f"{self.stones[0]}               {self.stones[7]}\n"
            f"   {self.stones[1]} {self.stones[2]} {self.stones[3]} {self.stones[4]} {self.stones[5]} {self.stones[6]}\n"
        )
        print("\n\n\n\n\n\n\n\n\n\n\n")

    def _convert_position(self, position):
        position = position if position < 7 else position + 1
        return position

    def _move(self):
        def validate_move(position):
            low_limit = 7 if self.turn else 1
            high_limit = 12 if self.turn else 6
            if low_limit <= position <= high_limit:
                position = self._convert_position(position)
                if self.stones[position] == 0:
                    print("There is no stones in the hole.")
                else:
                    self._change_turn()
                    moves_left = self.stones[position]
                    self.stones[position] = self.stones[position] = 0
                    self._update(position, moves_left)
            else:
                print(f"The move needs to be between {low_limit} to {high_limit}")

        position = int(input("Choose your move: "))
        validate_move(position)

    def _validate_index(self, position):
        return position if position < 14 else 0

    def _update(self, current_position, moves_left):
        if moves_left == 0:
            current_position = self._validate_index(current_position)
            self._check_special_actions(current_position)
        else:
            current_position = current_position + 1
            current_position = self._validate_index(current_position)
            self.stones[current_position] = self.stones[current_position] + 1
            time.sleep(0.5)
            self._print_map()
            self._update(current_position, moves_left - 1)

    def _get_opposite_position(self, position):
        if position == 1:
            position = 13
        elif position == 2:
            position = 12
        elif position == 3:
            position = 11
        elif position == 4:
            position = 10
        elif position == 5:
            position = 9
        elif position == 6:
            position = 8
        elif position == 8:
            position = 6
        elif position == 9:
            position = 5
        elif position == 10:
            position = 4
        elif position == 11:
            position = 3
        elif position == 12:
            position = 2
        elif position == 13:
            position = 1
        return position

    def _steal_stones(self, position):
        opposite_position = self._get_opposite_position(position)
        stone = self.stones[opposite_position]
        self.stones[opposite_position] = 0
        self.stones[self.turn] = self.stones[self.turn] + stone

    def _check_special_actions(self, position):
        if position == self.turn:
            self._change_turn()
            print("Play again.")
        elif self.stones[position] == 1:
            self._steal_stones(position)

    def _change_turn(self):
        self.turn = 7 if self.turn == 0 else 0

    def _is_game_over(self):
        player_1_row = self.stones[1:7]
        player_2_row = self.stones[8:14]
        if not any(player_1_row) or not any(player_2_row):
            player_1_total = reduce(lambda x, y: x + y, player_1_row)
            player_2_total = reduce(lambda x, y: x + y, player_2_row)
            self.stones[0] = self.stones[0] + player_2_total
            self.stones[7] = self.stones[7] + player_1_total
            print("Score")
            print(f"Player 1: {self.stones[7]}")
            print(f"Player 2: {self.stones[0]}")
            return True
        else:
            return False

    def start(self):
        while not self._is_game_over():
            print("\n\n\n\n\n\n\n\n\n\n\n")
            print(f"Player {bool(self.turn) + 1}'s move.'")
            self._print_map()
            self._move()
            print("\n-------------------------------\n")
