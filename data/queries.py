from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title, overview, cover_pic FROM shows;')


def get_most_rated_shows():
    return data_manager.execute_select("""
    SELECT shows.id,
       shows.title,
       shows.year,
       shows.runtime,
       shows.rating,
       string_agg(genres.name, ', ') as genres,
       shows.trailer,
       shows.homepage
    FROM shows
         INNER JOIN show_genres ON shows.id = show_genres.show_id
         INNER JOIN genres ON show_genres.genre_id = genres.id
    GROUP BY shows.id, rating
    ORDER BY rating DESC;
    """)


def get_show_details(show_id):
    return data_manager.execute_select("""
    SELECT shows.id,
       shows.title,
       shows.year,
       shows.runtime,
       shows.rating,
       string_agg(DISTINCT genres.name, ', ') as genres,
       shows.trailer,
       shows.homepage,
       shows.overview,
       string_agg(DISTINCT character_name, ', ') AS charaters_name,
       string_agg(DISTINCT a.name, ', ') AS actors_name,
       shows.cover_pic
    FROM shows
         INNER JOIN show_genres ON shows.id = show_genres.show_id
         INNER JOIN genres ON show_genres.genre_id = genres.id
         INNER JOIN show_characters sc on shows.id = sc.show_id
         INNER JOIN actors a on sc.actor_id = a.id
    WHERE shows.id = %(show_id)s
    GROUP BY shows.id, rating
    ORDER BY rating DESC;
    """, {'show_id': show_id})


def get_season_details_show_id(show_id):
    return data_manager.execute_select("""
    SELECT shows.id,
       season_number,
       seasons.title,
       seasons.overview
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    WHERE shows.id = %(show_id)s
    GROUP BY shows.id, season_number, seasons.title, seasons.overview
    ORDER BY season_number ASC;
    """, {'show_id': show_id})


def get_show_actors(show_id):
    return data_manager.execute_select("""
    SELECT 
        shows.id,
        sc.id,
        sc.actor_id,
        a.name,
        character_name
    FROM shows
        INNER JOIN show_characters sc on shows.id = sc.show_id
        INNER JOIN actors a on sc.actor_id = a.id
    WHERE shows.id = %(show_id)s
    GROUP BY a.name, shows.id, character_name, sc.id
    order by sc.id;
    """, {'show_id': show_id})


def get_actor_details(actor_id):
    return data_manager.execute_select("""
    SELECT 
        DISTINCT actors.name,
        actors.birthday,
        actors.death,
        actors.biography
    FROM actors
        INNER JOIN show_characters sc on actors.id = sc.actor_id
        INNER JOIN shows s on s.id = sc.show_id
    WHERE actor_id = %(actor_id)s;
    """, {'actor_id': actor_id})


def get_actor_works(actor_id):
    return data_manager.execute_select("""
    SELECT 
        s.title,
        s.id            
    FROM actors
        INNER JOIN show_characters sc on actors.id = sc.actor_id
        INNER JOIN shows s on s.id = sc.show_id
    WHERE actor_id = %(actor_id)s;
    """, {'actor_id': actor_id})


def get_all_actors():
    return data_manager.execute_select("""
    SELECT
        id,
        name
    FROM actors
    ORDER BY name ASC;
    """)


def get_most_active_actors():
    return data_manager.execute_select("""
    SELECT
        actors.id,
        actors.name,
        (CURRENT_DATE - actors.birthday) / 365 AS age,
        (actors.death - actors.birthday) / 365 AS age_of_death,
        COUNT(s.id) AS number_of_shows
    FROM actors
        INNER JOIN show_characters sc on actors.id = sc.actor_id
        INNER JOIN shows s on s.id = sc.show_id
    GROUP BY actors.id
    ORDER BY number_of_shows DESC;
    """)


def search_show_by_title(search_word):
    return data_manager.execute_select(f"""
    SELECT
        id,
        title,
        rating,
        shows.year,
        trailer
    FROM shows
    WHERE title ILIKE '%{search_word}%';
    """)


def add_user_from_register(user_name, user_email, user_firstname, user_lastname, user_pssw_hashed, user_reg_date, user_role):
    data_manager.execute_insert("""
    INSERT INTO ud (user_name, email, first_name, last_name, hash_pass, reg_date, user_role)
    VALUES ( %(un)s, %(el)s, %(fn)s, %(ln)s, %(hp)s, %(rd)s, %(ur)s);
    """, {'un': user_name, 'el': user_email, 'fn': user_firstname, 'ln': user_lastname, 'hp': user_pssw_hashed, 'rd': user_reg_date, 'ur': user_role})


def get_user_from_login(user_name):
    return data_manager.execute_select("""
    SELECT
        user_name,
        hash_pass
    FROM ud
    WHERE user_name = %(un)s;
    """, {'un': user_name})


def modify_show_details(idn, title, date, runtime, rating, homepage, trailer, cover, overview):
    data_manager.execute_insert("""
    UPDATE shows
    SET 
        title = %(st)s,
        year = %(sd)s,
        overview = %(so)s,
        runtime = %(sr)s,
        trailer = %(strail)s,
        homepage = %(sh)s,
        rating = %(srat)s,
        cover_pic = %(sc)s
    WHERE id = %(id)s;
    """, {'id': idn, 'st': title, 'sd': date, 'so': overview, 'sr': runtime, 'strail': trailer,
          'sh': homepage, 'srat': rating, 'sc': cover})
