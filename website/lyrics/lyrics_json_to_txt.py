from ast import literal_eval
from app.snippet import Snippet
import pickle as pkl

def lyrics_json_to_txt():
    """
    Convert json file to individual text files.

    Input should be json file output from scrapy spider.
    Files will be output to individual txt files.
    """
    i = 1
    with open('lyrics/lyricstranslate_t.json') as f:
        lines = f.readlines()
    songs = []
    for l in lines:
        try:
            songs += [literal_eval(l.replace('null', 'None'))[0]]
        except:
            1
    for s in songs:
        if (s.get('lyrics') != '' and s.get('lyrics') is not None):
            with open('lyrics_files/song_' + str(i) + '.txt', 'w') as g:
                g.write(s.get('lyrics'))
            i += 1


def lyrics_json_to_pkl():
    """
    Convert json file to array of Songs pkl.

    Input should be json file output from scrapy spider.
    """
    i = 1
    with open('lyrics/lyricstranslate_t.json') as f:
        lines = f.readlines()
    songs = []
    for l in lines:
        try:
            songs += [literal_eval(l.replace('null', 'None'))[0]]
        except:
            1
    snippets = []
    for s in songs:
        if (s.get('lyrics') != '' and s.get('lyrics') is not None):
            meta = {'type': 'lyric',
                    'title':s.get('title'),
                    'author': s.get('artist'),
                    'url': s.get('url')}
            snippets += [Snippet(s.get('lyrics'), meta)]
    # Score texts.
    for s in snippets:
        try:
            s.score_text()
        except:
            True
    with open('../../data/lyrics_snippets.pkl', 'wb') as f:
        pkl.dump(snippets, f)
    return snippets


# lyrics_json_to_txt()
lyrics_json_to_pkl()
