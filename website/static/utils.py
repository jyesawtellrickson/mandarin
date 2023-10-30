from snownlp import SnowNLP
import pandas as pd
from os import path
import pickle as pkl
from collections import Counter


def grade_word(c, hsk):
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

def hanyu_to_structured(text):
    """Convert freeform text to our structure.

    Structure:
    characters > words > lines > paragraphs > texts

    words are labelled with levels and ids.

    word {
        character_ids: [0,]
        word_id: 0
        line_id: 0
        paragraph_id: 0
        text_id: 0
        level: 0
    }
    """
    hsk_map = pd.read_csv(path.join(path.dirname(__file__)[:-15], 'data/hsk/all.csv'))

    text = [text] # 'hello\n\nbro' -> ["hello", "bro"]
    lines = [p.split("\n") for p in text] # => [["hello", "there"], ["bro" "bro"]]
    # convert each line into list of words
    paragraphs_ = []
    j = 0
    for paragraph in lines:
        line_ = []
        for line in paragraph:
            if len(line) > 0:
                converted_words = SnowNLP(line).words
                words_ = [{
                    "words": converted_words[i],
                    "index": j+i,
                    "grade": grade_word(converted_words[i], hsk_map)
                    } for i in range(len(converted_words))]
                j = len(words_)
                line_ += [words_]
        paragraphs_ += [line_]
    return {"hanyu": paragraphs_}


def hanyu_to_pinyin(text, together=False):
    # format text first, lines & words
    lines = text.split("\n")
    words = [SnowNLP(l).words for l in lines if len(l) > 0]
    # convert
    lines2 = []
    for l in words:
        lines2.append([''.join(SnowNLP(w).pinyin) for w in l])
    # back to string
    s = [' '.join(l) for l in lines2]

    if together:
        return '\n'.join(['\n'.join(i) for i in zip(lines, s)])
    else:
        return '\n'.join(s)

def html_from_pairs(pairs):
    """
    Given pairs of words and colours, prepare html.

    Args:
        (tuple) (text, colour)
    """
    #<p style="color:red;">This is red.</p>
    return


def get_pinyin(structured):
    pinyin = []
    for paragraph in structured["hanyu"]:
        p = []
        for line in paragraph:
            l = []
            for word in line:
                l.append({
                    "words": "".join(SnowNLP(word["words"]).pinyin),
                    "grade": word["grade"],
                    "index": word["index"],
                    })
            p.append(l)
        pinyin.append(p)

    structured["pinyin"] = pinyin
    return structured

def structured_to_html(structured, language="hanyu"):
    with open("data/simplified_to_other.pkl", "rb") as f:
        simp_to_other = pkl.load(f)

    if language != "together":
        s = ''
        paragraphs = structured[language]
        for paragraph in paragraphs:
            for line in paragraph:
                for word in line:
                    s += '<span id="{}"" data-grade="{}" title="{}">{}</span>'.format(
                        word["index"],
                        word["grade"],
                        simp_to_other.get(word["words"]),
                        word["words"]
                        )
                    if language in ("pinyin", "english"):
                        s += " "
                s += "\n"
            s += "\n"

    if language == "together":
        ss = []
        for language in ("hanyu", "pinyin"):
            s= ""
            paragraphs = structured[language]
            for paragraph in paragraphs:
                for line in paragraph:
                    for word in line:
                        s += '<span id="{}"" data-grade="{}" title="{}">{}</span>'.format(word["index"], word["grade"], simp_to_other.get(word["words"]), word["words"])
                        if language in ("pinyin", "english"):
                            s += " "
                    s += "\n"
                s += "\n"
            ss += [s]
        # print(ss[0].split("\n"))
        # print(ss[1].split("\n"))
        s = "\n".join("\n".join(l) for l in zip(ss[0].split("\n"), ss[1].split("\n")))

    return s

def colour_content(text):
    """Grade content and colour
    Check HSK, and if content matches certain level, then colour.

    Content must be ready to be used like:
    <p style="color:red;">This is red.</p>


    Args:
        (str) text: a song (including spaces, newline breaks)

    Returns:
        (tuple) pairs of words,colours in text structure
    """
    colour_map = {
        0: 'white',
        1: 'violet',
        2: 'blue',
        3: 'green',
        4: 'yellow',
        5: 'orange',
        6: 'red',
    }


    return levels



def generate_vocab(text):
    """
    Given simplified chinese text, create a vocab
    """
    with open("data/simplified_to_other.pkl", "rb") as f:
        simp_to_other = pkl.load(f)

    # Sort content by most common occuring, then grade, then index
    texts = hanyu_to_structured(text)
    # Flatten to hanyu [ni, hao, ma]
    texts = [t3 for t1 in texts["hanyu"] for t2 in t1 for t3 in t2]
    # Fill nones with defaults
    for i in range(len(texts)):
        if texts[i]["grade"] is None:
            texts[i]["grade"] = 7

    texts = sorted(texts, key=lambda x: (x.get("grade"), x.get("index")))
    words = [w["words"] for w in texts]
    #
    #
    # Get list of words
    counted = Counter(words).most_common()
    # Use dictionary => [(hao, definition), ()]
    result = [(c[0], simp_to_other.get(c[0], ""), c[1]) for c in counted if simp_to_other.get(c[0]) is not None]
    return "\n".join(["{}: {} [{}]".format(r[0], r[1], r[2]) for r in result])

def url_to_embed(url):
    video_id = url.split("=")[1]
    return "https://www.youtube-nocookie.com/embed/" + video_id + "?autoplay=1"
