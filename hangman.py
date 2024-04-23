alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R",
            "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "-"]
empty_dict = {letter: 0 for letter in alphabet}


def pick_word():
    res = input("Pick your target word: ").upper()
    problem = True if len(res) == 0 else False
    for checked in range(len(res)):
        if res[checked] not in alphabet:
            problem = True
    if problem:
        print("Invalid input. Try again.")
        return pick_word()
    return res


game_over = 6
spacing = " " * game_over * 2


def load_gun(shots):  # I opted for ASCII art
    if shots < 0 or shots > game_over:
        raise ValueError("This is overkill")
    print(",----" + spacing + " O\n" +
          "|     " + "> "*shots + "  "*(game_over-shots) + "|\n"
          "|  __" + spacing + "/|\\\n"
          "| /  " + spacing + " |\n" +
          "| |  " + spacing + "/ \\")


def ask(restricted):
    answer = input("Which letter do you want to guess? ").upper()
    while answer not in alphabet[:-2] or answer in restricted:
        if answer not in alphabet[:-2]:
            print("Invalid input.")
            answer = input("Which letter do you want to guess? ").upper()
        else:
            print("Redundant guess, try again.")
            answer = input("Which letter do you want to guess? ").upper()
    return answer


class Puzzle:
    def __init__(self, answer=None, tried=None):
        self.answer = answer.upper() if answer else pick_word()
        self.tried = [] if tried is None else tried
        self.size, self.solved, self.leftover, self.present, self.frequencies = self.discern()
        self.score = [0, 0]  # First index is right answers, second index is wrong answers

        for guess in self.tried:  # Handling cases with already partially played games
            if guess in self.leftover:
                self.solved.append(guess)
                self.leftover.remove(guess)
                self.score[0] += 1
            else:
                self.score[1] += 1

    def discern(self):
        present, frequencies = self.find_freq()
        return len(present), [], present, present, frequencies
        # Returns amount of letters needed, letters guessed and not guessed yet

    def reconfigure(self):
        self.answer = pick_word()
        self.size, self.solved, self.leftover, self.present, self.frequencies = self.discern()
        self.tried = []
        self.score = [0, 0]

    def find_freq(self):
        presence = empty_dict.copy()
        frequencies = empty_dict.copy()
        for i in range(len(self.answer)):
            if self.answer[i] in [" ", "-"]:
                continue
            frequencies[self.answer[i]] += 1
            presence[self.answer[i]] = 1
        present = [alpha for alpha in alphabet[:-2] if presence[alpha]]
        return present, frequencies

    def display(self):
        output = "    "
        for content in range(len(self.answer)):
            if self.answer[content] in self.tried or self.answer[content] in [" ", "-"]:
                output += self.answer[content]
            else:
                output += "_"
        load_gun(self.score[1])
        print(output)

    def input_guess(self, letter):
        if letter not in self.present:
            print(letter, "is wrong!")
            self.score[1] += 1
        else:
            print(letter, "is correct!")
            self.score[0] += 1
            self.solved.append(letter)
            self.leftover.remove(letter)
        self.tried.append(letter)
        self.display()

    def evaluate(self):
        if self.score[0] == self.size:
            print("You win!")
            return 1
        elif self.score[1] == game_over:
            print("You lose!")
            print("The word was:", self.answer.capitalize())
            return -1
        return 0

    def start_play(self):
        self.display()
        while not self.evaluate():
            letter = ask(self.tried)
            self.input_guess(letter)
        print("Good game!")
        replay = input("Want to play again? Y/N - ").upper()
        while replay not in ["Y", "N"]:
            print("Invalid input.")
            replay = input("Want to play again? Y/N - ").upper()
        if replay == "N":
            return
        else:
            self.reconfigure()
            self.start_play()


new_puzzle = Puzzle()
new_puzzle.start_play()
