"""Imports songs into database

Usage:


Details:
    Stories are read from the stories_folder,
    snippets are prepared and added to database,
    stats are calculated.


"""
import pickle as pkl
from website import db
from main import app
from website.models import Snippet, Translation, Stat
from ast import literal_eval
import website.snippet as old_snippet
from os import listdir
from os.path import isfile, join


# app.app_context().push()
print("Importing stories")
stories_folder = 'data/stories/'

onlyfiles = [f for f in listdir(stories_folder) if isfile(join(stories_folder, f))]

story_dicts = []
for file in onlyfiles:
    with open(stories_folder + file) as f:
        lines = f.readlines()

    meta = {'type': 'story',
            'title': file,
            'author': 'chatgpt',
            'text': "".join(lines),
            }

    story_dicts += [meta]

print(story_dicts)

for s in story_dicts:
    snippet = Snippet(artist=l.get("author"), name=l.get("title"), language="zh-CN", text_type="story")
    db.session.add(snippet)
    db.session.commit()
    translation = Translation(text=l.get("text"), language="zh-CN", snippet_id=snippet.id)
    db.session.add(translation)
    db.session.commit()

# iterate over translations and score and add stats
print("Calculating stats")
print(len(Translation.query.all()))
for t in Translation.query.limit(200).all():
    translation_text = t.text
    translation_id = t.id
    s = old_snippet.Snippet(translation_text, {})
    _ = s.score_text()
    stat = {
        'total_characters': s.stats.get('total_characters'),
        'unique_characters': s.stats.get('unique_characters'),
        'score': s.stats.get('score', 10),
        }
    stat = Stat(
        translation_id=translation_id,
        score=stat.get("score"),
        total_characters=stat.get("total_characters"),
        unique_characters=stat.get("unique_characters"),
        )
    db.session.add(stat)
db.session.commit()
"""
