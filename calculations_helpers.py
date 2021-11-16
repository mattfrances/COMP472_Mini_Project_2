def format_heuristic_evaluations_by_depth(depth_data):
  text = '{'
  for i in range(len(depth_data)):
    if(depth_data[i]==0):
      continue
    last_character = ', ' if i!=len(depth_data)-1 else ''
    text += F'{i+1}: {depth_data[i]}{last_character}'
  text += '}'
  return text

def calculate_average_depth_of_heuristic_evaluation_tree(depth_data):
  running_sum = 0
  running_product = 0
  for i in range(len(depth_data)):
    running_sum+=depth_data[i]
    running_product += i*depth_data[i]
  average_depth = running_product/running_sum
  return average_depth

# TO DO
def calculate_average_recursion_depth_at_current_state(depth_data):
  return

def calculate_average_evaluation_time(time_data):
  running_sum = 0
  for i in range(len(time_data)):
    running_sum += time_data[i]
  average = running_sum/len(time_data)
  return average

def calculate_evaluations_by_depth(heuristic_data_for_all_moves):
  evaluations_by_depth = []

  for turn in range(len(heuristic_data_for_all_moves)):
    for heuristic_evaluation in range(len(heuristic_data_for_all_moves[turn])):
      if(heuristic_evaluation == len(evaluations_by_depth)):
        evaluations_by_depth.append(heuristic_data_for_all_moves[turn][heuristic_evaluation])
      else:
        evaluations_by_depth[heuristic_evaluation] += heuristic_data_for_all_moves[turn][heuristic_evaluation]

  return evaluations_by_depth
