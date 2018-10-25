import io
import json
import os
from time import time

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.stem.snowball import SnowballStemmer
from string import punctuation

def process(file):
    terms = clean(file['data'])
    result = {}
    result['terms'] = terms
    result['time'] = time()
    with io.open(os.path.pardir + '/json/out.text.json', 'w', encoding='utf8') as outfile:
        text = json.dumps(result,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)
    return result

def clean(file):
    stop = set(stopwords.words('english'))
    exclude = set(punctuation)
    lemma = WordNetLemmatizer()
    # stemmer = PorterStemmer()
    #stemmer = SnowballStemmer("english", ignore_stopwords=True)

    # remove stop words & punctuation, stemming and lemmatize words
    s_free = " ".join([i for i in file.lower().split() if i not in stop])
    p_free = ''.join(ch for ch in s_free if ch not in exclude)
    #lemm = " ".join(lemma.lemmatize(word) for word in p_free.split())
    #stem = " ".join(stemmer.stem(word) for word in lemm.split())
    lemm = " ".join(lemma.lemmatize(word) for word in p_free.split())
    words = lemm.split()

    # only take words which are greater than 2 characters
    cleaned = [word for word in words if len(word) > 2]
    return cleaned


if __name__ == '__main__':
    try:
        with io.open(os.path.pardir + '/json/in.text.json') as data_file:
            data = json.load(data_file)
            if time() <= data['time'] + 20:
                process(data)
    except:
        pass