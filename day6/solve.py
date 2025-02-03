def turn_right(direction):
    return (direction + 1) % 4

def forward(x, y, direction):
    if direction == 0:   # up
        return x, y-1
    elif direction == 1: # right
        return x+1, y
    elif direction == 2: # down
        return x, y+1
    elif direction == 3: # left
        return x-1, y

def can_move(grid, x, y):
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == '.'

def simulate_guard(grid, start_x, start_y, start_dir):
    x, y, direction = start_x, start_y, start_dir
    visited_states = set()
    visited_positions = set()
    visited_positions.add((x,y))

    while True:
        state = (x, y, direction)
        if state in visited_states:
            return 'loop', visited_positions
        visited_states.add(state)

        nx, ny = forward(x, y, direction)
        # Check if leaving the map
        if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
            return 'exit', visited_positions

        if grid[ny][nx] == '#':
            direction = turn_right(direction)
            continue
        else:
            x, y = nx, ny
            visited_positions.add((x, y))

def find_loop_obstruction_positions(grid, guard_x, guard_y, guard_dir):
    loop_positions = []
    height = len(grid)
    width = len(grid[0])
    mod_grid = [list(row) for row in grid]

    for y in range(height):
        for x in range(width):
            if (x,y) == (guard_x, guard_y):
                continue
            if mod_grid[y][x] == '.':
                mod_grid[y][x] = '#'
                result, _ = simulate_guard(mod_grid, guard_x, guard_y, guard_dir)
                if result == 'loop':
                    loop_positions.append((x,y))
                mod_grid[y][x] = '.'

    return loop_positions

def parse_grid(raw_grid):
    directions_map = {'^':0,'>':1,'v':2,'<':3}
    guard_x = guard_y = guard_dir = None
    grid = []
    for y, line in enumerate(raw_grid):
        row = list(line)
        for x, ch in enumerate(row):
            if ch in directions_map:
                guard_x, guard_y = x, y
                guard_dir = directions_map[ch]
                row[x] = '.'  # Replace guard symbol with floor
        grid.append("".join(row))
    return grid, guard_x, guard_y, guard_dir

if __name__ == "__main__":
    # Read input from input.txt
    with open("input.txt", "r") as f:
        raw_grid = [line.rstrip("\n") for line in f]

    grid, gx, gy, gdir = parse_grid(raw_grid)
    loop_positions = find_loop_obstruction_positions(grid, gx, gy, gdir)
    print("Number of possible positions for obstruction:", len(loop_positions))
