import time

# TODO - make the minimax function "time aware"
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
	def __init__(self, n, b, s, max_depth, max_time, recommend = True):
		self.initialize_game(n, b)
		self.recommend = recommend
		self.n = n
		self.s = s
		self.b = b
		self.max_depth = max_depth
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

	# TODO - improve algorithm to calculate longest sequence in a given array
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

	# TODO - fix this up l8er
	def is_end(self):
		# Vertical win - check all verticals
		for row in self.current_state:
			winner = self.has_s_consecutive_values(row)
			if winner:
				return winner
		# Horizontal win - check all horizontals
		for y in range(0, len(self.current_state)):
			horizontal_arr = []
			for x in range(len(self.current_state)):
				horizontal_arr.append(self.current_state[x][y])
			winner = self.has_s_consecutive_values(horizontal_arr)
			if winner:
				return winner
		# Main diagonal win TODO - bug in code, will only find middle diagonal, not any diagonal
		diagonal_arr = []
		for i in range(len(self.current_state)):
			diagonal_arr.append(self.current_state[i][i])
		winner = self.has_s_consecutive_values(diagonal_arr)
		if winner:
			return winner
		# Second diagonal win TODO - bug in code, will only find middle diagonal, not any diagonal
		second_diagonal_arr = []
		for i in range(len(self.current_state)):
			idx = len(self.current_state) - 1 - i
			second_diagonal_arr.append(self.current_state[i][idx])
		winner = self.has_s_consecutive_values(second_diagonal_arr)
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

	def minimax(self, depth=0, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:

		value = float('inf')
		if max:
			value = float('-inf')
		x = None
		y = None

		# If max depth reached, or we've reached a terminal node
		# 	then run the heuristic and return the score	
		if depth >= self.max_depth or self.is_end():
			#run heuristic on self.current_state and return score
			score = self.heuristic_e1()
			return (score, x, y)

		for i in range(0, len(self.current_state)):
			for j in range(0, len(self.current_state)):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(depth = depth + 1, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(depth = depth + 1, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
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
			# else: # algo == self.ALPHABETA
			# 	if self.player_turn == 'X':
			# 		(m, x, y) = self.alphabeta(max=False)
			# 	else:
			# 		(m, x, y) = self.alphabeta(max=True)
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
	max_depth = int(input('Enter the maximum depth for the adversarial search: '))
	max_time = int(input('Enter the maximum time (in seconds) permitted for the AI to return a move: '))
	g = Game(n, blocks, s, max_depth, max_time, recommend = True)
	g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
	# g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

