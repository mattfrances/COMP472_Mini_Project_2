def get_verticals(current_state):
  all_verticals = []
  for i in range(len(current_state)):
    all_verticals.append([row[i] for row in current_state])
  return all_verticals

def get_horizontals(current_state):
  return [row for row in current_state]

def get_diagonals(current_state):
  all_diagonals = []
  for k in range(len(current_state)*2 - 1):
    print('k: ', k)
    current_diagonal = []
    for j in range(k+1):
      print('j: ', j)
      i = k-j
      print('i: ', i)
      print()
      if i < len(current_state) and j < len(current_state):
        current_diagonal.append(current_state[i][j])
    all_diagonals.append(current_diagonal)
  return all_diagonals

def get_secondary_diagonals(current_state):
  all_diagonals = []
  for k in range(len(current_state)*2 - 1):
    current_diagonal = []
    for j in range(k+1):
      i = k-j
      if i < len(current_state) and j < len(current_state):
        current_diagonal.append(current_state[j][i])
    all_diagonals.append(current_diagonal)
  return all_diagonals