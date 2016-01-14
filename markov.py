import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string, n):
    """Takes input text as string; returns _dictionary_ of markov chains with n-gram keys."""

    chains = {}

    words = text_string.split()

    for index in range(len(words) - n):
        word_gram = []

        for i in range(n):
            word_gram.append(words[index + i])
        word_gram = tuple(word_gram)

        if word_gram not in chains:
            chains[word_gram] = [words[index + n]]

        else:
            chains[word_gram].append(words[index + n])

    # BI-GRAM VERSION

    # chains = {}

    # words = text_string.split()

    # for i in range(len(words) - 2):
    #     key = (words[i], words[i + 1])
    #     value = words[i + 2]

    #     if key not in chains:
    #         chains[key] = []

    #     chains[key].append(value)

    #     # or we could replace the last three lines with:
    #     #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains, n):
    """Takes dictionary of markov chains with n-gram keys; returns random text."""


    # BI-GRAM VERSION

    # key = choice(chains.keys())
    # words = [key[0], key[1]]
    # old_text_string = ""

    # while key in chains:
    #     # Keep looping until we have a key that isn't in the chains
    #     # (which would mean it was the end of our original text)
    #     #
    #     # Note that for long texts (like a full book), this might mean
    #     # it would run for a very long time.

    #     word = choice(chains[key])
    #     words.append(word)
    #     key = (key[1], word)

    #     text_string = " ".join(words)

    while True:
        # We're choosing a random tuple key from our dictionary, chains.
        # If the first word in the random tuple key is capitalized, go forward.
        link = choice(chains.keys())
        if link[0].istitle():
            break

    # Converting our tuple key to a list so we can join the words in our resulting text.
    link_list = list(link)

    # While our tuple key is found in our chains dictionary,
    # Choose a random word from the list of values found at that key.
    # Add that random word to our list of words.
    # We convert the tuple key slice from index 1 to the end into a list,
    # And add the random word to create a new key link, which is converted back to a tuple.
    # Finally, we combine all words in our list to make a long string (Markov text!)
    old_text_string = ""
    while link in chains:
        random_word = choice(chains[link])
        link_list.append(random_word)

        link_temp = list(link[1:])
        link_temp.append(random_word)
        link = tuple(link_temp)
        
        text_string = " ".join(link_list)

        # Check to see if our text_string exceeds 140 characters.
        # If it exceeds 140, revert to last iteration of the while loop
        # (saved as old_text_string).
        if len(text_string) > 140:
            text_string = old_text_string
            break
        else:
            # Saves our current string as our old_text_string 
            # which is within 140 characters, before trying to add
            # another word.
            old_text_string = text_string

    return text_string


def tweet(chains):
    """Tweets a Markov text to our twitter handle: @AnnieChachiBot"""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()

    # Send a tweet with our Markov text
    status = api.PostUpdate(make_text(chains, int(sys.argv[1])))
    print status.text

    tweet_again()

    
def tweet_again():    
    """Asks if user wants to tweet again."""

    tweet_again_answer = raw_input("Press any key to tweet again [q to quit] > ")
    if tweet_again_answer == 'q':
        return
    else:    
        tweet(chains)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[2:]


# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text, int(sys.argv[1]))

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)
