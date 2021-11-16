import time
import os.path
from get_directions import *
from calculations_helpers import *

count_wins_e1 = 0
count_wins_e2 = 0
sb_eval_time = 0
sb_total_heuristic_evals = 0

sb_player_name_x = ''
sb_player_name_O = ''
sb_type_of_search = ''
sb_type_of_heuristic_player_x = ''
sb_type_of_heuristic_player_y = ''

avg_eval_time = 0
tot_heur_evals = 0
evals_depth = 0
tot_moves = 0
avg_evals_depth = 0


class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	"""
	Params
	n: size of the board
	b: array of indices of integer tuples for blocks
	s: consecutive pieces required to win the game
	"""
	def __init__(self, n, b, s, d1, d2, max_time, recommend = True):
		self.initialize_game(n, b)
		self.recommend = recommend
		self.n = n
		self.s = s
		self.b = b
		self.d1 = d1
		self.d2 = d2
		self.max_time = max_time
		self.buffer_time = 0.005
		self.num_of_heuristic_evaluations_for_current_turn = 0
		self.total_num_of_heuristic_evaluations = 0
		self.evaluation_times = []
		self.total_num_of_heuristic_evaluations
		self.current_depth=0
		self.num_of_heuristic_evaluations_at_current_depth = 0
		self.heuristic_evaluations_by_depth_for_current_turn = []
		self.heuristic_data_for_all_moves = []
		self.total_moves=0
		self.player_x_heuristic = True
		self.player_y_heuristic = False
		self.avg_recusive_depths = []

	def initialize_game(self,n,b):
		tempMatrix = []
		for i in range(0,n):
			row = []
			for j in range(0,n):
				row.append('.')
			tempMatrix.append(row)
		for block in b:
			tempMatrix[block[0]][block[1]] = '*'
		self.current_state = tempMatrix

		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
			print(F'\n(move #{self.total_moves})')
			f.write(F'\n(move #{self.total_moves})\n')

			print()
			f.write('\n')

			for y in range(0, len(self.current_state)):
				for x in range(0, len(self.current_state)):
					with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
						print(F'{self.current_state[x][y]}', end="")
						f.write(F'{self.current_state[x][y]}')
				with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
					print()
					f.write('\n')
			with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
				print()
				f.write('\n')
		
	def is_valid(self, px, py):
		if px < 0 or px > len(self.current_state) - 1 or py < 0 or py > len(self.current_state) - 1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def has_s_consecutive_values(self, arr):
		largest_count = 0
		largest_count_char = ''

		for i in range(len(arr) - self.s + 1):
			if arr[i] != 'X' and arr[i] != 'O':
				continue
			sub_array = arr[i:i+self.s]
			current_char = sub_array[0]
			count = 1
			for j in range(1, len(sub_array)):
				if sub_array[j] == current_char:
					count += 1
				else:
					if count > largest_count:
						largest_count = count
						largest_count_char = current_char
						break
			if count > largest_count:
				largest_count = count
				largest_count_char = current_char
						
		if largest_count >= self.s:
			return largest_count_char
		else:
			return None

	def is_end(self):
		# Vertical win
		verticals = get_verticals(self.current_state)
		for arr in verticals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Horizontal win
		horizontals = get_horizontals(self.current_state)
		for arr in horizontals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Diagonals win
		diagonals = get_diagonals(self.current_state)
		for arr in diagonals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Second diagonals win
		second_diagonals = get_secondary_diagonals(self.current_state)
		for arr in second_diagonals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Is whole board full?
		for row in self.current_state:
			for item in row:
				if (item == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':

				global count_wins_e1
				count_wins_e1 += 1
				with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}', 'a') as f:
					print('The winner is X!')
					f.write('The winner is X!\n')
			elif self.result == 'O':
				global count_wins_e2
				count_wins_e2 += 1
				with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}', 'a') as f:
					print('The winner is O!')
					f.write('The winner is O!\n')
			elif self.result == '.':
				with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
					print("It's a tie!")
					f.write("It's a tie!")

			global tot_moves
			tot_moves += self.total_moves

			global avg_eval_time
			avg_eval_time += calculate_average_evaluation_time(self.evaluation_times)

			global tot_heur_evals
			tot_heur_evals += self.total_num_of_heuristic_evaluations

			global evals_depth 
			evals_depth  = calculate_evaluations_by_depth(self.heuristic_data_for_all_moves)

			with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}', 'a') as f:
				print(F'6(b)i   Average evaluation time: {calculate_average_evaluation_time(self.evaluation_times)}')
				f.write(F'6(b)i   Average evaluation time: {calculate_average_evaluation_time(self.evaluation_times)}\n')

				print(F'6(b)ii  Total heuristic evaluations: {self.total_num_of_heuristic_evaluations}')
				f.write(F'6(b)ii  Total heuristic evaluations: {self.total_num_of_heuristic_evaluations}\n')

				print(F'6(b)iv Evaluations by depth: {format_heuristic_evaluations_by_depth(calculate_evaluations_by_depth(self.heuristic_data_for_all_moves))}')
				f.write(F'6(b)iv Evaluations by depth: {format_heuristic_evaluations_by_depth(calculate_evaluations_by_depth(self.heuristic_data_for_all_moves))}\n')

				print(F'6(b)v Average of the per-move average recursion depth: {sum(self.avg_recusive_depths) / len(self.avg_recusive_depths)}')
				f.write(F'6(b)v Average of the per-move average recursion depth: {sum(self.avg_recusive_depths) / len(self.avg_recusive_depths)}\n')

				print(F'6(b)vi  Total moves: {self.total_moves}')
				f.write(F'6(b)vi  Total moves: {self.total_moves}\n')
			self.initialize_game(self.n, self.b)
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		self.total_moves+=1
		self.heuristic_data_for_all_moves.append(self.heuristic_evaluations_by_depth_for_current_turn)
		self.total_num_of_heuristic_evaluations += self.num_of_heuristic_evaluations_for_current_turn
		self.current_depth=0
		self.num_of_heuristic_evaluations_at_current_depth = 0
		self.heuristic_evaluations_by_depth_for_current_turn = []
		self.num_of_heuristic_evaluations_for_current_turn = 0
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def heuristic_e1(self):
		self.num_of_heuristic_evaluations_for_current_turn+=1
		vertical = get_verticals(self.current_state)
		horizontal = get_horizontals(self.current_state)
		diagonal = get_diagonals(self.current_state)
		secondary_diagonal = get_secondary_diagonals(self.current_state)
		all_rows = [*vertical, *horizontal, *diagonal, *secondary_diagonal]
		score = 0
		for row in all_rows:
			num_x = row.count('X')
			num_o = row.count('O')
			score += num_x ** 2
			score -= num_o ** 2
		return score

	def heuristic_e2(self):
		self.num_of_heuristic_evaluations_for_current_turn+=1
		vertical = get_verticals(self.current_state)
		horizontal = get_horizontals(self.current_state)
		diagonal = get_diagonals(self.current_state)
		secondary_diagonal = get_secondary_diagonals(self.current_state)
		all_rows = [*vertical, *horizontal, *diagonal, *secondary_diagonal]
		goal_rows_X=0
		goal_rows_Y=0

		for row in all_rows:
			for i in range(len(row)):
				if i+self.s >= len(row): # if index of current position in the row + length of consecutive characters needed for a row to be considered open for a win. is greater than or equal to the length of the row, there is no open row for a win.
					break
				for j in range(i,i+self.s+1): # from given position in the row, is there an open row for a win.
					if row[j]=='X':
						if row[j]=='Y' or row[j]=='*': 
							break
						elif i==i+self.s: # if can succesfully iterate over entire row subset, a goal row has been found.
							goal_rows_X+=1
					else:
						if row[j]=='X' or row[j]=='*': 
							break
						elif i==i+self.s: # if can succesfully iterate over entire row subset, a goal row has been found.
							goal_rows_Y+=1

		score = goal_rows_X-goal_rows_Y
		return score

	def minimax(self, start_time, depth=0, max=False, simple_heuristic=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to inf or -inf as worse than the worst case:

		value = float('inf')
		if max:
			value = float('-inf')
		x = None
		y = None

		# If max depth or time is reached, or we've reached a terminal node
		# 	then run the heuristic and return the score
		if(self.current_depth!=depth):
			self.num_of_heuristic_evaluations_at_current_depth = 0
		self.current_depth = depth

		# Initializing array containing all information related to heuristic evaluations for a single turn.
		if(self.current_depth == len(self.heuristic_evaluations_by_depth_for_current_turn)): 
			self.heuristic_evaluations_by_depth_for_current_turn.append(self.num_of_heuristic_evaluations_at_current_depth)
		else:
			self.heuristic_evaluations_by_depth_for_current_turn[self.current_depth] = self.num_of_heuristic_evaluations_at_current_depth

		time_spent = (time.time() - start_time) + self.buffer_time
		if (time_spent >= self.max_time) or (self.player_turn == 'X' and depth >= self.d1) or (self.player_turn == 'O' and depth >= self.d2) or self.is_end():
			self.num_of_heuristic_evaluations_at_current_depth += 1
			self.heuristic_evaluations_by_depth_for_current_turn[self.current_depth] = self.num_of_heuristic_evaluations_at_current_depth
			score = self.heuristic_e1() if simple_heuristic else self.heuristic_e2()
			return (score, x, y, depth)

		children_depths = []
		for i in range(0, len(self.current_state)):
			for j in range(0, len(self.current_state)):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _, avg_depth) = self.minimax(start_time, depth = depth + 1, max=False, simple_heuristic=self.player_y_heuristic)
						children_depths.append(avg_depth)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _, avg_depth) = self.minimax(start_time, depth = depth + 1, max=True, simple_heuristic=self.player_x_heuristic)
						children_depths.append(avg_depth)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'

		avg_children_depth = sum(children_depths) / len(children_depths)
		return (value, x, y, avg_children_depth)



	def alphabeta(self, start_time, alpha=float('-inf'), beta=float('inf'), depth=0, max=False, simple_heuristic=True):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to inf or -inf as worse than the worst case:
		value = float('inf')
		if max:
			value = float('-inf')
		x = None
		y = None

		# If max depth or time is reached, or we've reached a terminal node
		# 	then run the heuristic and return the score
		if(self.current_depth!=depth):
			self.num_of_heuristic_evaluations_at_current_depth = 0
		self.current_depth = depth

		# Initializing array containing all information related to heuristic evaluations for a single turn.
		if(self.current_depth == len(self.heuristic_evaluations_by_depth_for_current_turn)): 
			self.heuristic_evaluations_by_depth_for_current_turn.append(self.num_of_heuristic_evaluations_at_current_depth)
		else:
			self.heuristic_evaluations_by_depth_for_current_turn[self.current_depth] = self.num_of_heuristic_evaluations_at_current_depth

		time_spent = (time.time() - start_time) + self.buffer_time
		if (time_spent >= self.max_time) or (self.player_turn == 'X' and depth >= self.d1) or (self.player_turn == 'O' and depth >= self.d2) or self.is_end():
			self.num_of_heuristic_evaluations_at_current_depth += 1
			self.heuristic_evaluations_by_depth_for_current_turn[self.current_depth] = self.num_of_heuristic_evaluations_at_current_depth
			score = self.heuristic_e1() if simple_heuristic else self.heuristic_e2()
			return (score, x, y, depth)

		children_depths = []
		for i in range(0, len(self.current_state)):
			for j in range(0, len(self.current_state)):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _, avg_depth) = self.alphabeta(start_time, alpha, beta, depth = depth + 1, max=False, simple_heuristic=False)
						children_depths.append(avg_depth)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _, avg_depth) = self.alphabeta(start_time, alpha, beta, depth = depth + 1, max=True, simple_heuristic=True)
						children_depths.append(avg_depth)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'

					if max: 
						if value >= beta:
							return (value, x, y, avg_depth)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y, avg_depth)
						if value < beta:
							beta = value
		avg_children_depth = sum(children_depths) / len(children_depths)
		return (value, x, y, avg_children_depth)

	def play(self,algo=None,player_x=None,player_o=None):	
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		
		player_name_x = 'Human' if player_x == self.HUMAN else 'AI'
		player_name_O = 'Human' if player_o == self.HUMAN else 'AI'
		type_of_search = 'True' if algo==self.alphabeta else 'False'
		type_of_heuristic_player_x = 'e1(regular)' if self.player_x_heuristic==True else 'e2(defensive)'
		type_of_heuristic_player_y = 'e1(regular)' if self.player_y_heuristic==True else 'e2(defensive)'

		global sb_player_name_x
		global sb_player_name_O
		global sb_type_of_search
		global sb_type_of_heuristic_player_x
		global sb_type_of_heuristic_player_y
		sb_player_name_x = 'Human' if player_x == self.HUMAN else 'AI'
		sb_player_name_O = 'Human' if player_o == self.HUMAN else 'AI'
		sb_type_of_search = 'True' if algo==self.alphabeta else 'False'
		sb_type_of_heuristic_player_x = '(regular)' if self.player_x_heuristic==True else '(defensive)'
		sb_type_of_heuristic_player_y = '(regular)' if self.player_y_heuristic==True else '(defensive)'

		with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}', 'a') as f:
			print(F'\nn={self.n} b={len(self.b)} s={self.s} t={self.max_time}')
			f.write(F'\nn={self.n} b={len(self.b)} s={self.s} t={self.max_time}\n')

			print(F'blocks={self.b}')
			f.write(F'blocks={self.b}\n')

			print(F'Player 1: {player_name_x} d={self.d1} a={type_of_search} {type_of_heuristic_player_x}')
			f.write(F'Player 1: {player_name_x} d={self.d1} a={type_of_search} {type_of_heuristic_player_x}\n')

			print(F'Player 2: {player_name_O} d={self.d2} a={type_of_search} {type_of_heuristic_player_y}')
			f.write(F'Player 2: {player_name_O} d={self.d2} a={type_of_search} {type_of_heuristic_player_y}\n')

		# with open('scoreboard.txt', 'a') as fl:
		# 	fl.write(F'n={self.n} b={len(self.b)} s={self.s} t={self.max_time}\n')
		# 	f.write(F'Player 1: {player_name_x} d={self.d1} a={type_of_search}
		# 	f.write(F'Player 2: {player_name_O} d={self.d2} a={type_of_search}

		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y, avg_recursive_depth) = self.minimax(start_time=start, max=False)
				else:
					(_, x, y, avg_recursive_depth) = self.minimax(start_time=start, max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y, avg_recursive_depth) = self.alphabeta(start_time=start, max=False)
				else:
					(m, x, y, avg_recursive_depth) = self.alphabeta(start_time=start, max=True)
			end = time.time()
			evaluation_time = round(end - start, 7)
			self.evaluation_times.append(evaluation_time)
			self.avg_recusive_depths.append(avg_recursive_depth)
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:

						with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}', 'a') as f:
							print(F'Recommended move: x = {x}, y = {y}')
							f.write(F'Recommended move: x = {x}, y = {y}\n')

							print(F'i   Evaluation time: {evaluation_time}s')
							f.write(F'i   Evaluation time: {evaluation_time}s\n')

							print(F'ii  Heuristic evaluations: {self.num_of_heuristic_evaluations_for_current_turn}')
							f.write(F'ii  Heuristic evaluations: {self.num_of_heuristic_evaluations_for_current_turn}\n')

							print(F'iii Evaluations by depth: {format_heuristic_evaluations_by_depth(self.heuristic_evaluations_by_depth_for_current_turn)}')
							f.write(F'iii Evaluations by depth: {format_heuristic_evaluations_by_depth(self.heuristic_evaluations_by_depth_for_current_turn)}\n')

							print(F'iv Average evaluation depth: {calculate_average_depth_of_heuristic_evaluation_tree(self.heuristic_evaluations_by_depth_for_current_turn)}')
							f.write(F'iv Average evaluation depth: {calculate_average_depth_of_heuristic_evaluation_tree(self.heuristic_evaluations_by_depth_for_current_turn)}\n')

							print(F'v Average recursion depth: {avg_recursive_depth}')
							f.write(F'v Average recursion depth: {avg_recursive_depth}\n')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
				with open(F'gameTrace={self.n}{len(self.b)}{self.s}{self.max_time}.txt', 'a') as f:
					print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
					f.write(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}\n')

					print(F'i   Evaluation time: {evaluation_time}s')
					f.write(F'i   Evaluation time: {evaluation_time}s\n')

					print(F'ii  Heuristic evaluations: {self.num_of_heuristic_evaluations_for_current_turn}')
					f.write(F'ii  Heuristic evaluations: {self.num_of_heuristic_evaluations_for_current_turn}\n')

					print(F'iii Evaluations by depth: {format_heuristic_evaluations_by_depth(self.heuristic_evaluations_by_depth_for_current_turn)}')
					f.write(F'iii Evaluations by depth: {format_heuristic_evaluations_by_depth(self.heuristic_evaluations_by_depth_for_current_turn)}\n')

					print(F'iv Average evaluation depth: {calculate_average_depth_of_heuristic_evaluation_tree(self.heuristic_evaluations_by_depth_for_current_turn)}')
					f.write(F'iv Average evaluation depth: {calculate_average_depth_of_heuristic_evaluation_tree(self.heuristic_evaluations_by_depth_for_current_turn)}\n')

					print(F'v Average recursion depth: {avg_recursive_depth}')
					f.write(F'v Average recursion depth: {avg_recursive_depth}\n')

			self.current_state[x][y] = self.player_turn
			self.switch_player()

