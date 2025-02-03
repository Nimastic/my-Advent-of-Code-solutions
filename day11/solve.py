def split_number(num):
    """
    Splits a number into two parts based on its length.
    Returns the left and right halves as integers.
    """
    str_num = str(num)
    mid = len(str_num) // 2
    left = int(str_num[:mid]) if str_num[:mid] else 0
    right = int(str_num[mid:]) if str_num[mid:] else 0
    return left, right

def blink(stones):
    """
    Simulates one blink of the stones.
    """
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            left, right = split_number(stone)
            new_stones.append(left)
            new_stones.append(right)
        else:
            new_stones.append(stone * 2024)
    return new_stones

def simulate_blinks(initial_stones, blinks):
    """
    Simulates a given number of blinks on the initial stones.
    """
    stones = initial_stones
    for _ in range(blinks):
        stones = blink(stones)
    return stones

# Puzzle input
initial_stones = [0, 7, 6618216, 26481, 885, 42, 202642, 8791]

# Simulate 75 blinks
final_stones = simulate_blinks(initial_stones, 75)

# Output the number of stones after 75 blinks
print("Number of stones after 75 blinks:", len(final_stones))
