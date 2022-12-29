from math import inf
from collections import Counter
import itertools
from time import time
import array as arr
from numpy import random
import matplotlib.pyplot as plt

TIME_LIMIT = 1
usermode = input("Enter mode...0 for play-mode and 1 for analysis-mode:")
if usermode == "1":
    print("analysis mode in progress...no input required")
        
    def index(x, y):
        x -= 1
        y -= 1
        return ((x//3)*27) + ((x % 3)*3) + ((y//3)*9) + (y % 3)


    def box(x, y):
        return index(x, y) // 9


    def next_box(i):
        return i % 9


    def indices_of_box(b):
        return list(range(b*9, b*9 + 9))


    def print_board(state):
        for row in range(1, 10):
            row_str = ["|"]
            for col in range(1, 10):
                row_str += [state[index(row, col)]]
                if (col) % 3 == 0:
                    row_str += ["|"]
            if (row-1) % 3 == 0:
                print("-"*(len(row_str)*2-1))
            print(" ".join(row_str))
        print("-"*(len(row_str)*2-1))
    

    
    def add_piece(state, move, player):
        if not isinstance(move, int):
            move = index(move[0], move[1])
        return state[: move] + player + state[move+1:]


    def update_box_won(state):
        temp_box_win = ["."] * 9
        for b in range(9):
            idxs_box = indices_of_box(b)
            box_str = state[idxs_box[0]: idxs_box[-1]+1]
            temp_box_win[b] = check_small_box(box_str)
        return temp_box_win


    def check_small_box(box_str):
        global possible_goals
        for idxs in possible_goals:
            (x, y, z) = idxs
            if (box_str[x] == box_str[y] == box_str[z]) and box_str[x] != ".":
                return box_str[x]
        return "."


    def possible_moves(last_move):
        global box_won
        if not isinstance(last_move, int):
            last_move = index(last_move[0], last_move[1])
        box_to_play = next_box(last_move)
        idxs = indices_of_box(box_to_play)
        if box_won[box_to_play] != ".":
            pi_2d = [indices_of_box(b) for b in range(9) if box_won[b] == "."]
            possible_indices = list(itertools.chain.from_iterable(pi_2d))
        else:
            possible_indices = idxs
        return possible_indices


    def successors(state, player, last_move):
        succ = []
        moves_idx = []
        possible_indexes = possible_moves(last_move)
        for idx in possible_indexes:
            if state[idx] == ".":
                moves_idx.append(idx)
                succ.append(add_piece(state, idx, player))
        return zip(succ, moves_idx)


    def print_successors(state, player, last_move):
        for st in successors(state, player, last_move):
            print_board(st[0])
    

    def opponent(p):
        return "O" if p == "X" else "X"


    def evaluate_small_box(box_str, player):
        global possible_goals
        score = 0
        three = Counter(player * 3)
        two = Counter(player * 2 + ".")
        one = Counter(player * 1 + "." * 2)
        three_opponent = Counter(opponent(player) * 3)
        two_opponent = Counter(opponent(player) * 2 + ".")
        one_opponent = Counter(opponent(player) * 1 + "." * 2)

        for idxs in possible_goals:
            (x, y, z) = idxs
            current = Counter([box_str[x], box_str[y], box_str[z]])

            if current == three:
                score += 100
            elif current == two:
                score += 10
            elif current == one:
                score += 1
            elif current == three_opponent:
                score -= 100
                return score
            elif current == two_opponent:
                score -= 10
            elif current == one_opponent:
                score -= 1

        return score


    def evaluate(state, last_move, player):
        global box_won
        score = 0
        score += evaluate_small_box(box_won, player) * 200
        for b in range(9):
            idxs = indices_of_box(b)
            box_str = state[idxs[0]: idxs[-1]+1]
            score += evaluate_small_box(box_str, player)
        return score


   
    def minimax2(state, last_move, player, depth):
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, opponent(player))
        succ = successors(state, player, last_move)
        best_move = (-inf, None)
        for s in succ:
            val = min_turn2(s[0], s[1], opponent(player), depth-1)
            if val > best_move[0]:
                best_move = (val, s)
        return best_move[1]

    def min_turn2(state, last_move, player, depth):
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, opponent(player))
        succ = successors(state, player, last_move)
        best_value = inf
        for s in succ:
            val = max_turn2(s[0], s[1], opponent(player), depth-1)
            if val < best_value:
                best_value = val
        return best_value

    def max_turn2(state, last_move, player, depth):
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, player)
        succ = successors(state, player, last_move)
        best_value = -inf
        for s in succ:
            val = min_turn2(s[0], s[1], opponent(player), depth-1)
            if val > best_value:
                best_value = val
        return best_value


    
    def minimax(state, last_move, player, depth):
        succ = successors(state, player, last_move)
        best_move = (-inf, None)
        for s in succ:
            val = min_turn(s[0], s[1], opponent(player), depth-1,-inf, inf)
            if val > best_move[0]:
                best_move = (val, s)
        return best_move[1]


    def min_turn(state, last_move, player, depth, alpha, beta):
        global box_won
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, opponent(player))
        succ = successors(state, player, last_move)
        for s in succ:
            val = max_turn(s[0], s[1], opponent(player), depth-1,alpha,beta)
            if val < beta:
                beta = val
            if alpha >= beta:
                break
        return beta


    def max_turn(state, last_move, player, depth, alpha, beta):
        global box_won
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, player)
        succ = successors(state, player, last_move)
        for s in succ:
            val = min_turn(s[0], s[1], opponent(player), depth-1,alpha, beta)
            if alpha < val:
                alpha = val
            if alpha >= beta:
                break
        return alpha


    def valid_input(state, move):
        global box_won
        if not (0 < move[0] < 10 and 0 < move[1] < 10):
            return False
        if box_won[box(move[0], move[1])] != ".":
            return False
        if state[index(move[0], move[1])] != ".":
            return False
        return True


 


    def game(state, depth=2):
        time_array = arr.array('f')
        time_array1 = arr.array('f')
        time_array2 = arr.array('f')
        global box_won, possible_goals 
        possible_goals = [(0, 4, 8), (2, 4, 6)]
        possible_goals += [(i, i+3, i+6) for i in range(3)]
        possible_goals += [(3*i, 3*i+1, 3*i+2) for i in range(3)]
        box_won = update_box_won(state)
        print(box_won)
        print_board(state)
        bot_move = -1
        user_move = -1
        user_state=state
        s_time=time()
        while True:
            s1_time=time()
            user_state,user_move = minimax2(user_state, user_move, "X", depth)
            e1_time=time()
            time_array1.append(e1_time-s1_time)
            
            user_state = add_piece(state, user_move, "X")
            print_board(user_state)
            print("time taken by X:",e1_time-s1_time)
            box_won = update_box_won(user_state)

            game_won = check_small_box(box_won)
            if game_won != ".":
                state = user_state
                break
            
            s_time = time()
            bot_state, bot_move = minimax(user_state, bot_move, "O", depth)
            state = add_piece(bot_state, bot_move, "O")
            e_time = time()
            time_array2.append(e_time-s_time)
            print_board(bot_state)
            print("time taken by O:",e_time-s_time)
            state = bot_state
            box_won = update_box_won(bot_state)
            game_won = check_small_box(box_won)
            if game_won != ".":
                break

        if game_won == "X":
            print("X won")
            time_array1.pop(0)
        else:
            print("O won")
        for i in range(len(time_array2)):
            time_array.append(time_array1[i]-time_array2[i])
        
        plt.subplot(1, 3, 1)
        plt.plot(time_array)
        plt.title("Time Difference")
        
        plt.subplot(1, 3, 2)
        plt.plot(time_array1)
        plt.title("Minimax")
        
        
        plt.subplot(1, 3, 3)
        plt.plot(time_array2)
        plt.title("Alpha-Beta Pruning")
        
        plt.xlabel("Iteration")
        plt.ylabel("Time in microseconds")
        plt.show()

        return state
    state="."*81
    game(state,depth=2)
