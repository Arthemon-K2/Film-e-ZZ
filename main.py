from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
from data import queries
import datetime

load_dotenv()
app = Flask('Film-e-ZZ')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated')
def most_rated_shows():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(queries.get_most_rated_shows())
    pagination_most_rated_shows = get_shows(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('most-rated.html',
                           shows=pagination_most_rated_shows,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


def get_shows(offset=0, per_page=15):
    most_rated_shows = queries.get_most_rated_shows()[offset: offset + per_page]
    return most_rated_shows


@app.route('/show/<int:id>')
def show_details(id):
    show_details = queries.get_show_details(id)
    season_details = queries.get_season_details_show_id(id)
    actors = queries.get_show_actors(id)
    return render_template('show-details.html', show=show_details, seasons=season_details, actors=actors)


@app.route('/actor/<int:id>')
def show_actor_informations(id):
    details = queries.get_actor_details(id)
    actor_works = queries.get_actor_works(id)
    return render_template('actor-details.html', actor=details, actor_works=actor_works)


@app.route('/actors')
def get_all_actors():
    actors_list = queries.get_all_actors()
    return render_template('actors.html', actors_list=actors_list)


@app.route('/actors/most-active-actors')
def most_active_actors():
    most_a_actors = queries.get_most_active_actors()
    return render_template('most-active-actors.html', a_actors=most_a_actors)


@app.route('/search', methods=['GET', 'POST'])
def search_show_by_title():
    if request.method == 'POST':
        user_search = str(request.form['title_search'])
        hits = queries.search_show_by_title(user_search)
        print(user_search, hits)
        return render_template('search-show.html', hits=hits)
    return render_template('search-show.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
