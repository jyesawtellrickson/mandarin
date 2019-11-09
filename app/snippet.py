"""rank_text.py
For a given document, process and prepare scoring.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from snownlp import SnowNLP
from string import punctuation, whitespace
from os import path


class Snippet:
    def __init__(self, text, meta):
        # meta includes author, title, url, type
        self.meta = meta if meta else {}
        self.text = text
        self.lyrics_processed = ''
        self.clean_text()
        self.graded = None
        self.stats = {}

    @staticmethod
    def grade_word(self, c, hsk):
        """Grade a character with HSK system.

        Args:
            c (str): Single Chinese character
            hsk (DataFrame): 

        Returns:
            int: Level of Chinese character or None.
        """
        # Try to match the character, no matter the length.
        c_level = hsk[(hsk.simplified == c) | (hsk.traditional == c)] \
            .hsk_level \
            .sort_values() \
            .tolist()
        if len(c_level) > 0:
            return c_level[0]
        else:
            return None

    def rank_text(self):
        """Rank text using HSK method.
        """
        if len(self.lyrics_processed) == 0:
            return None
        # Create hsk dataframe for use in grading.
        hsk = pd.read_csv(path.join(path.dirname(__file__)[:-4], 'data/hsk/all.csv'))
        # Remove space and newline characters.
        if (self.lyrics_processed):
            text = ''.join([t for t in self.lyrics_processed if t != ' ' and t != '\n'])
        else:
            text = ''.join([t for t in self.text if t != ' ' and t != '\n'])
        # Convert text to characters.
        characters = SnowNLP(text).words
        # Create dict for each HSK level.
        levels = {}
        for i in hsk.hsk_level.unique():
            levels[i] = []
        levels[0] = []
        for c in characters:
            # Try to match the character, no matter the length.
            grade = self.grade_word(self, c, hsk)
            if grade is not None:
                levels[grade] += [c]
            else:
                if len(c) > 1:
                    # If we couldn't match the double character,
                    # try matching the individual characters.
                    grades = [self.grade_word(self, cp, hsk) for cp in c]
                    # If no matches, push double character.
                    if all(v is None for v in grades):
                        levels[0] += [c]
                    # If some matches, push individual characters.
                    else:
                        for i, g in enumerate(grades):
                            levels[int(g or 0)] += [c[i]]
                # But if it's only 1 long, just push.
                else:
                    levels[0] += [c]
        for i in levels.keys():
            levels[i] = list(set(levels[i]))
        self.graded = levels
        return levels

    def character_length(self):
        if self.graded is not None:
            return sum([len(v) for k, v in self.graded.items()])
        else:
            return 0

    def score_text(self, level=None):
        if self.graded is None:
            self.rank_text()
        if self.character_length() == 0:
            return None
        levels = self.graded
        self.stats['total_characters'] = len(self.lyrics_processed)
        self.stats['unique_characters'] = sum([len(v) for k, v in levels.items()])
        if level is None:
            tmp = {}
            for i in range(1, 7):
                tmp[i] = round(
                    sum([len(levels[i]) for i in range(1, i + 1)]) \
                    / self.stats['unique_characters'], 2)
            self.stats['readability'] = tmp
        else:
            self.stats['readability'] = {
                level: round(sum([len(levels[i]) for i in range(1, level+1)]) \
                    / self.stats['unique_characters'], 2)}
        self.stats['score'] = round(sum([k * len(v) for k, v in levels.items()]) \
             / sum([len(v) for k, v in levels.items() if k != 0]), 2)
        # print('Total Characters: {}'.format(self.stats['total_characters']))
        # print('Unique Characters: {}'.format(self.stats['unique_characters']))
        # print(levels)
        # print('Readability: {:.2f}'.format(self.stats['readability']))
        # print('Score: {:.2f}'.format(self.stats['score']))
        print(self.meta.get('title'))
        return self.stats

    def plot_hsk_levels(self):
        tmp = [[k, len(v)] for k, v in self.graded.items()]
        tmp = sorted(tmp, key = lambda x: x[0])
        x = [t[0] for t in tmp]
        y = [t[1] for t in tmp]
        plt.bar(x, y)
        plt.show()


    def print_example_characters(self, l=10):
        for i in self.graded.keys():
            print('{}: {}'.format(i, ', '.join(self.graded[i][:l])))

    def clean_text(self):
        """
        Convert the text to cleaned version.
        :return:
        """
        lyrics_tmp = self.text
        lyrics_tmp = lyrics_tmp.lower()
        # Remove English characters.
        lyrics_tmp = re.sub(r'[a-z]+', '', lyrics_tmp)
        # Remove branding phrases.
        # Remove punctuation.
        lyrics_tmp = re.sub(r'[' + punctuation + ']+', '', lyrics_tmp)
        # Remove double lines.
        lyrics_tmp = re.sub(r'\\n\\n', '\\n', lyrics_tmp)
        if self.meta.get('title') != None:
            self.meta['title'] =  \
                self.meta.get('title').strip(whitespace)
        # Convert to Simplified Chinese.
        lyrics_tmp = SnowNLP(lyrics_tmp).hans

        self.lyrics_processed = lyrics_tmp