def create_blocks(board_size):
	num_b = int(input('Enter the number of blocks: '))
	blocks = []
	while len(blocks) < num_b:
		x = int(input(F'Enter the x coordinate of Block_{len(blocks)}: '))
		if x < 0 or x > board_size - 1:
			print('The index entered is out of bounds, please try again')
			continue
		y = int(input(F'Enter the y coordinate of Block_{len(blocks)}: '))
		if y < 0 or y > board_size - 1:
			print('The index entered is out of bounds, please try again')
			continue
		blocks.append((x, y))

	return blocks

r_games = 2
def main():
	n = int(input('Enter size of board: '))
	blocks = create_blocks(n)
	s = int(input('Enter the number of consecutive pieces required to win: '))
	max_depth_player_1 = int(input('Enter Player 1\'s maximum depth for the adversarial search: '))
	max_depth_player_2 = int(input('Enter Player 2\'s maximum depth for the adversarial search: '))
	max_time = int(input('Enter the maximum time (in seconds) permitted for the AI to return a move: '))
	g = Game(n, blocks, s, max_depth_player_1, max_depth_player_2, max_time, recommend = True)


	for i in range(r_games*2):
		g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)

	if os.path.exists('scoreboard.txt'): 
		open('scoreboard.txt', 'w').close()
	with open('scoreboard.txt', 'a') as fl:
		fl.write(F'n={g.n} b={len(g.b)} s={g.s} t={g.max_time}\n')
		fl.write(F'Player 1: {sb_player_name_x} d={g.d1} a={sb_type_of_search}\n')
		fl.write(F'Player 2: {sb_player_name_O} d={g.d2} a={sb_type_of_search}\n\n')
		fl.write(F'{r_games} games\n\n')
		fl.write(F'Total wins for heuristic e1: {count_wins_e1} ({100*count_wins_e1/(r_games*2)}%) {sb_type_of_heuristic_player_x}\n')
		fl.write(F'Total wins for heuristic e2: {count_wins_e2} ({100*count_wins_e2/(r_games*2)}%) {sb_type_of_heuristic_player_y} \n')
		
		fl.write(F'i   Average evaluation time: {avg_eval_time/(2*r_games)} \n')
		fl.write(F'ii  Total heuristic evaluations: {tot_heur_evals/(2*r_games)} \n')
		#fl.write(F'iii Evaluations by depth: {evals_depth/(2*r_games)} \n')
		fl.write(F'iv  Average evaluation depth: {avg_evals_depth/(2*r_games)} \n')
		fl.write(F'vi  Average moves per game: {tot_moves/(2*r_games)} \n')
		
	
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	# g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.HUMAN)

	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.HUMAN)
	# g.play(algo=Game.ALPHABETA,player_x=Game.HUMAN,player_o=Game.AI)
	# g.play(algo=Game.ALPHABETA,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()