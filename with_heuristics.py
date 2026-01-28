import time
import random

map1_regions = {0: 'Western Australia', 1: 'Northern Territory', 2: 'South Australia', 3: 'Queensland',
                     4: 'New South Wales', 5: 'Victoria', 6: 'Tasmania'}
map1_adjacency = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3, 4, 5],
    3: [1, 2, 4],
    4: [2, 3, 5],
    5: [2, 4],
    6: []
}

map2_regions = {0: 'Washington', 1: 'Oregon', 2: 'California', 3: 'Idaho', 4: 'Nevada', 5: 'Arizona', 6: 'Utah',
             7: 'Montana', 8: 'Wyoming', 9: 'Colorado', 10: 'New Mexico', 11: 'North Dakota', 12: 'South Dakota',
             13: 'Nebraska', 14: 'Kansas', 15: 'Oklahoma', 16: 'Texas', 17: 'Minnesota', 18: 'Iowa',
             19: 'Missouri', 20: 'Arkansas', 21: 'Louisiana', 22: 'Wisconsin', 23: 'Illinois', 24: 'Mississippi',
             25: 'Michigan', 26: 'Indiana', 27: 'Kentucky', 28: 'Tennessee', 29: 'Alabama', 30: 'Ohio',
             31: 'West Virginia', 32: 'Virginia', 33: 'North Carolina', 34: 'South Carolina', 35: 'Georgia',
             36: 'Florida', 37: 'Pennsylvania', 38: 'Maryland', 39: 'Delaware', 40: 'New Jersey', 41: 'New York',
             42: 'Connecticut', 43: 'Hawaii', 44: 'Massachusetts', 45: 'Rhode Island', 46: 'Vermont',
             47: 'New Hampshire', 48: 'Maine', 49: 'Alaska'}

map2_adjacency = {0: [3, 1], 1: [0, 3, 4, 2], 2: [1, 4, 5], 3: [0, 1, 4, 6, 8, 7], 4: [1, 2, 5, 6, 3], 5: [2, 4, 6, 9, 10],
              6: [3, 4, 5, 10, 9, 8], 7: [3, 8, 12, 11], 8: [7, 3, 6, 9, 13, 12], 9: [8, 6, 5, 10, 15, 14, 13],
              10: [5, 6, 9, 15, 16], 11: [7, 12, 17], 12: [11, 7, 8, 13, 18, 17], 13: [18, 12, 8, 9, 14, 19],
              14: [13, 9, 15, 19], 15: [16, 20, 19, 14, 9, 10], 16: [10, 15, 20, 21], 17: [11, 12, 18, 22],
              18: [17, 12, 13, 19, 23, 22], 19: [18, 13, 14, 15, 20, 27, 28, 23], 20: [19, 15, 16, 21, 24, 28],
              21: [16, 20, 24], 22: [17, 18, 23, 25], 23: [22, 18, 19, 27, 26], 24: [29, 21, 28, 20], 25: [22, 26, 30],
              26: [25, 23, 27, 30], 27: [26, 23, 19, 28, 32, 31, 30], 28: [27, 19, 20, 24, 29, 35, 33, 32],
              29: [28, 24, 36, 35], 30: [25, 26, 27, 31, 37], 31: [30, 27, 32, 37, 38], 32: [38, 31, 27, 28, 33],
              33: [32, 28, 35, 34], 34: [33, 35], 35: [29, 28, 33, 34, 36], 36: [29, 35], 37: [30, 31, 41, 40, 38, 39],
              38: [31, 32, 39, 37], 39: [40, 38, 37], 40: [39, 37, 41], 41: [37, 40, 42, 44, 45, 46], 42: [40, 41, 44, 45],
              43: [], 44: [42, 47, 41, 45, 46], 45: [44, 42], 46: [41, 44, 47], 47: [46, 44, 48], 48: [47], 49: []}

color_legend = {0: 'CHECK!!!', 1: 'Red', 2: 'Blue', 3: 'Green', 4: 'Yellow', 5: 'Cyan', 6: 'Magenta', 6: 'Black',
                 7: 'White'}


