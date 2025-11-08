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
        if current_puzzle.can_move("up"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.up()
            queue.append(new_puzzle)
        if current_puzzle.can_move("down"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.down()
            queue.append(new_puzzle)
        if current_puzzle.can_move("left"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.left()
            queue.append(new_puzzle)
        if current_puzzle.can_move("right"):
            new_puzzle = current_puzzle.copy()
            new_puzzle.right()
            queue.append(new_puzzle)