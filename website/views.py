from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, Snippet, Translation, Stat, Favourite
from . import db
import json
from sqlalchemy.sql import func


views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    Translation.query.filter_by(translation_id=snippet_id).first()
    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["noteId"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


def get_snippet(id):
    return Snippet.query.get(id)

@views.route("/song/id/<string:snippet_id>", methods=["GET"])
def song_id(snippet_id):
    snippet = get_snippet(snippet_id)
    translation = Translation.query.filter_by(snippet_id=snippet_id).first()
    return render_template("text.html", user=current_user, snippet=snippet, translation=translation)

@views.route("/song/name/<string:snippet_name>", methods=["GET", "POST"])
def song_name(snippet_name):
    if request.method == "POST":
        snippet_id = request.form.get("snippet_id")
        translation_id = request.form.get("translation_id")
        new_favourite = Favourite(user_id=current_user.id, snippet_id=snippet_id, translation_id=translation_id)

        db.session.add(new_favourite)
        db.session.commit()
        flash("Added to favourites!", category="success")

    snippet = Snippet.query.filter_by(name=snippet_name).first()
    translation=None
    if snippet:
        translation = Translation.query.filter_by(snippet_id=snippet.id).first()

    return render_template("text.html", user=current_user, snippet=snippet, translation=translation)



@views.route("/song/random", methods=["GET"])
def random_song():
    snippet = Snippet.query.order_by(func.random()).first()
    # translation = Translation.query.filter_by(snippet_id=snippet.id).first()
    return redirect(url_for('views.song_id', snippet_id=snippet.id))

@views.route("/song_list", methods=["GET"])
def songs():
    top_x = 30
    """song_list = (Snippet.query
                .filter_by(text_type="song")
                .all()[:top_x])"""
    song_list = (db.session.query(Snippet.name, Snippet.artist, Stat.score)
        .select_from(Snippet)
        .join(Translation)
        .join(Stat)
        .filter(Stat.score > 0)
        .order_by(Stat.score.asc())
        .limit(top_x).all())
    return render_template(
        "snippet_list.html",
        songs=song_list,
        user=current_user,
        snippet_type="song",
        snippets_length=db.session.query(Snippet).count()
        )



@views.route("/search", methods=["GET", "POST"])
def search():
    result=None
    if request.method == "POST":
        name = request.form.get("name")

        if len(name) < 1:
            flash("Note is too short", category="error")
        else:
            result = Snippet.query.filter_by(name=name).first()
            if result:
                flash("Result found", category="success")
            else:
                flash("No result :(", category="error")

    return render_template("search.html", user=current_user, result=result)


@views.route("/add-snippet", methods=["GET", "POST"])
def add_snippet():
    if request.method == "POST":
        text = request.form.get("text")
        name = request.form.get("name")

        new_snippet = Snippet(name=name, artist=text, language='zh-CN', url="www.hi.com")

        db.session.add(new_snippet)
        db.session.commit()
        flash("Snippet added", category="success")

    return render_template("add_snippet.html", user=current_user)
