import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

def linearly_edge_reinforced_random_walk_plane(steps, c):
    current_pos = np.array([75, 75])

    # plt.plot(current_pos[0], current_pos[1], 'ro', markersize=5, markerfacecolor='r')

    move_weights = np.ones((150, 150, 150, 150))

    for i in range(1, steps):
        neighbors = get_neighbors(current_pos)

        move_probs = get_move_probs(current_pos, move_weights)
        # print(move_probs)
        # print(np.sum(move_probs))
        chosen_move_index = np.random.choice(len(neighbors), 1, p=move_probs.flatten())[0]
        chosen_move = neighbors[chosen_move_index]

        move_weights[current_pos[0], current_pos[1], chosen_move[0], chosen_move[1]] += c
        move_weights[chosen_move[0], chosen_move[1], current_pos[0], current_pos[1]] += c

        # plt.plot(current_pos[0], current_pos[1], 'ro', markersize=5, markerfacecolor='r')

        current_pos = chosen_move

        # plt.plot(current_pos[0], current_pos[1], 'ro', markersize=5, markerfacecolor='b')

        # plt.pause(0.01)

    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.title('Linearly Edge-Reinforced Random Walk on 2D Plane')
    # plt.show()
    x = abs(current_pos[0] - 50)
    y = abs(current_pos[1] - 50)
    return x + y

def get_neighbors(pos):
    i, j = pos

    possible_moves = np.array([[i, j+1], [i+1, j], [i, j-1], [i-1, j]])

    return possible_moves

def get_weight_sum(pos, move_weights):
    x, y = pos
    n1 = move_weights[x, y, x, y+1]
    n2 = move_weights[x, y, x+1, y]
    n3 = move_weights[x, y, x, y-1]
    n4 = move_weights[x, y, x-1, y]
    weight_sum = n1 + n2 + n3 + n4
    return weight_sum

def get_move_probs(current_pos, move_weights):
    x, y = current_pos
    weight_sum = get_weight_sum(current_pos, move_weights)

    p1 = move_weights[x, y, x, y+1] / weight_sum
    p2 = move_weights[x, y, x+1, y] / weight_sum
    p3 = move_weights[x, y, x, y-1] / weight_sum
    p4 = move_weights[x, y, x-1, y] / weight_sum

    probs = np.array([p1, p2, p3, p4])

    return probs

def get_proccess_stats():
    _index = [5,10]
    _columns = [1,2]
    for a in range (15,1001,5):
        _index.append(a)
    print(_index)
    for b in range (3,51):
        _columns.append(b)
    print(_columns)
    for c in range(10,11):
        print(f'instant {c} begins...')
        w, h = 50, 200
        Matrix = [[0 for x in range(w)] for y in range(h)] 
        for steps in range(5,1001,5):
            print(f'begining {steps} steps walk')
            for i in range(1,51):
                print(f'doing {i}th try for {steps} steps for c = {c}')
                distance = linearly_edge_reinforced_random_walk_plane(steps, c)
                Matrix[int(steps/5) - 1][i - 1] = distance
        df = pd.DataFrame(Matrix,
                index=_index, columns=_columns)
        _sheet_name = f'Sheet + {c}'
        df.to_excel('LERRW_SHEET.xlsx', sheet_name=_sheet_name)

get_proccess_stats()


