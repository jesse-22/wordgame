import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
WILDCARD = '*'
HAND_SIZE = int(input("How many hands do you want to play"))

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    first_component = 0
    second_component = 0
    first_total = 0
    second_total = 0
    final_word_score = 0
    word_length = len(word)

    for letter in word:
        first_component = first_component + SCRABBLE_LETTER_VALUES[letter.lower()]

    # Get the second component
    second_component = (7 * word_length) - (3 * (n - word_length))

    # Test to see if second_component * first_component > second_component * 1
    # Return the greater total as final score for that word
    first_total = first_component * second_component
    second_total = first_component * 1

    if first_total > second_total:
        final_word_score = first_total
    else:
        final_word_score = second_total

    return final_word_score


def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()


def deal_hand(n):
    hand = {}
    num_vowels = int(math.ceil(n / 3))
    x_wc = WILDCARD
    hand[x_wc] = hand.get(x_wc, 0) + 1
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    word_lowercase = word.lower()
    for ch in word_lowercase:
        hand[ch] = hand.get(ch, 0) - 1
        if hand.get(ch, 0) == 0:
            del hand[ch]
    return hand


def is_valid_word(word, hand, word_list):
    word_lower = word.lower()
    word_lower_list = word_lower
    wordList = set(word_list)  # to generate copy of list wordList
    new_word = ""
    possible_words = set(new_word)
    if WILDCARD in word_lower:
        for letter in word_lower_list:
            for v in VOWELS:
                new_word = word.replace(WILDCARD, v)
                if new_word.lower() in wordList:
                    possible_words.add(new_word)
        if len(possible_words) != 0:
            return True
    else:
        cards_left = hand.copy()
        valid = True  # assume a valid word for now
        if word_lower in wordList:  # is the word in the valid LIST of words?
            for ch in word_lower:
                if not ch in cards_left or cards_left[ch] == 0:
                    valid = False
                    break
                else:
                    cards_left[ch] -= 1
        else:
            valid = False
        return valid


def calculate_handlen(hand):
    hand_length = len(hand)
    return hand_length


def play_hand(hand, word_list):
    total_points_for_hand = 0
    total_points_current_hand = 0
    final_score = 0
    user_play = input("Please enter a word or !! to indicate you are done: ")

    while calculate_handlen(hand) != 0:
        check = is_valid_word(user_play, hand, word_list)
        updated_hand = update_hand(hand, user_play)
        hand_length = calculate_handlen(updated_hand)
        if check:
            print("Current hand: ", end=' ')
            display_hand(updated_hand)
            spoints = get_word_score(user_play, hand_length)
            total_points_current_hand += spoints
            print(user_play, "scored", spoints, "points.", "total points:", total_points_current_hand)
            user_play = input("Enter a word or '!!' to indicate you are finished")
            if user_play == '!!':
                print("Total Score for hand:", total_points_current_hand)
                final_score += total_points_current_hand
                return final_score
        else:
            print("That isn't a valid word, please try again")
    return final_score


def substitute_hand(hand, letter):
    hand_copy = dict(hand)
    if letter in hand_copy.keys():
        x = random.choice(ALL_LETTERS)
        while x in hand_copy:
            x = random.choice(ALL_LETTERS)
        if x not in hand_copy:
            del hand_copy[letter]
            hand_copy[x] = hand_copy.get(x, 0) + 1
    return hand_copy


def play_game(word_list):
    final_score1 = 0
    final_score2 = 0
    final_score3 = 0
    final_score = 0
    HAND_TOTAL = 0
    n = 7
    user_input = HAND_SIZE
    current_hand = deal_hand(n)
    copy_hand = dict(current_hand)
    print("Current hand: ", end='')
    display_hand(current_hand)
    substitute_letter = input("Would you like to substitute a letter?")
    if substitute_letter == 'yes':
        letter = input("What letter would you like to substitute")
        current_hand = substitute_hand(current_hand, letter)
        print("Current Hand: ", end='')
        display_hand(current_hand)
    while HAND_TOTAL < HAND_SIZE:
        score1 = play_hand(current_hand, word_list)
        final_score1 += score1
        HAND_TOTAL += 1
        replay_hand = input("Would you like to replay the hand?")
        if replay_hand == 'yes':
            print("Current hand: ", end='')
            display_hand(copy_hand)
            score2 = play_hand(copy_hand, word_list)
            replay_hand = input("Would you like to replay the hand?")
            final_score2 += score2
            HAND_TOTAL += 1
        if HAND_TOTAL < HAND_SIZE and replay_hand == 'no':
            hand = deal_hand(7)
            print("Current hand: ", end='')
            display_hand(hand)
            score3 = play_hand(hand, word_list)
            final_score3 += score3
            HAND_TOTAL += 1
        final_score = final_score1 + final_score2 + final_score3
        if HAND_TOTAL == HAND_SIZE:
            print("Total score over all hands: ", final_score)

if __name__ == '__main__':
    word_list_test = load_words()
    play_game(word_list_test)
    # hand_test = deal_hand(7)
    # hand_test = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u': 1}
    # letter_test = 'u'
    # substitute_hand(hand_test, letter_test)
    # play_hand(hand_test, word_list_test)
    # play_game(word_list)
    # word_test = "Rapture"
    # n_test = 7
    # get_word_score(word_test, n_test)

    # is_valid_word(word_test, hand_test, word_list_test)
    # hand_test = deal_hand(7)
    # display_hand(hand_test)
    # is_valid_word(word_test, hand_test, word_list_test)
    # calculate_handlen(hand_test)
