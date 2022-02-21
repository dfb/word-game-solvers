import sys
# https://raw.githubusercontent.com/jeremy-rifkin/Wordlist/master/master.txt
# https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
# https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt <-- too few!
# https://raw.githubusercontent.com/dolph/dictionary/master/ospd.txt
# https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt
#words = [x.strip() for x in open('listado-general.txt', 'rb').read().decode('utf8').split('\n')]
#words = [x.strip() for x in open('ospd.txt', 'rb').read().decode('utf8').split('\n')]
words = [x.strip() for x in open('nytimes_wordle.txt').read().split('\n')]
words = [x.upper() for x in words if x]

WORD_LEN = 5
possibles = [x for x in words if len(x) == WORD_LEN]

guessedLetters = set()
unguessedLetters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
while 1:
    print(len(possibles), 'possible words remain')
    userInput = input('Your next guess AND game\'s response: ').strip().upper()
    parts = userInput.split()
    assert len(parts) == 2
    guess, response = parts
    assert len(guess) == WORD_LEN
    assert len(response) == WORD_LEN

    guessedLetters |= set(guess)
    unguessedLetters = unguessedLetters.difference(set(guess))

    # Whittle down the list of possible words
    for i, (letter, color) in enumerate(zip(guess, response)):
        assert color in 'BYG', color
        if color == 'B':
            # NOTE: despite what the website instructions say, black does not /always/ mean the
            # word does not contain the letter at all. In cases where the guess uses the letter
            # multiple times but the final word uses it fewer times, excess occurences in the
            # guess will be shown as black. For example, if the final word has one 'e' but the
            # guess has 2 'e's, then the first 'e' of the guess will be yellow or green while
            # the 2nd 'e' will be black
            gcount = guess.count(letter)
            possibles = [x for x in possibles if x.count(letter) < gcount]
        elif color == 'G':
            # if color is green, keep only words that have that letter in that position
            possibles = [x for x in possibles if x[i] == letter]
        else:
            # if color is yellow, keep words that do NOT have that letter in that position...
            possibles = [x for x in possibles if x[i] != letter]

            # ...and then keep only words that do have that letter somewhere
            possibles = [x for x in possibles if letter in x]

    # Find most frequently used unguessed letters
    letterCounts = {} # unguessed letter -> frequency
    for word in possibles:
        for letter in word:
            if letter in unguessedLetters:
                letterCounts[letter] = letterCounts.get(letter, 0) + 1
    mostFreq = []
    for count, letter in sorted([(v,k) for (k,v) in letterCounts.items()], reverse=True):
        mostFreq.append((count, letter))
    print('Most freq unguessed:', mostFreq[:5])

    # Score words based on how well they use unguessed letters
    scored = [] # (score, word)
    for word in possibles:
        score = 0
        used = '' # don't give them credit for using an unguessed letter more than once
        for letter in word:
            if letter in used:
                continue
            used += letter
            score += letterCounts.get(letter, 0) # no points for an already-guessed letter
        scored.append((score, word))
    for score, word in sorted(scored, reverse=True)[:15]:
        print(score, word)

    #for word in sorted(possibles):
    #    print('possible:', word)

