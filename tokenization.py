from collections import defaultdict
from bs4 import BeautifulSoup
import re


def tokenize_url_content(url_content):
    """
    Tokenize the text into words using re
    """
    soup = BeautifulSoup(url_content, 'html.parser')
    text = soup.get_text()
    tokens = text.split()                               # separating each token by space
    return tokens

def compute_word_frequencies(tokens):
    """
    Compute word frequencies from tokens
    """
    word_frequencies = defaultdict(int)
    for token in tokens:
        word_frequencies[token] += 1
    return word_frequencies