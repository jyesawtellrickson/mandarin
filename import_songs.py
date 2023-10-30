"""Imports songs into database

Usage:


Details:
    Documents are read from the folder,
    snippets are prepared and added to database,
    along with their translations,
    stats are calculated.


"""
import pickle as pkl
from website import db
from main import app
from website.models import Snippet, Translation, Stat
from ast import literal_eval
import website.snippet as old_snippet
from sqlalchemy.sql import exists

app.app_context().push()


"""if len(Snippet.query.all()) == 0:

    print("Importing songs")

    with open('data/lyrics/20230911_1547.json') as f:
        lines = f.readlines()
    songs = []

    for l in lines:
        try:
            songs += [literal_eval(l.replace('null', 'None'))[0]]
        except:
            1

    lyrics = []
    for s in songs:
        if (s.get('lyrics') != '' and s.get('lyrics') is not None):
            meta = {'type': 'lyric',
                    'title':s.get('title'),
                    'author': s.get('artist'),
                    'url': s.get('video_link'),
                    'text': s.get('lyrics').encode('utf-8', 'replace').decode(),
                    }
            lyrics += [meta]

    for l in lyrics:
        snippet = Snippet(artist=l.get("author"), name=l.get("title"), url=l.get("url"), language="zh-CN", text_type="song")
        db.session.add(snippet)
        db.session.commit()
        translation = Translation(text=l.get("text"), language="zh-CN", snippet_id=snippet.id)
        db.session.add(translation)
        db.session.commit()
"""

# iterate over translations and score
print("Calculating stats")
print(f"Current stats: {db.session.query(Stat).count()}")
print(f"Total trnslations: {db.session.query(Translation).count()}")

# Only create stats that haven't already been generated.
stmt = exists().where(Translation.id == Stat.translation_id)

for t in db.session.query(Translation).filter(~stmt).limit(1000).all():
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
