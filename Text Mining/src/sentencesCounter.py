"""
Author: Francisco Medel Molinero
SentenceCounter description: The function of this script is to return the number of sentences of a file
Input of the function: text document that we want to process
Output: Number of sentences of the file
"""
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize

text = None
with open('doc.txt', 'r') as f:
    text = f.read()

sentences = sent_tokenize(text)

print(len(sentences))