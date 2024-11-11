import re
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup
from Tokernizer import *

#REGEX to find anything date/calendar related. 
pattern = re.compile(r'\b(calendar|date)\b', re.IGNORECASE)

stop_words = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

'''
    Return False if there is a calendat attribute anywhere. 
'''
def check_calendar(text):
    if(pattern.findall(text)):
        return True 
    return False

def dead_site(text):
    #Pattern to remove newline characters.
    text = re.sub(r'\n', ' ', text)
    #Check for no content: 
    if not text:
        return True
    if(len(text) < 750):
        return True 
    #Remove stop words: 

    return False
    #Check for low content:

def write_site(text, url):
    #Pattern to get rid of stop words:
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in stop_words) + r')\b'

    # Remove the stop words from the text
    text = re.sub(pattern, '', text)

    # Print the cleaned text
    with open("search_text.txt", 'w', encoding='utf-8') as file:
        file.write(text)
    analyze_file(url)