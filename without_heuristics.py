import time
import random

AUS_MAP = {
    0: 'Western Australia', 1: 'Northern Territory', 2: 'South Australia',
    3: 'Queensland', 4: 'New South Wales', 5: 'Victoria', 6: 'Tasmania'
}
AUS_BORDERS = {
    0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3, 4, 5], 3: [1, 2, 4],
    4: [2, 3, 5], 5: [2, 4], 6: []
}

USA_MAP = {
    0: 'Washington', 1: 'Oregon', 2: 'California', 3: 'Idaho', 4: 'Nevada', 5: 'Arizona',
    6: 'Utah', 7: 'Montana', 8: 'Wyoming', 9: 'Colorado', 10: 'New Mexico',
    11: 'North Dakota', 12: 'South Dakota', 13: 'Nebraska', 14: 'Kansas', 15: 'Oklahoma',
    16: 'Texas', 17: 'Minessota', 18: 'Iowa', 19: 'Missouri', 20: 'Arkansas',
    21: 'Lousiana', 22: 'Wisconsin', 23: 'Illinois', 24: 'Mississippi', 25: 'Michigan',
    26: 'Indiana', 27: 'Kentucky', 28: 'Tennessee', 29: 'Alabama', 30: 'Ohio',
    31: 'West Virginia', 32: 'Virgnia', 33: 'North Carolina', 34: 'South Carolina',
    35: 'Georgia', 36: 'Florida', 37: 'Pennsylvania', 38: 'Maryland', 39: 'Delaware',
    40: 'New Jersey', 41: 'New York', 42: 'Connecticut', 43: 'Hawaii', 44: 'Massachusetts',
    45: 'Rhode Island', 46: 'Vermont', 47: 'New Hamsphire', 48: 'Maine', 49: 'Alaska'
}
USA_BORDERS = {0: [3, 1], 1: [0, 3, 4, 2], 2: [1, 4, 5], 3: [0, 1, 4, 6, 8, 7], 4: [1, 2, 5, 6, 3],
                   5: [2, 4, 6, 9, 10], 6: [3, 4, 5, 10, 9, 8], 7: [3, 8, 12, 11], 8: [7, 3, 6, 9, 13, 12],
                   9: [8, 6, 5, 10, 15, 14, 13], 10: [5, 6, 9, 15, 16], 11: [7, 12, 17], 12: [11, 7, 8, 13, 18, 17],
                   13: [18, 12, 8, 9, 14, 19], 14: [13, 9, 15, 19], 15: [16, 20, 19, 14, 9, 10], 16: [10, 15, 20, 21],
                   17: [11, 12, 18, 22], 18: [17, 12, 13, 19, 23, 22], 19: [18, 13, 14, 15, 20, 27, 28, 23],
                   20: [19, 15, 16, 21, 24, 28], 21: [16, 20, 24], 22: [17, 18, 23, 25], 23: [22, 18, 19, 27, 26],
                   24: [29, 21, 28, 20], 25: [22, 26, 30], 26: [25, 23, 27, 30], 27: [26, 23, 19, 28, 32, 31, 30],
                   28: [27, 19, 20, 24, 29, 35, 33, 32], 29: [28, 24, 36, 35], 30: [25, 26, 27, 31, 37],
                   31: [30, 27, 32, 37, 38], 32: [38, 31, 27, 28, 33], 33: [32, 28, 35, 34], 34: [33, 35],
                   35: [29, 28, 33, 34, 36], 36: [29, 35], 37: [30, 31, 41, 40, 38, 39], 38: [31, 32, 39, 37],
                   39: [40, 38, 37], 40: [39, 37, 41], 41: [37, 40, 42, 44, 45, 46], 42: [40, 41, 44, 45], 43: [],
                   44: [42, 47, 41, 45, 46], 45: [44, 42], 46: [41, 44, 47], 47: [46, 44, 48], 48: [47], 49: []}

COLOR_CATALOG = {
    1: 'Red', 2: 'Brown', 3: 'Purple', 4: 'Ash',
    5: 'Cyan', 6: 'Blue', 7: 'White', 8: 'Black'
}


