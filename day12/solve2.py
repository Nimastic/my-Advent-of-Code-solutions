from collections import deque

def parse_map(input_text):
    return [list(line.strip()) for line in input_text.splitlines()]

def find_region(grid, x, y, visited):
    rows, cols = len(grid), len(grid[0])
    plant_type = grid[x][y]
    queue = deque([(x, y)])
    visited[x][y] = True

    area = 0
    sides = 0

    while queue:
        cx, cy = queue.popleft()
        area += 1

        # Check all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == plant_type:
                    if not visited[nx][ny]:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
                else:
                    sides += 1
            else:
                # Edge of the grid contributes to sides
                sides += 1

    return area, sides

def calculate_total_cost(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    total_cost = 0

    for x in range(rows):
        for y in range(cols):
            if not visited[x][y]:
                area, sides = find_region(grid, x, y, visited)
                total_cost += area * sides

    return total_cost

# Read input file
with open('./input.txt', 'r') as file:
    input_text = file.read()

# Process the map
garden_map = parse_map(input_text)

# Calculate the total cost
total_cost = calculate_total_cost(garden_map)

print("Total cost of fencing all regions:", total_cost)
