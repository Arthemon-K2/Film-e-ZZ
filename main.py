from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_paginate import Pagination, get_page_args
import utils
from data import queries

load_dotenv()
app = Flask('Film-e-ZZ')
app.secret_key = b'Film-e-ZZs3cr3tk3y'


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html', username='Visitor')


@app.route('/shows')
def get_all_shows():
    if 'username' in session:
        shows = queries.get_shows()
        return render_template('shows.html', shows=shows, username=session['username'])
    else:
        shows = queries.get_shows()
        return render_template('shows.html', shows=shows, username='Visitor')

@app.route('/shows/most-rated')
def most_rated_shows():
    if 'username' in session:
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        total = len(queries.get_most_rated_shows())
        pagination_most_rated_shows = get_shows(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
        return render_template('most-rated.html',
                               shows=pagination_most_rated_shows,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               username=session['username'])
    else:
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        total = len(queries.get_most_rated_shows())
        pagination_most_rated_shows = get_shows(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
        return render_template('most-rated.html',
                               shows=pagination_most_rated_shows,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               username='Visitor')


def get_shows(offset=0, per_page=15):
    most_rated_shows = queries.get_most_rated_shows()[offset: offset + per_page]
    return most_rated_shows


@app.route('/show/<int:id>')
def show_details(id):
    if 'username' in session:
        show_details = queries.get_show_details(id)
        season_details = queries.get_season_details_show_id(id)
        actors = queries.get_show_actors(id)
        return render_template('show-details.html', show=show_details, seasons=season_details, actors=actors,
                               username=session['username'])
    else:
        show_details = queries.get_show_details(id)
        season_details = queries.get_season_details_show_id(id)
        actors = queries.get_show_actors(id)
        return render_template('show-details.html', show=show_details, seasons=season_details, actors=actors,
                               username='Visitor')


@app.route('/show/<int:id>/edit', methods=['GET', 'POST'])
def edit_show_details(id):
    if request.method == 'GET':
        show_details = queries.get_show_details(id)
        season_details = queries.get_season_details_show_id(id)
        actors = queries.get_show_actors(id)
        return render_template('edit-show-details.html', show=show_details, seasons=season_details, actors=actors,
                           username=session['username'])
    elif request.method == 'POST':
        show_edited_title = request.form.get('show_title')
        show_edited_date = request.form.get('show_release_date')
        show_edited_runtime = request.form.get('show_runtime')
        show_edited_rating = request.form.get('show_rating')
        show_edited_homepage = request.form.get('show_homepage')
        show_edited_trailer = request.form.get('show_trailer')
        show_edited_cover_art = request.form.get('show_cover_pic')
        show_edited_overview = request.form.get('show_overview')
        queries.modify_show_details(id, show_edited_title, show_edited_date, show_edited_runtime,
                                    show_edited_rating, show_edited_homepage, show_edited_trailer,
                                    show_edited_cover_art, show_edited_overview)
        return redirect(url_for('show_details', id=id))


@app.route('/actor/<int:id>')
def show_actor_informations(id):
    if 'username' in session:
        details = queries.get_actor_details(id)
        actor_works = queries.get_actor_works(id)
        return render_template('actor-details.html', actor=details, actor_works=actor_works,
                               username=session['username'])
    else:
        details = queries.get_actor_details(id)
        actor_works = queries.get_actor_works(id)
        return render_template('actor-details.html', actor=details, actor_works=actor_works,
                               username='Visitor')


@app.route('/actors')
def get_all_actors():
    if 'username' in session:
        actors_list = queries.get_all_actors()
        return render_template('actors.html', actors_list=actors_list, username=session['username'])
    else:
        actors_list = queries.get_all_actors()
        return render_template('actors.html', actors_list=actors_list, username='Visitor')


@app.route('/actors/most-active-actors')
def most_active_actors():
    if 'username' in session:
        most_a_actors = queries.get_most_active_actors()
        return render_template('most-active-actors.html', a_actors=most_a_actors, username=session['username'])
    else:
        most_a_actors = queries.get_most_active_actors()
        return render_template('most-active-actors.html', a_actors=most_a_actors, username='Visitor')


@app.route('/search', methods=['GET', 'POST'])
def search_show_by_title():
    if 'username' in session:
        if request.method == 'POST':
            user_search = str(request.form['title_search'])
            hits = queries.search_show_by_title(user_search)
            return render_template('search-show.html', hits=hits, username=session['username'])
        return render_template('search-show.html', username=session['username'])
    else:
        if request.method == 'POST':
            user_search = str(request.form['title_search'])
            hits = queries.search_show_by_title(user_search)
            return render_template('search-show.html', hits=hits, username='Visitor')
        return render_template('search-show.html', username='Visitor')


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
        queries.add_user_from_register(user_name, user_email, user_firstname, user_lastname, user_pssw_hashed,
                                       user_reg_date, user_role)
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
    if 'username' in session:
        session.clear()
    return redirect('/')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
