import time
from get_directions import get_diagonals, get_directions, get_horizontals, get_secondary_diagonals, get_verticals

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
	def __init__(self, n, b, s, recommend = True):
		self.initialize_game(n, b)
		self.recommend = recommend
		self.n = n
		self.s = s
		self.b = b

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
		# Main diagonal win
		diagonal_arr = []
		for i in range(len(self.current_state)):
			diagonal_arr.append(self.current_state[i][i])
		winner = self.has_s_consecutive_values(diagonal_arr)
		if winner:
			return winner
		# Second diagonal win
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

	# TODO
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
			# if algo == self.MINIMAX:
			# 	if self.player_turn == 'X':
			# 		(_, x, y) = self.minimax(max=False)
			# 	else:
			# 		(_, x, y) = self.minimax(max=True)
			# else: # algo == self.ALPHABETA
			# 	if self.player_turn == 'X':
			# 		(m, x, y) = self.alphabeta(max=False)
			# 	else:
			# 		(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					# if self.recommend:
					# 	print(F'Evaluation time: {round(end - start, 7)}s')
						# print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			# if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						# print(F'Evaluation time: {round(end - start, 7)}s')
						# print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

	['X', '*', 'O', 'X', 'O']

	def heuristic_e2(self, current_state):
		vertical = get_directions.get_verticals()
		horizontal = get_directions.get_horizontals()
		diagonal = get_directions.get_diagonals()
		secondary_diagonal = get_directions.get_secondary_diagonals()
		rows = [*vertical, *horizontal, *diagonal, *secondary_diagonal]
		goal_rows_X=0
		goal_rows_Y=0

		for row in rows:
			for i in range(len(row)):
				if i+self.s >= len(row): # if index of current position in the row + length of consecutive characters needed for a row to be considered open for a win. is greater than or equal to the length of the row, there is no open row for a win.
					break
				for j in range(i,i+self.s+1): # from given position in the row, is there an open row for a win.
					if row[j]=='X':
						if row[j]=='Y' or row[j]=='*': 
							break
						else if i==i+self.s: # if can succesfully iterate over entire row subset, a goal row has been found.
							goal_rows_X+=1
					else:
						if row[j]=='X' or row[j]=='*': 
							break
						elif i==i+self.s: # if can succesfully iterate over entire row subset, a goal row has been found.
							goal_rows_Y+=1
		score = goal_rows_X-goal_rows_y
		return score

def main():
	n = int(input('Enter size of board: '))
	s = int(input('Enter the number of consecutive pieces required to win: '))
	b = [(0,0), (1,0)]
	g = Game(n, b, s, recommend = True)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	g.play(algo=Game.MINIMAX,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()