import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.num_pos_reviews = 0
        self.num_neg_reviews = 0
        self.pos_words = {}
        self.neg_words = {}
        self.num_pos_words = 0
        self.num_neg_words = 0
        self.sum_pos_words = 0
        self.sum_neg_words = 0
        self.num_reviews = 0


    def train(self, lines): #calculate number of positive and negative reviews , the number of times each word appeared in a positive or negative review
        lines = self.process_data(lines)
        
        for row in lines:
            if row[0] == '1':
                self.num_neg_reviews += 1
                for word in row[2:] :
                    if word in self.neg_words.keys():
                        self.neg_words[word] += 1
                    else:
                        self.neg_words[word] = 1
            else:
                self.num_pos_reviews += 1
                for word in row[2:]:
                    if word in self.pos_words.keys():
                        self.pos_words[word] += 1
                    else:
                        self.pos_words[word] = 1
        self.num_reviews = len(lines)
        self.num_pos_words = len(self.pos_words)
        self.num_neg_words = len(self.neg_words)
        self.sum_pos_words = sum(self.pos_words.values())
        self.sum_neg_words = sum(self.neg_words.values())



    def classify(self, lines):
        predictions = []
        data = self.process_data(lines)
        for line in data:
            p_pos = math.log(self.num_pos_reviews / self.num_reviews)
            p_neg = math.log(self.num_neg_reviews / self.num_reviews)
            for word in line[2:]:
                if word in self.pos_words.keys():
                     p_pos = p_pos + math.log((self.pos_words[word] + 1 )/ (self.num_pos_words + self.sum_pos_words))
                else:
                        p_pos = p_pos + math.log(1 / (self.num_pos_words + self.sum_pos_words + self.sum_neg_words))
                if word in self.neg_words.keys():
                    p_neg = p_neg + math.log((self.neg_words[word] + 1 )/ (self.sum_neg_words + self.num_neg_words ))
                else:
                    p_neg = p_neg + math.log(1 / (self.num_neg_words + self.sum_neg_words + self.sum_pos_words))
            if p_pos >= p_neg:
                predictions.append('5')
            else:
                predictions.append('1')
        return predictions

                

    
       

        



    def process_data (self , lines):
        # need to remove capitalization ;remove punctuation ,remove stop words
        data = []
        for line in lines:
            data.append(line.split('|'))
        for row in data :
            text = row[2]
            text = text.lower()
            text = re.sub(r'[^\w\s]','',text)
            row[2 ] = text
            row[2:] = row[2].split(' ')
        
        return data
        
    