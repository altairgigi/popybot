from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import numpy

stemmer = SnowballStemmer("italian")

def tokenise(sentence):
    return word_tokenize(sentence)

def stem(word):
    pronouns = ["mi", "ti", "ci", "lo", "la"]

    for pronoun in pronouns:
        if word.endswith(pronoun):
            word = word[:-len(pronoun)];

    return stemmer.stem(word)

def bag_of_words(tokenised_sentece, all_words):
    word_list = [stem(word) for word in tokenised_sentece]

    bag = numpy.zeros(len(all_words), dtype=numpy.float32)

    for index, word in enumerate(all_words):
        if word in word_list:
            bag[index] = 1.0

    return bag
