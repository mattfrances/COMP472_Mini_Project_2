import random
import glob
from line_em_up import Game

def random_blocks_generator(matrix_size, num_of_blocks):
  blocks = []
  # Note: for performance reasons, we will always generate the same number of blocks as matrix size
  i = 0
  while i < num_of_blocks:
    x = random.randint(0, matrix_size-1)
    y = random.randint(0, matrix_size-1)
    if [x,y] not in blocks:
      blocks.append([x,y])
      i+=1
  return blocks

configurations = [
  {
    'n': 4,
    'b': [(0,0),(0,3),(3,0),(3,3)],
    's': 3,
    't': 5,
    'd1': 6,
    'd2': 6,
    'algo': Game.MINIMAX,
  },
  {
    'n': 4,
    'b': [(0,0),(0,3),(3,0),(3,3)],
    's': 3,
    't': 1,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 5,
    'b': 4,
    's': 4,
    't': 1,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 5,
    'b': 4,
    's': 4,
    't': 5,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 8,
    'b': 5,
    's': 5,
    't': 1,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 8,
    'b': 5,
    's': 5,
    't': 5,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 8,
    'b': 6,
    's': 5,
    't': 1,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
  {
    'n': 8,
    'b': 6,
    's': 5,
    't': 5,
    'd1': 6,
    'd2': 6,
    'algo': Game.ALPHABETA,
  },
]

def main():
  # for each game config
  for item in configurations:
    # run the game 10 times
    for i in range(10):
      blocks = item['b'] if isinstance(item['b'], list) else random_blocks_generator(item['n'], item['b'])
      g = Game(item['n'], blocks, item['s'], item['d1'], item['d2'], item['t'], recommend = True)
      g.play(algo=item['algo'],player_x=Game.AI,player_o=Game.AI)

  # append all txt files to scoreboard.txt
  txt_files = glob.glob('*.txt')
  with open("scoreboard.txt", "wb") as outputFile:
    for f in txt_files:
        with open(f, "rb") as inputFile:
            outputFile.write(F'FILE NAME: {f}\n\n')
            outputFile.write(inputFile.read())
            outputFile.write('\n\n\n\n\n\n\n\n\n')

if __name__ == "__main__":
  main()