import sys
import threading
import time

if len(sys.argv) != 3:
    print("You must write two arguments for this program")
    sys._exit()

correct_words, letter_scores, total_score, remain_time, start_time = {}, {}, 0, 30, time.time()

shuffled_words_file = open(sys.argv[1], "r", encoding='utf-8-sig')
for line in shuffled_words_file:
    split_line, words_list= line.split(":"), []
    for word in split_line[1].split(","):
        words_list.append(word.rstrip().replace("İ", "i").lower())
    correct_words.update({split_line[0].replace("İ", "i").lower(): words_list})


letter_file = open(sys.argv[2], "r", encoding='utf-8-sig')
for line in letter_file:
    letter_scores.update({line.split(":")[0].replace("İ", "i").lower(): int(line.split(":")[1])})

shuffled_words_file.close(), letter_file.close()


def print_guessed(guessed_list):
    for word in guessed_list:
        if guessed_list[-1] != word:
            print(word.lower(), end="-")
        else:
            print(word.lower())


def time_thread_func():
    global remain_time
    for _ in range(30):
        time.sleep(1)
        remain_time -= 1
    print(f"\nScore for {shuffled_word.lower()} is {shuffled_word_score} and guessed words are:", end=" ")
    print_guessed(guess_list)
    print("Game is over. Your total score is:", total_score, "\nPress enter to end the program...")


def control_input(shuffled_word, input):
    if input.lower() not in correct_words[shuffled_word]:
        print("Your guess word is not a valid word")
    elif input.lower() in guess_list:
        print("This word is guessed before")
    else:
        guess_list.append(input.lower())
        score(input.lower())


def score(word):
    global shuffled_word_score, total_score
    word_score = 0
    for letter in word:
        word_score += letter_scores[letter.lower()]
    shuffled_word_score += word_score*len(word)
    total_score += word_score*len(word)


time_thread = threading.Thread(target=time_thread_func)
time_thread.start()

for shuffled_word in correct_words.keys():
    guess_list, shuffled_word_score = [], 0
    print("Shuffled letters are: ", shuffled_word.lower(),
          " Please guess words for these letters with minimum three letters")
    while remain_time != 0 and guess_list != correct_words[shuffled_word]:
        guessed_word = input("Guessed Word: ").replace("İ", "i")
        if remain_time != 0:
            control_input(shuffled_word, guessed_word)
            print("You have", remain_time, "time")
    if remain_time == 0:
        break
    print("You guessed all words...")
    print(f"Score for {shuffled_word.lower()} is {shuffled_word_score} and guessed words are:", end=" ")
    print_guessed(guess_list)

