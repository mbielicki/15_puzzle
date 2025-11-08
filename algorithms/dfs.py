from puzzle import Puzzle


def dfs(puzzle: Puzzle) -> Puzzle:
    stack = [puzzle]
    visited = set()
    i = 0

    while stack:
        i += 1
        current_puzzle = stack.pop()
        print(f"\rDFS iteration {i}, stack size: {len(stack)}, moves: {len(current_puzzle.history)}       ", end="")
        
        if current_puzzle.is_solved():
            return current_puzzle
        if current_puzzle.__repr__() in visited:
            continue
        visited.add(current_puzzle.__repr__())

        if current_puzzle.can_move("U") and current_puzzle.previous_move() != "D":
            new_puzzle = current_puzzle.copy()
            new_puzzle.up()
            stack.append(new_puzzle)
        if current_puzzle.can_move("D") and current_puzzle.previous_move() != "U":
            new_puzzle = current_puzzle.copy()
            new_puzzle.down()
            stack.append(new_puzzle)
        if current_puzzle.can_move("L") and current_puzzle.previous_move() != "R":
            new_puzzle = current_puzzle.copy()
            new_puzzle.left()
            stack.append(new_puzzle)
        if current_puzzle.can_move("R") and current_puzzle.previous_move() != "L":
            new_puzzle = current_puzzle.copy()
            new_puzzle.right()
            stack.append(new_puzzle)