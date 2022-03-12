import numpy as np
import re
from wordfreq import word_frequency

words_file = open("wordle_words_all.txt", "r")
content = words_file.read()
words_list = content.split("\n")
words_file.close()

alphabet = "abcdefghijklmnopqrstuvwxyz"
alpha_dict = {}
for letter in alphabet:
	alpha_dict[letter] = 0
	
for word in words_list:
	for letter in word:
		alpha_dict[letter] += 1
		
print(alpha_dict)

frequencies = {}
total_letters = len(words_list) * 5
for letter in alpha_dict:
	frequencies[letter] = alpha_dict[letter] / total_letters

print(frequencies)
	
class wordle():
	def __init__(self):
		self.pools = [[], [], [], [], []]
		for pool in self.pools:
			pool[:] = alphabet
		self.guesses = []
		self.options = []
		self.guess = ""
		self.result = ""
		self.grep = "....."
		self.in_word = []
		self.noptions = 0
		
	def __repr__(self):
		return "x: incorrect\n?: letter in word, but wrong location\n=: correct"
		
	def updatepool(self):
		i = 0
		for char in self.result:
			if char == "x":
				for pool in self.pools:
					try:
						pool.remove(self.guess[i])
					except:
						pass
			if char == "?":
				self.pools[i].remove(self.guess[i])
			i += 1
			
		
	def result2grep(self):
		grep = r""
		i = 0
		for char in self.result:
			if char == "=":
				grep += self.guess[i]
				self.in_word.append(self.guess[i])
			elif char == "x":
				grep += "[" + "".join(self.pools[i]) + "]"
			elif char == "?":
				grep += "[" + "".join(self.pools[i]) + "]"
				self.in_word.append(self.guess[i])
				print(letter)
			i += 1
		return grep
		
	def getoptions(self):
		return filter(lambda x: re.search(self.grep, x), words_list)
	
	def freq_score(self, word):
		raw_score = np.sum([frequencies[letter] for letter in "".join(set(word))])
		return raw_score
		
	def all_in(self, word):
		for letter in self.in_word:
			if letter not in word:
				return False
		return True
		
	def bestoption(self):
		best = ""
		best_score = 0
		self.noptions = 0
		self.total_frequency = 0
		for option in self.options:
			if self.all_in(option):
				option_score = self.freq_score(option)
				if len(self.guesses) == 5:
					option_score += 20000 * word_frequency(option, 'en')
				elif len(self.guesses) > 1:
					option_score += 1000 * word_frequency(option, 'en') * len(self.guesses)
				self.total_frequency += word_frequency(option, 'en')
				print(option, option_score)
				if option_score > best_score:
					best = option
					best_score = option_score
				self.noptions += 1
		return best
		
	def getconfidence(self):
		return word_frequency(self.guess, 'en') / self.total_frequency
		
	def turn(self):
		self.options = self.getoptions()
		self.guess = self.bestoption()
		print(self)
		print("Guess:", self.guess, "Confidence:", self.getconfidence() * 100, "%")
		self.guesses.append(self.guess)
		self.result = input("Result: ")
		if self.result == "NIWL":
			words_list.remove(self.guess)
			self.turn()
		else:
			self.play()
		
	def play(self, fail=True):
		if len(self.guesses) == 0:
			self.turn()
		elif self.result == "=====":
			print("Win in", len(self.guesses), "tries!")
		elif len(self.guesses) >= 6 and fail == True:
			print("Failure... I am so sorry to have let you down :(")
		else:
			self.updatepool()
			self.grep = self.result2grep()
			self.turn()
			
if __name__ == "__main__":
	game = wordle()
	game.play()
