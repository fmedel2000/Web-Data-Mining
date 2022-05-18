"""
Author: Francisco Medel Molinero
Text processor description: The function of this script is to perform an entity classification of a text document using POS and NER tagging methods and for each detected entity extract the first sentence of the wikipedia summary of that entity and simplify that sentence by creating a noun phrase.
Input of the function: text document that we want to process
Output of the function: 3 json files: entities of POS tagging, entities of NER tagging and finally, one document with noun entity + noun phrase simplified
"""

# Imports
from nltk.corpus import stopwords
from nltk.sentiment.util import *
import nltk
import wikipedia
import json

import warnings

warnings.catch_warnings()

warnings.simplefilter("ignore")

stops = stopwords.words('english')

text = None

# Opening the text document that we want to process
with open('doc.txt', 'r') as f:
    text = f.read()


# Named Entity Recognition
def extractEntities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


# Function to get the noun phrase extracted of the wikipedia summary for each entity detected
def customEntityProcessor(dictionary, output):
    data = {}
    for key in dictionary:
        try:
            # Summary of the entity in wikipedia
            summary = wikipedia.page(key).summary

            # get the first sentence of the summary
            firstSentence = ' '.join(re.split(r'(?<=[.:;])\s', summary)[:1])

            # function to test if something is a noun
            is_noun = lambda pos: pos[:2] == 'NN'

            # function to test if something is an adjective
            is_adjective = lambda pos: pos[:2] == 'JJ'
            tokenized = nltk.word_tokenize(firstSentence)

            # We filter the words that are nouns and adjectives from the first sentence of the entity
            elements = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos) or is_adjective(pos)]

            # From list to string
            string = ' '.join([str(item) for item in elements])

            # Saving key/value
            data[key] = string
        except wikipedia.exceptions.DisambiguationError as e:
            # Saving key/value
            data[key] = e.options[0]
    # Saving the dictionary into a json file
    json.dump(data, output)
    return data


# Opening the files to write the information on them
pos = open('POS_entities.json', 'w')
ner = open('NER_entities.json', 'w')
output = open('output.json', 'w')

# Tokenization of the text document's elements
tokens = nltk.word_tokenize(text)

# POS tagging method
tagged = nltk.pos_tag(tokens)
json.dump(tagged, pos)

# NER entities(entities chunked JJ, NN, VBZ, ...)
ne_chunked = nltk.ne_chunk(tagged, binary=True)
json.dump(ne_chunked, ner)

# Named Entity recognition
dictionary = extractEntities(ne_chunked)

# We call this function to get the noun phrase extracted of the wikipedia summary for each entity detected
customEntityProcessor(dictionary, output)
