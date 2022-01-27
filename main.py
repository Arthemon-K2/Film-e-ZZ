import password as password
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
from flask_paginate import Pagination, get_page_args
from data import queries
from datetime import datetime
import utils

load_dotenv()
app = Flask('Film-e-ZZ')
app.secret_key = b'Film-e-ZZs3cr3tk3y'



@app.route('/')
def index():
    print(session['username'])
    shows = queries.get_shows()
    return render_template('index.html', shows=shows, username=session['username'])


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
        return render_template('search-show.html', hits=hits)
    return render_template('search-show.html')


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        user_name = request.form.get('inputUsername')
        user_email = request.form.get('inputEmail')
        user_firstname = request.form.get('inputFirstname')
        user_lastname = request.form.get('inputLastname')
        user_pssw_hashed = utils.hash_password(request.form.get('inputPassword'))
        user_role = request.form.get('userRole')
        user_reg_date = datetime.now()
        queries.add_user_from_register(user_name, user_email, user_firstname, user_lastname, user_pssw_hashed, user_reg_date, user_role)
        return redirect('/')



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user_name = request.form.get('inputUsername')
        user_password = request.form.get('inputPassword')

        loggedInUser = queries.get_user_from_login(user_name)

        if loggedInUser is not None and utils.verify_password(user_password, loggedInUser[0]['hash_pass']):
            session['username'] = request.form.get('inputUsername')
            return redirect('/')
        else:
            return render_template('login.html')


@app.route('/logout')
def user_logout():
    return render_template('/')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