else:        
    print("play mode in progress....")
    def minimax(state, last_move, player, depth):
        succ = successors(state, player, last_move)
        best_move = (-inf, None)
        for s in succ:
            val = min_turn(s[0], s[1], opponent(player), depth-1,-inf, inf)
            if val > best_move[0]:
                best_move = (val, s)
        return best_move[1]


    def min_turn(state, last_move, player, depth, alpha, beta):
        global box_won
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, opponent(player))
        succ = successors(state, player, last_move)
        for s in succ:
            val = max_turn(s[0], s[1], opponent(player), depth-1,alpha, beta)
            if val < beta:
                beta = val
            if alpha >= beta:
                break
        return beta


    def max_turn(state, last_move, player, depth, alpha, beta):
        global box_won
        if depth <= 0 or check_small_box(box_won) != ".":
            return evaluate(state, last_move, player)
        succ = successors(state, player, last_move)
        for s in succ:
            val = min_turn(s[0], s[1], opponent(player), depth-1,alpha, beta)
            if alpha < val:
                alpha = val
            if alpha >= beta:
                break
        return alpha


    def valid_input(state, move):
        global box_won
        if not (0 < move[0] < 10 and 0 < move[1] < 10):
            return False
        if box_won[box(move[0], move[1])] != ".":
            return False
        if state[index(move[0], move[1])] != ".":
            return False
        return True


    def take_input(state, bot_move):
        all_open_flag = False
        if bot_move == -1 or len(possible_moves(bot_move)) > 9:
            all_open_flag = True
        if all_open_flag:
            print("enter position in matrix fashion")
        else:
            box_dict = {0: "UL", 1: "AC", 2: "UR",
                        3: "LC", 4: "C", 5: "RC",
                        6: "BL", 7: "BC", 8: "BR"}
            print("Where do you want to throw the 'X'? MUST BE IN THE QUADRANT :-"
                  + box_dict[next_box(bot_move)])
        x = int(input("Row = "))
        if x == -1:
            raise SystemExit
        y = int(input("Column = "))
        print("")
        if bot_move != -1 and index(x, y) not in possible_moves(bot_move):
            raise ValueError
        if not valid_input(state, (x, y)):
            raise ValueError
        return (x, y)


    def game(state="." * 81, depth=20):
        global box_won, possible_goals 
        possible_goals = [(0, 4, 8), (2, 4, 6)]
        possible_goals += [(i, i+3, i+6) for i in range(3)]
        possible_goals += [(3*i, 3*i+1, 3*i+2) for i in range(3)]
        box_won = update_box_won(state)
        print_board(state)
        bot_move = -1

        while True:
            try:
                user_move = take_input(state, bot_move)
            except ValueError:
                print("Invalid value")
                print_board(state)
                continue
            except SystemError:
                print("error..game over")
                break

            user_state = add_piece(state, user_move, "X")
            print_board(user_state)
            box_won = update_box_won(user_state)

            game_won = check_small_box(box_won)
            if game_won != ".":
                state = user_state
                break

            print("wait...")
            bot_state, bot_move = minimax(user_state, user_move, "O", depth)
            
            print("$" * 40)
            print("The computer put 'O' in", bot_move, "\n")
            print_board(bot_state)
            state = bot_state
            box_won = update_box_won(bot_state)
            game_won = check_small_box(box_won)
            if game_won != ".":
                break

        if game_won == "X":
            print("You won")
        else:
            print("You lost")
        

        return state

    state= "." * 81
    game(state, depth=2)