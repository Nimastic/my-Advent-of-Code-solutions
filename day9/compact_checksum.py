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
        # Note: file_id might be more than a single digit if large, convert to str
        fid_str = str(file_id)
        for _ in range(f_len):
            layout.append(fid_str)
        file_id += 1
        
        # If there is a free space length after this file length, read it
        if i < len(digits):
            s_len = digits[i]
            i += 1
            layout.extend(['.'] * s_len)
    
    return layout

def is_compaction_complete(layout):
    """
    Check if there are no free spaces ('.') that have file blocks to the right.
    In other words, every '.' should appear after all file blocks.
    """
    # The condition for completion is that once we hit the first '.' from the left,
    # there should be no file block after it.
    first_dot = None
    for idx, block in enumerate(layout):
        if block == '.':
            first_dot = idx
            break
    
    if first_dot is None:
        # No free spaces at all, we are done
        return True
    
    # If there's a '.' found, ensure no file blocks after it
    for idx in range(first_dot+1, len(layout)):
        if layout[idx] != '.':
            return False
    return True

def compact_disk(layout):
    """
    Simulate the process described:
    Move file blocks one at a time from the end of the disk to the leftmost free space,
    until all free spaces are at the end with no file blocks to their right.
    """
    # Repeat until no '.' that violates the condition
    while not is_compaction_complete(layout):
        # Find the leftmost '.' that still has file blocks after it
        # (i.e., the first '.' encountered from left to right for which
        # the condition isn't satisfied)
        leftmost_dot = None
        for i in range(len(layout)):
            if layout[i] == '.':
                # Check if there's any file block after this dot
                if any(block != '.' for block in layout[i+1:]):
                    leftmost_dot = i
                    break
        
        # Find the rightmost file block
        rightmost_file_pos = None
        for i in range(len(layout)-1, -1, -1):
            if layout[i] != '.':
                rightmost_file_pos = i
                break
        
        # Move that rightmost file block to the leftmost '.' position
        block_to_move = layout[rightmost_file_pos]
        layout[leftmost_dot] = block_to_move
        layout[rightmost_file_pos] = '.'

    return layout

def calculate_checksum(layout):
    """
    Calculate the checksum: sum of position * file_id for each file block.
    Skip free spaces.
    """
    checksum = 0
    for pos, block in enumerate(layout):
        if block != '.':
            # block should be a string representing a file ID (could be more than one digit)
            fid = int(block)
            checksum += pos * fid
    return checksum

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        disk_map_str = f.read().strip()
    
    layout = parse_disk_map(disk_map_str)
    final_layout = compact_disk(layout)
    result = calculate_checksum(final_layout)
    print(result)
