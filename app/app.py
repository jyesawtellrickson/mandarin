import pandas as pd
import random
import time
import datetime


class App:
    def __init__(self, name):
        try:
            self.history = pd.read_csv('database.csv')
        except FileNotFoundError:
            self.history = pd.DataFrame(columns=['user', 'test', 'result', 'tested_at', 'answered_at'])
        self.max_level = 1
        self.vocab = None
        self.get_vocab()
        return

    def get_vocab(self):
        self.vocab = pd.read_csv('../data/hsk/all.csv')
        self.vocab = self.vocab[self.vocab.hsk_level<=self.max_level]
        return

    def random_english(self, count):
        res = list()
        for i in range(count):
            res.append(self.vocab.english[(random.randint(0, len(self.vocab)))])
        return res

    def english_from_simplified(self, simp):
        return self.vocab[self.vocab.simplified==simp].english

    @staticmethod
    def randomise_list(l):
        random.shuffle(l)
        return l

    def update_database(self, obj):
        up = list()
        for col in self.history.columns:
            try:
                up.append(obj[col])
            except:
                up.append('')
        up_df =pd.DataFrame([up], columns=self.history.columns)
        self.history = self.history.append(up_df)
        self.history.to_csv('database.csv', index=False)
        return

    def practice(self):
        vs = self.vocab
        test = random.randint(0, len(vs))
        print(vs.iloc[test].simplified)
        s = datetime.datetime.now()
        opt = self.randomise_list(self.random_english(3) + [vs.iloc[test].english])
        corr = opt.index(vs.iloc[test].english)+1
        ans = input("Guess:\n" + '\n'.join(opt) + '\n\nAnswer: ')
        e = datetime.datetime.now()
        print(ans, vs.iloc[test].english)
        self.update_database({'user': 'jye',
                              'test': vs.iloc[test].pinyin_1,
                              'result': str(ans)==str(corr),
                              'tested_at': s,
                              'answered_at': e})
        return #test, str(ans)==corr


if __name__ == '__main__':
    my_app = App('jye')
    my_app.practice()
