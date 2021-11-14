import time

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
		print()
		for y in range(0, len(self.current_state)):
			for x in range(0, len(self.current_state)):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > len(self.current_state) - 1 or py < 0 or py > len(self.current_state) - 1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	# TODO (maybe) - improve algorithm to calculate longest sequence in a given array
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

	def get_verticals(self):
		all_verticals = []
		for i in range(len(self.current_state)):
			all_verticals.append([row[i] for row in self.current_state])
		return all_verticals

	def get_horizontals(self):
		return [row for row in self.current_state]

	def get_diagonals(self):
		all_diagonals = []
		for k in range(len(self.current_state)*2 - 1):
			current_diagonal = []
			for j in range(k+1):
				i = k-j
				if i < len(self.current_state) and j < len(self.current_state):
					current_diagonal.append(self.current_state[i][j])
			all_diagonals.append(current_diagonal)
		return all_diagonals

	def get_secondary_diagonals(self):
		all_diagonals = []
		for k in range(len(self.current_state)*2 - 1):
			current_diagonal = []
			for j in range(k+1):
				i = k-j
				if i < len(self.current_state) and j < len(self.current_state):
					current_diagonal.append(self.current_state[j][i])
			all_diagonals.append(current_diagonal)
		return all_diagonals

	def is_end(self):
		# Vertical win
		verticals = self.get_verticals()
		for arr in verticals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Horizontal win
		horizontals = self.get_horizontals()
		for arr in horizontals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Diagonals win
		diagonals = self.get_diagonals()
		for arr in diagonals:
			winner = self.has_s_consecutive_values(arr)
			if winner:
				return winner
		# Second diagonals win
		second_diagonals = self.get_secondary_diagonals()
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
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
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
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def heuristic_e1(self):
		vertical = self.get_verticals()
		horizontal = self.get_horizontals()
		diagonal = self.get_diagonals()
		secondary_diagonal = self.get_secondary_diagonals()
		all_rows = [*vertical, *horizontal, *diagonal, *secondary_diagonal]
		score = 0
		for row in all_rows:
			num_x = row.count('X')
			num_o = row.count('O')
			score += num_x ** 2
			score -= num_o ** 2
		return score

	def heuristic_e2(self):
		vertical = self.get_verticals()
		horizontal = self.get_horizontals()
		diagonal = self.get_diagonals()
		secondary_diagonal = self.get_secondary_diagonals()
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

	def minimax(self, depth=0, max=False, simple_heuristic=True):
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

		# If max depth reached, or we've reached a terminal node
		# 	then run the heuristic and return the score	
		if (self.player_turn == 'X' and depth >= self.d1) or (self.player_turn == 'O' and depth >= self.d2) or self.is_end():
			score = self.heuristic_e1() if simple_heuristic else self.heuristic_e2()
			return (score, x, y)

		for i in range(0, len(self.current_state)):
			for j in range(0, len(self.current_state)):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(depth = depth + 1, max=False, simple_heuristic=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(depth = depth + 1, max=True, simple_heuristic=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)



	def alphabeta(self, depth=0, alpha=float('-inf'), beta=float('inf'), max=False, simple_heuristic=True):
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

		# If max depth reached, or we've reached a terminal node
		# 	then run the heuristic and return the score	
		if (self.player_turn == 'X' and depth >= self.d1) or (self.player_turn == 'O' and depth >= self.d2) or self.is_end():
			score = self.heuristic_e1() if simple_heuristic else self.heuristic_e2()
			return (score, x, y)

		for i in range(0, len(self.current_state)):
			for j in range(0, len(self.current_state)):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(depth = depth + 1, max=False, simple_heuristic=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(depth = depth + 1, max=True, simple_heuristic=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'

					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)



	def play(self,algo=None,player_x=None,player_o=None):		
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
				print(F'Evaluation time: {round(end - start, 7)}s')
				print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
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

def main():
	n = int(input('Enter size of board: '))
	blocks = create_blocks(n)
	s = int(input('Enter the number of consecutive pieces required to win: '))
	max_depth_player_1 = int(input('Enter Player 1\'s maximum depth for the adversarial search: '))
	max_depth_player_2 = int(input('Enter Player 2\'s maximum depth for the adversarial search: '))
	max_time = int(input('Enter the maximum time (in seconds) permitted for the AI to return a move: '))
	g = Game(n, blocks, s, max_depth_player_1, max_depth_player_2, max_time, recommend = True)
	
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	# g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.HUMAN)

	g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.HUMAN)
	# g.play(algo=Game.ALPHABETA,player_x=Game.HUMAN,player_o=Game.AI)
	# g.play(algo=Game.ALPHABETA,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()