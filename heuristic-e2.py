import get_directions


# current_state = [
#   ['X', '*', 'O', 'X', 'O'],
#   ['X', 'X', 'X', 'O', 'X'],
#   ['O', '*', 'X', 'O', 'X'],
#   ['O', 'O', '*', 'O', 'X'],
#   ['.', 'X', 'X', 'X', 'O']
# ]

def heuristic_e2():
  vertical = get_directions.get_verticals()
  horizontal = get_directions.get_horizontals()
  diagonal = get_directions.get_diagonals()
  secondary_diagonal = get_directions.get_secondary_diagonals()
  all_rows = [*vertical, *horizontal, *diagonal, *secondary_diagonal]

  score = 0
  for row in all_rows:
    num_x = row.count('X')
    num_o = row.count('O')

    score += num_x ** 2
    score -= num_o ** 2

  return score

print(heuristic_e2())