class RegionColoringSolver:
    def __init__(self, region_count, borders):
        self.region_count = region_count
        self.borders = borders
        self.colors = [0] * region_count
        self.backtrack_count = 0
        self.chromatic_number = 0

    def is_valid(self, region, color):
        return all(self.colors[neighbor] != color for neighbor in self.borders[region])

    def initialize_domains(self, color_count):
        return {i: {c: 2 for c in range(1, color_count + 1)} for i in range(self.region_count)}

    def initialize_tracker(self, color_count):
        return {i: {c: -1 for c in range(1, color_count + 1)} for i in range(self.region_count)}

    def greedy_color_assignment(self, color_count, domains):
        visited = set()
        for region in self.borders:
            if region not in visited:
                for color in domains[region]:
                    if self.is_valid(region, color):
                        self.colors[region] = color
                        visited.add(region)
                        break
                for neighbor in self.borders[region]:
                    if neighbor not in visited:
                        for color in domains[neighbor]:
                            if self.is_valid(neighbor, color):
                                self.colors[neighbor] = color
                                visited.add(neighbor)
                                break
        return max(self.colors)

    def calculate_chromatic_number(self, max_colors):
        domains = self.initialize_domains(max_colors)
        return self.greedy_color_assignment(max_colors, domains)

    def dfs_backtracking(self, chromatic_number, order):
        domains = self.initialize_domains(chromatic_number)
        status = {i: 10 for i in self.borders}
        parent = {i: -1 for i in self.borders}
        self.backtrack_count = 0

        def dfs(region):
            assigned = False
            status[region] = 20
            for color in domains[region]:
                if self.is_valid(region, color):
                    if not assigned:
                        self.colors[region] = color
                        domains[region][color] = 1
                        assigned = True
                else:
                    if not assigned:
                        self.backtrack_count += 1
                    domains[region][color] = 0
            if not assigned:
                return -1
            for neighbor in self.borders[region]:
                if status[neighbor] == 10:
                    parent[neighbor] = region
                    if dfs(neighbor) == -1:
                        return -1
            status[region] = 30
            return self.backtrack_count

        for region in order:
            if status[region] == 10:
                if dfs(region) == -1:
                    break
        return self.backtrack_count

    def dfs_forward_checking(self, chromatic_number, order):
        domains = self.initialize_domains(chromatic_number)
        tracker = self.initialize_tracker(chromatic_number)
        status = {i: 10 for i in self.borders}
        parent = {i: -1 for i in self.borders}
        self.backtrack_count = 0

        def dfs(region):
            assigned = False
            prev_color = -1
            status[region] = 20
            for color in domains[region]:
                if domains[region][color] == 2:
                    if not assigned:
                        self.colors[region] = color
                        domains[region][color] = 1
                        assigned = True
                        self.forward_reduce(region, color, domains, tracker)
                elif domains[region][color] == 1:
                    prev_color = color

            if assigned and prev_color != -1:
                self.forward_undo(region, prev_color, domains, tracker)

            if not assigned:
                self.backtrack_count += 1
                if parent[region] != -1:
                    dfs(parent[region])

            for neighbor in self.borders[region]:
                if status[neighbor] == 10:
                    parent[neighbor] = region
                    dfs(neighbor)
            status[region] = 30
            return self.backtrack_count

        for region in order:
            if status[region] == 10:
                dfs(region)
        return self.backtrack_count

    def dfs_singleton_forward(self, chromatic_number, order):
        domains = self.initialize_domains(chromatic_number)
        tracker = self.initialize_tracker(chromatic_number)
        status = {i: 10 for i in self.borders}
        parent = {i: -1 for i in self.borders}
        self.backtrack_count = 0

        def dfs(region):
            assigned = False
            prev_color = -1
            status[region] = 20
            for color in domains[region]:
                if domains[region][color] == 2:
                    if not assigned:
                        self.colors[region] = color
                        domains[region][color] = 1
                        assigned = True
                        self.singleton_reduce(region, color, domains, tracker)
                elif domains[region][color] == 1:
                    prev_color = color

            if assigned and prev_color != -1:
                self.singleton_undo(region, prev_color, domains, tracker)

            if not assigned:
                self.backtrack_count += 1
                if parent[region] != -1:
                    dfs(parent[region])

            for neighbor in self.borders[region]:
                if status[neighbor] == 10:
                    parent[neighbor] = region
                    dfs(neighbor)
            status[region] = 30
            return self.backtrack_count

        for region in order:
            if status[region] == 10:
                dfs(region)
        return self.backtrack_count

    def forward_reduce(self, region, color, domains, tracker):
        for neighbor in self.borders[region]:
            domains[neighbor][color] = 0
            if tracker[neighbor][color] == -1:
                tracker[neighbor][color] = region

    def forward_undo(self, region, color, domains, tracker):
        for neighbor in self.borders[region]:
            if tracker[neighbor][color] == region and domains[neighbor][color] == 0:
                domains[neighbor][color] = 2

    def singleton_reduce(self, region, color, domains, tracker):
        for neighbor in self.borders[region]:
            prev = domains[neighbor][color]
            domains[neighbor][color] = 0
            if prev == 2:
                single_color = self.singleton_check(neighbor, domains)
                if single_color > 0:
                    self.singleton_reduce(neighbor, single_color, domains, tracker)
            if tracker[neighbor][color] == -1:
                tracker[neighbor][color] = region

    def singleton_undo(self, region, color, domains, tracker):
        for neighbor in self.borders[region]:
            if tracker[neighbor][color] == region and domains[neighbor][color] == 0:
                domains[neighbor][color] = 2

    def singleton_check(self, region, domains):
        valid_colors = [c for c, v in domains[region].items() if v == 2]
        return valid_colors[0] if len(valid_colors) == 1 else 0


def main():
    start = time.time_ns()
    map_choice = input("Select map:\n1. Australia\n2. USA\n\n")
    if map_choice == '1':
        layout = AUS_MAP
        borders = AUS_BORDERS
        label = "Australia"
    elif map_choice == '2':
        layout = USA_MAP
        borders = USA_BORDERS
        label = "USA"
    else:
        print("Invalid choice.")
        return

    solver = RegionColoringSolver(len(borders), borders)
    solver.chromatic_number = solver.calculate_chromatic_number(5)
    print(f"\nChromatic number for {label}: {solver.chromatic_number}")

    order = list(range(solver.region_count))
    random.shuffle(order)

    method = input(
        "\nSelect coloring method:\n"
        "1. DFS Only\n"
        "2. DFS with Forward Checking\n"
        "3. DFS with Singleton Propagation\n\n"
    )

    if method == '1':
        solver.dfs_backtracking(solver.chromatic_number, order)
    elif method == '2':
        solver.dfs_forward_checking(solver.chromatic_number, order)
    elif method == '3':
        solver.dfs_singleton_forward(solver.chromatic_number, order)
    else:
        print("Invalid method.")
        return

    end = time.time_ns()
    assigned_colors = [COLOR_CATALOG[c] for c in solver.colors]
    print("\nColor assignments:")
    for i, color in enumerate(assigned_colors):
        print(f"{layout[i]}: {color}")
    print("\nBacktracks:", solver.backtrack_count)
    print("Time taken (ns):", end - start)


if __name__ == "__main__":
    main()
