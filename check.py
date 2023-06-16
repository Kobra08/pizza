
import nltk
from nltk.stem import WordNetLemmatizer
import os
import sqlite3 as sql
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from config import item_dict, count_dict, payment_method_dict, sizes_dict
class Bucket:
    def __init__(self, link) -> None:
        self.name = None
        self.zakaz = None
        self.address = None
        self.payment_method = None
        self.link = link

    def set_name(self, name):
        self.name = name

    def set_zakaz(self, zakaz):
        processor = ProcessMessage()
        self.zakaz = processor.process_purchase(zakaz)

    def set_address(self, address):
        self.address = address
    
    def set_payment_method(self, payment_method):
        processor = ProcessMessage()
        self.payment_method = processor.process_payment_method(payment_method)

    def get_name(self):
        return self.name

    def get_zakaz(self):
        return self.zakaz

    def get_address(self):
        return self.address

    def get_payment_method(self):
        return self.payment_method


class ProcessMessage:

    def __init__(self) -> None:
        try: 
            self.stopwords = stopwords.words("russian")
        except LookupError:
            nltk.download('stopwords')
            nltk.download('popular')
            nltk.download('punkt')
        finally:
            self.stopwords = stopwords.words("russian")
            self.stemmer = SnowballStemmer(language="russian")

    def tokenise(self, message):
        tokens = nltk.word_tokenize(message.lower())
        tokens = [token for token in tokens if token not in self.stopwords and token not in punctuation]
        stemmed_words = [self.stemmer.stem(word) for word in tokens]
        return stemmed_words
        

    def process_purchase(self, message):
        stemmed_words = self.tokenise(message)
        items = []
        counts = []
        sizes = []
        for i in stemmed_words:
            if i in item_dict.keys():
                items.append(item_dict.get(i))
            if i in count_dict.keys():
                counts.append(count_dict.get(i))
            if i in sizes_dict.keys():
                sizes.append(sizes_dict.get(i))

        purchase = dict(zip(items, list(zip(counts, sizes))))
        print(purchase)
        return purchase
    
    def process_payment_method(self, message):
        stemmed_words = self.tokenise(message)
        method = None
        for i in stemmed_words:
            if i in payment_method_dict.keys():
                method = payment_method_dict.get(i)
        return method



    def stopwords(self, tokens, stop_words):
        filtered_tokens = []                
        for token in tokens:
            if token not in stop_words:
                filtered_tokens.append(token)


# connection = sql.connect('user.sqlite', check_same_thread=False)
# q = connection.cursor()

# q.execute('''CREATE TABLE user
# (id int auto_increment primary key,
# IDIS varchar(100),
# Name varchar(100),
# Number varchar(100),
# Date varchar(100),
# Time varchar(100),
# People varchar(100),
# Koment varchar(100))''')
# connection.commit()