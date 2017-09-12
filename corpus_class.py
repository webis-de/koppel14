import data_prep as dp
import numpy as np

class corpus:
    def __init__(self, start = '', end = '', authors = ''):
        self.start, self.end, self.authors = start, end, authors

    def build_by_xml(self, path, number_of_words=500, number_of_files = 500):
        self.start, self.end, self.authors = dp.open_xml(path, max_of_files = number_of_files, n_of_words = number_of_words)
        
    def build_pairs(self):
        self.pair = dp.pair_vec(len(self.start))
        self.end = np.take(self.end, self.pair)
        
    def build_matrix(self):
        data = dp.build_matrix(np.concatenate((self.start, self.end)))
        self.X = data[:len(self.start)]
        self.Y = data[len(self.end):]
        
    def get_length(self):
        return len(self.authors)
    
    def same_author(self, k):
        return self.pair[k] == k
    
    def get_pair(self, k,num = True, text = False):
        if text and num:
            return [self.X[k], self.Y[k], self.start[k], self.end[k]]
        if text:
            return [self.start[k], self.end[k]]
        else:
            return [self.X[k], self.Y[k]]
    
    