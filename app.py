"""functions that display, operate on class Movie objects"""

from flask import Flask, render_template, redirect, url_for, session
from forms import QueryForm
from flask_bootstrap import Bootstrap
import imdb
import media
import json
import os


def between_years(min_year=0, max_year=9999, n=6):
    """returns top n movies from imdb top250 list
    produced between min_year and max_year"""

    imdb_access = imdb.IMDb()
    top250 = imdb_access.get_top250_movies()

    results = []
    for movie in top250:
        if movie['year'] >= min_year and movie['year'] <= max_year:
            results.append(media.Movie(imdb_id=movie.movieID))
        if (len(results) >= n):
            return results
    return results


def filter_movies(movies, *args):
    """returns a list of Movie objects that have
       attributes specified in args"""

    results = []
    for movie in movies:
        if set(args) <= set(movie.__dict__.keys()):
            results.append(movie)
    return results


app = Flask(__name__)
Bootstrap(app)
app.config['PREFERRED_URL_SCHEME'] = os.environ["PREFERRED_URL_SCHEME"]
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['DEBUG'] = os.environ["DEBUG"]


@app.route('/', methods=['GET', 'POST'])
def main_page():

    form = QueryForm()
    if form.validate_on_submit():
        movies = between_years(form.min_year.data,
                               form.max_year.data,
                               form.number.data)
        m = [json.dumps(movie.__dict__, ensure_ascii=False) for movie in movies]
        session['movies'] = m
        return redirect(url_for('movie_list'))
    return render_template('form.html', form=form)


big_lebowski = media.Movie(title="Big Lebowski", imdb_id="0118715",
                           trailer_youtube_url="https://www.youtube.com/watch?v=SUXWAEX2jlg")

@app.route('/list', methods=['GET'])
def movie_list():
    # movies = [json.loads(movie, encoding='utf-8') for movie in session['movies']]
    movies = [big_lebowski]
    return render_template('main.html', movies=movies)
