def parse_disk_map(disk_map_str):
    """
    Parse the disk map string into a layout of file IDs and '.' for free spaces.
    The disk map has alternating file length and free space length integers.
    """
    digits = list(map(int, disk_map_str))
    layout = []
    file_id = 0
    i = 0
    while i < len(digits):
        # Read file length
        f_len = digits[i]
        i += 1
        # Append file blocks
        fid_str = str(file_id)
        for _ in range(f_len):
            layout.append(fid_str)
        file_id += 1
        
        # If there is a free space length after this file length, read it
        if i < len(digits):
            s_len = digits[i]
            i += 1
            layout.extend(['.'] * s_len)
    
    return layout, file_id

def find_file_positions(layout, fid_str):
    """
    Given the layout and a file ID string (e.g., '0', '1', '10'), 
    return the start and end indices (inclusive) of that file's contiguous block.
    Assumes each file is contiguous as per the initial conditions and no partial moves.
    """
    positions = [i for i, block in enumerate(layout) if block == fid_str]
    if not positions:
        return None, None
    return min(positions), max(positions)

def find_leftmost_free_space(layout, length_needed, right_bound):
    """
    Find the leftmost contiguous free space block ('.') to the left of 'right_bound' 
    that can fit 'length_needed' blocks.
    
    'right_bound' is typically the start index of the file we're trying to move,
    meaning we only look at positions < right_bound.
    
    We scan from left to right for a run of '.' of at least length_needed that lies entirely to the left of right_bound.
    Return the start index of that free space segment if found, otherwise None.
    """
    count = 0
    start_index = None
    for i in range(right_bound):
        if layout[i] == '.':
            if start_index is None:
                start_index = i
            count += 1
            if count >= length_needed:
                # Found a suitable segment
                # The segment runs from start_index to i
                return start_index
        else:
            # Reset the count and start
            count = 0
            start_index = None
    return None

def move_file(layout, fid_str, start, end, target_start):
    """
    Move the file (all its blocks from start to end indices) into the free space 
    starting at target_start.
    
    Steps:
    - Extract the file blocks
    - We'll have to shift blocks to the right to open space at target_start
      equal to the file's length.
    - Insert the file blocks at target_start
    - The original file location becomes '.' free space.
    """
    file_blocks = layout[start:end+1]
    file_length = len(file_blocks)
    
    # Remove the file from its current position
    for i in range(start, end+1):
        layout[i] = '.'
    
    # Now we have a free space of at least file_length at target_start (guaranteed by earlier check).
    # But we must ensure we don't overwrite any files that might be there after shifting.
    # Actually, since we're moving into a known contiguous free space segment, it means
    # at the moment of finding that segment, it was entirely '.'.
    # However, the file could be "jumping" over other files if there's no overlap?
    # Wait, by definition we found a contiguous run of '.' at target_start of at least file_length.
    # To place the file there, we just overwrite those '.' with the file blocks.
    # No shifting of other blocks is needed because we specifically searched for a free segment of '.'.
    
    for i in range(file_length):
        layout[target_start + i] = file_blocks[i]

def compact_part2(layout, file_count):
    """
    Implement Part Two compaction:
    - Consider files in decreasing order of file ID.
    - Try to move each file once, if possible.
    """
    # File IDs go from 0 to file_count-1
    # Decreasing order means we start from file_count-1 down to 0
    for fid in range(file_count-1, -1, -1):
        fid_str = str(fid)
        start, end = find_file_positions(layout, fid_str)
        if start is None:
            # File not found (possibly length zero?), skip
            continue
        
        file_length = (end - start + 1)
        
        # Find a suitable free space to the left
        # The problem states: attempt to move whole files to the leftmost span of free spaces that can fit it
        # We only consider free spaces to the left of the file's current start.
        target_start = find_leftmost_free_space(layout, file_length, start)
        
        if target_start is not None:
            # Move the file
            move_file(layout, fid_str, start, end, target_start)
        # If no suitable space, do nothing

def calculate_checksum(layout):
    """
    Calculate the checksum: sum of position * file_id for each file block.
    """
    checksum = 0
    for pos, block in enumerate(layout):
        if block != '.':
            fid = int(block)
            checksum += pos * fid
    return checksum

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        disk_map_str = f.read().strip()
    
    layout, file_count = parse_disk_map(disk_map_str)
    compact_part2(layout, file_count)
    result = calculate_checksum(layout)
    print(result)
