import sys
from math import gcd

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Collect antenna positions by frequency
    # frequency_map: { freq_char: [(x1,y1), (x2,y2), ...], ... }
    frequency_map = {}
    for y in range(height):
        for x in range(width):
            c = grid[y][x]
            if c != '.':
                frequency_map.setdefault(c, []).append((x, y))

    antinodes = set()

    # For each frequency, find all lines formed by pairs of antennas
    for freq, coords in frequency_map.items():
        # If only one antenna for this frequency, it cannot form a line with another antenna
        # and thus no additional antinodes apart from itself. Wait, per the updated model,
        # even if there's only one antenna, it needs another to form a line, so skip.
        if len(coords) < 2:
            continue

        # Consider each pair of antennas to define a line
        # For each line, find all points on that line within the grid bounds
        # A line is defined by a direction vector (sx, sy) = (dx/g, dy/g)
        for i in range(len(coords)):
            x1, y1 = coords[i]
            for j in range(i+1, len(coords)):
                x2, y2 = coords[j]
                dx = x2 - x1
                dy = y2 - y1
                g = gcd(dx, dy)
                sx = dx // g
                sy = dy // g

                # Explore in one direction
                px, py = x1, y1
                while 0 <= px < width and 0 <= py < height:
                    antinodes.add((px, py))
                    px += sx
                    py += sy

                # Explore in the opposite direction
                px, py = x1, y1
                while 0 <= px < width and 0 <= py < height:
                    antinodes.add((px, py))
                    px -= sx
                    py -= sy

    # Additionally, in the updated model (Part Two), any antenna that shares a frequency with
    # at least one other antenna is itself also an antinode. The above logic already includes
    # all antennas on these lines, but let's ensure every antenna for frequencies that have >=2 
    # antennas is included:
    for freq, coords in frequency_map.items():
        if len(coords) > 1:
            for (x, y) in coords:
                antinodes.add((x, y))

    print(len(antinodes))

if __name__ == "__main__":
    main()
