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


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    old_text_string = ""

    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

        text_string = " ".join(words)
        
        # Check to see if our text_string exceeds 140 characters.
        # If it exceeds 140, revert to last iteration of the while loop
        # (saved as old_text_string).
        if len(text_string) > 140:
            text_string = old_text_string
            break

        # Saves our current string as our old_text_string 
        # which is within 140 characters, before trying to add
        # another word.
        old_text_string = text_string

    return text_string


def tweet(chains):
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
    status = api.PostUpdate(make_text(chains))
    print status.text

    
def tweet_again():    

    while True:
        tweet_again_answer = raw_input("Press any key to tweet again [q to quit] > ")
        if tweet_again_answer == 'q':
            break
        else:
            tweet(chains)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)
