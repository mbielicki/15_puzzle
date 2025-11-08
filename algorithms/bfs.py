from puzzle import Puzzle

def bfs(puzzle: Puzzle) -> Puzzle:
    queue = [puzzle]
    i = 0

    while queue:
        i+= 1
        print(f"\rBFS iteration {i}, queue size: {len(queue)}       ", end="")
        current_puzzle = queue.pop(0)
        if current_puzzle.is_solved():
            return current_puzzle
        if current_puzzle.can_move("U"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.up()
            queue.append(new_puzzle)
        if current_puzzle.can_move("D"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.down()
            queue.append(new_puzzle)
        if current_puzzle.can_move("L"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.left()
            queue.append(new_puzzle)
        if current_puzzle.can_move("R"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.right()
            queue.append(new_puzzle)