class MapColorSolver:

    def __init__(self, num_states, adjacency_list):
        self.num_states = num_states
        self.adjacency_list = adjacency_list
        self.num_colors = 0
        self.assigned_colors = [0] * self.num_states 
        self.backtrack_count = 0

    def initialize_domain_tracking(self, num):
        tracking_dict = {}
        for i in range(self.num_states):
            tracking_dict[i] = {}
            for n in range(1, num + 1):
                tracking_dict[i][n] = -1
        return tracking_dict

    def initialize_state_domains(self, num):
        domain_dict = {}
        for i in range(self.num_states):
            domain_dict[i] = {}
            for n in range(1, num + 1):
                domain_dict[i][n] = 2
        return domain_dict

    
    def has_conflict_with_neighbors(self, state, color):
        return any(self.assigned_colors[j] == color for j in self.adjacency_list[state])

    def solve_coloring_problem(self, max_colors):
        domain_dict = self.initialize_state_domains(max_colors)
        min_required_colors = self.greedy_color_assignment(max_colors, domain_dict)
        return min_required_colors

    def greedy_color_assignment(self, num_colors, domain_dict):
        visited_states = []
        backtrack_counter = 0
        for state in self.adjacency_list:
            if state not in visited_states:
                for color in domain_dict[state]:
                    if not self.has_conflict_with_neighbors(state, color):
                        self.assigned_colors[state] = color
                        visited_states.append(state)
                        break
                for neighbor in self.adjacency_list[state]:
                    if neighbor not in visited_states:
                        for color in domain_dict[neighbor]:
                            if not self.has_conflict_with_neighbors(neighbor, color):
                                self.assigned_colors[neighbor] = color
                                visited_states.append(neighbor)
                                break
                            else:
                                backtrack_counter += 1
        return max(self.assigned_colors)

    def dfs_backtracking_solver(self, chrom_num, heuristic):
        domain_dict = self.initialize_state_domains(chrom_num)
        global state_status
        global parent_state
        state_status = {}
        parent_state = {}
        self.backtrack_count = 0
        for state in self.adjacency_list:
            state_status[state] = 10
            parent_state[state] = -1

        for state in self.adjacency_list:
            if state_status[state] == 10:
                backtrack = self.dfs_recursive_backtrack(state, domain_dict, heuristic)
                if backtrack == -1:
                    break
        return backtrack

    def dfs_recursive_backtrack(self, state, domain_dict, heuristic):
        global state_status
        global parent_state
        assigned = 0
        state_status[state] = 20

        if heuristic == '3':
            color_choice = self.select_least_constraining_value(state, domain_dict)
            if color_choice != -1:
                self.assigned_colors[state] = color_choice
                domain_dict[state][color_choice] = 1
                assigned = 1
            else:
                self.backtrack_count += 1
                return self.backtrack_count
        else:
            for color in domain_dict[state]:
                if self.has_conflict_with_neighbors(state, color) == False:
                    if assigned == 0:
                        self.assigned_colors[state] = color
                        domain_dict[state][color] = 1
                        assigned = 1
                else:
                    if assigned == 0:
                        self.backtrack_count += 1
                    domain_dict[state][color] = 0
            if assigned == 0:
                return -1

        if heuristic == '1':
            neighbor = self.select_min_remaining_values(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                backtrack = self.dfs_recursive_backtrack(neighbor, domain_dict, heuristic)
                if backtrack == -1:
                    return backtrack
        elif heuristic == '2':
            neighbor = self.select_high_degree_neighbor(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                backtrack = self.dfs_recursive_backtrack(neighbor, domain_dict, heuristic)
                if backtrack == -1:
                    return backtrack
        else:
            for neighbor in self.adjacency_list[state]:
                if state_status[neighbor] == 10:
                    parent_state[neighbor] = state
                    backtrack = self.dfs_recursive_backtrack(neighbor, domain_dict, heuristic)
                    if backtrack == -1:
                        return backtrack

            state_status[state] = 30
            return self.backtrack_count


    def dfs_forward_check_visit(self, state, domain_dict, track, heuristic):
        global state_status
        global parent_state
        assigned = 0
        previous_color = -1
        colors = {}
        state_status[state] = 20

        if heuristic == '3':
            for color in domain_dict[state]:
                if domain_dict[state][color] == 1:
                    previous_color = color

            color_choice = self.select_least_constraining_value(state, domain_dict)
            if color_choice != -1:
                self.assigned_colors[state] = color_choice
                domain_dict[state][color_choice] = 1
                assigned = 1
                self.forward_check_reduce_domain(state, color_choice, domain_dict, track)
            else:
                assigned = 0
        else:
            for color in domain_dict[state]:
                if domain_dict[state][color] == 2:
                    if assigned == 0:
                        self.assigned_colors[state] = color
                        domain_dict[state][color] = 1
                        assigned = 1
                        self.forward_check_reduce_domain(state, color, domain_dict, track)
                elif domain_dict[state][color] == 1:
                    previous_color = color

        if assigned == 1 and previous_color != -1:
            self.forward_check_restore_domain(state, previous_color, domain_dict, track)
            colors[previous_color] = 2

        if assigned == 0:
            self.backtrack_count += 1
            if parent_state[state] != -1:
                self.dfs_forward_check_visit(parent_state[state], domain_dict, track, heuristic)

        if heuristic == '1':
            neighbor = self.select_min_remaining_values(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                self.dfs_forward_check_visit(neighbor, domain_dict, track, heuristic)
        elif heuristic == '2':
            neighbor = self.select_high_degree_neighbor(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                self.dfs_forward_check_visit(neighbor, domain_dict, track, heuristic)
        else:
            for neighbor in self.adjacency_list[state]:
                if state_status[neighbor] == 10:
                    parent_state[neighbor] = state
                    self.dfs_forward_check_visit(neighbor, domain_dict, track, heuristic)
        state_status[state] = 30
        return self.backtrack_count

    def dfs_with_forward_checking(self, chrom_num, heuristic):
        global state_status
        global parent_state
        domain_dict = self.initialize_state_domains(chrom_num)
        track = self.initialize_domain_tracking(chrom_num)
        state_status = {}
        parent_state = {}
        self.backtrack_count = 0
        for state in self.adjacency_list:
            state_status[state] = 10
            parent_state[state] = -1

        for state in self.adjacency_list:
            if state_status[state] == 10:
                backtrack = self.dfs_forward_check_visit(state, domain_dict, track, heuristic)
        return backtrack

    def forward_check_reduce_domain(self, state, color, domain_dict, track):
        for neighbor in self.adjacency_list[state]:
            domain_dict[neighbor][color] = 0
            if track[neighbor][color] == -1:
                track[neighbor][color] = state

    def forward_check_restore_domain(self, state, color, domain_dict, track):
        for neighbor in self.adjacency_list[state]:
            if track[neighbor][color] == state and domain_dict[neighbor][color] == 0:
                domain_dict[neighbor][color] = 2

    
    def dfs_with_forward_checking_singleton(self, chrom_num, heuristic):
        global state_status
        global parent_state
        domain_dict = self.initialize_state_domains(chrom_num)
        track = self.initialize_domain_tracking(chrom_num)
        state_status = {}
        parent_state = {}
        self.backtrack_count = 0
        for state in self.adjacency_list:
            state_status[state] = 10
            parent_state[state] = -1

        for state in self.adjacency_list:
            if state_status[state] == 10:
                backtrack = self.dfs_forward_check_singleton_visit(state, domain_dict, track, heuristic)
        return backtrack

    def dfs_forward_check_singleton_visit(self, state, domain_dict, track, heuristic):
        global state_status
        global parent_state
        assigned = 0
        previous_color = -1
        colors = {}
        state_status[state] = 20

        if heuristic == '3':
            for color in domain_dict[state]:
                if domain_dict[state][color] == 1:
                    previous_color = color

            color_choice = self.select_least_constraining_value(state, domain_dict)
            if color_choice != -1:
                self.assigned_colors[state] = color_choice
                domain_dict[state][color_choice] = 1
                assigned = 1
                self.singleton_reduce_domain(state, color_choice, domain_dict, track)
            else:
                assigned = 0
        else:
            for color in domain_dict[state]:
                if domain_dict[state][color] == 2:
                    if assigned == 0:
                        self.assigned_colors[state] = color
                        domain_dict[state][color] = 1
                        assigned = 1
                        self.singleton_reduce_domain(state, color, domain_dict, track)
                elif domain_dict[state][color] == 1:
                    previous_color = color

        if assigned == 1 and previous_color != -1:
            self.singleton_restore_domain(state, previous_color, domain_dict, track)
            colors[previous_color] = 2

        if assigned == 0:
            self.backtrack_count += 1
            if parent_state[state] != -1:
                self.dfs_forward_check_singleton_visit(parent_state[state], domain_dict, track, heuristic)

        if heuristic == '1':
            neighbor = self.select_min_remaining_values(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                self.dfs_forward_check_singleton_visit(neighbor, domain_dict, track, heuristic)
        elif heuristic == '2':
            neighbor = self.select_high_degree_neighbor(state, domain_dict)
            if neighbor == -1:
                return self.backtrack_count
            else:
                parent_state[neighbor] = state
                self.dfs_forward_check_singleton_visit(neighbor, domain_dict, track, heuristic)
        else:
            for neighbor in self.adjacency_list[state]:
                if state_status[neighbor] == 10:
                    parent_state[neighbor] = state
                    self.dfs_forward_check_singleton_visit(neighbor, domain_dict, track, heuristic)
        state_status[state] = 30
        return self.backtrack_count

    def singleton_reduce_domain(self, state, color, domain_dict, track):
        for neighbor in self.adjacency_list[state]:
            check = domain_dict[neighbor][color]
            domain_dict[neighbor][color] = 0
            if check == 2:
                color_s = self.is_singleton(neighbor, domain_dict)
                if color_s > 0:
                    self.singleton_reduce_domain(neighbor, color_s, domain_dict, track)
            if track[neighbor][color] == -1:
                track[neighbor][color] = state

    # Determine if a state is a singleton.
    def is_singleton(self, neighbor, domain_dict):
        color_dict = domain_dict[neighbor]
        count = 0
        temp_color = 0

        for key, value in color_dict.items():
            if value == 2:
                count += 1
                temp_color = key

        if count != 1:
            temp_color = 0

        return temp_color

    def singleton_restore_domain(self, state, color, domain_dict, track):
        for neighbor in self.adjacency_list[state]:
            if track[neighbor][color] == state and domain_dict[neighbor][color] == 0:
                domain_dict[neighbor][color] = 2

    def select_high_degree_neighbor(self, state, domain_dict):
        global state_status
        adjacencies = {}
        max_degree = 0
        selected = -1
        for neighbor in self.adjacency_list[state]:
            if state_status[neighbor] == 10:
                count = 0
                for n in self.adjacency_list[neighbor]:
                    if state_status[n] == 10:
                        count += 1
                if count > max_degree:
                    max_degree = count
                    selected = neighbor
        return selected

    def select_min_remaining_values(self, state, domain_dict):
        global state_status
        min_values = 99
        selected = -1
        for neighbor in self.adjacency_list[state]:
            if state_status[neighbor] == 10:
                count = 0
                for color in domain_dict[neighbor]:
                    if domain_dict[neighbor][color] == 2:
                        count += 1
                if min_values > count and count > 0:
                    min_values = count
                    selected = neighbor
        return selected

    def select_least_constraining_value(self, state, domain_dict):
        global state_status
        min_values = 99
        selected = -1
        for color in domain_dict[state]:
            if self.has_conflict_with_neighbors(state, color) == True:
                continue
            count = 0
            if domain_dict[state][color] == 2:
                for neighbor in self.adjacency_list[state]:
                    if state_status[neighbor] == 10:
                        if domain_dict[neighbor][color] == 2:
                            count += 1
                if min_values > count and count > 0:
                    min_values = count
                    selected = color
        return selected

def main():
    start_time = time.time_ns()
    map_choice = input('Select map to be colored : \n1.Australia\n2.USA\n')
    print()
    if map_choice == '1':
        state_mapping = map1_regions
        borders = map1_adjacency
        map_coloring = MapColorSolver(len(borders), borders)
        min_colors = map_coloring.solve_coloring_problem(5)
        map_coloring.num_colors = min_colors
        print("The lowest chromatic number that can be achieved for the Australia map is: ", map_coloring.num_colors)
        print()

    elif map_choice == '2':
        state_mapping = map2_regions
        borders = map2_adjacency
        map_coloring = MapColorSolver(len(borders), borders)
        min_colors = map_coloring.solve_coloring_problem(5)
        map_coloring.num_colors = min_colors
        print("The lowest chromatic number that can be achieved for the United States map is: ", map_coloring.num_colors)
        print()

    heuristic_choice = input(
        'Choose a heuristic from the options below:\n1.Minimum Remaining Values (MRV)\n2.Degree Constraint\n3.Least Constraining Value\n')
    print()
    print("Step 1: DFS only:")
    print()
    map_coloring.backtrack_count = 0
    map_coloring.backtrack_count = map_coloring.dfs_backtracking_solver(map_coloring.num_colors, heuristic_choice)
    end_time = time.time_ns()
    assigned_colors = []
    print("Total number of backtracks: ", map_coloring.backtrack_count)
    for colors in map_coloring.assigned_colors:
        assigned_colors.append(color_legend[colors])

    print("Colors assigned to the states in their original order: ", assigned_colors)
    print("Time taken", (end_time - start_time), 'ns')
    print()

    print("Step 2: DFS with Forward Checking:")
    print()
    map_coloring.backtrack_count = 0
    map_coloring.backtrack_count = map_coloring.dfs_with_forward_checking(map_coloring.num_colors, heuristic_choice)
    end_time = time.time_ns()
    assigned_colors = []
    print("Total number of backtracks: ", map_coloring.backtrack_count)
    for colors in map_coloring.assigned_colors:
        assigned_colors.append(color_legend[colors])
    print("Colors assigned to the states in their original order: ", assigned_colors)
    print("Time taken", (end_time - start_time), 'ns')
    print()

    print("Step 3: DFS with Forward Checking and Singleton Domain Propagation:")
    print()
    map_coloring.backtrack_count = 0
    map_coloring.backtrack_count = map_coloring.dfs_with_forward_checking_singleton(map_coloring.num_colors, heuristic_choice)
    end_time = time.time_ns()
    assigned_colors = []
    print("Total number of backtracks: ", map_coloring.backtrack_count)
    for colors in map_coloring.assigned_colors:
        assigned_colors.append(color_legend[colors])
    print("Colors assigned to the states in their original order: ", assigned_colors)
    print("Time taken", (end_time - start_time), 'ns')
    print()


main()
