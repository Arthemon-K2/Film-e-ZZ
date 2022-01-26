from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


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
       string_agg(DISTINCT a.name, ', ') AS actors_name
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
    ORDER BY season_number ASC
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
    order by sc.id
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
    WHERE actor_id = %(actor_id)s
    """, {'actor_id': actor_id})


def get_actor_works(actor_id):
    return data_manager.execute_select("""
    SELECT 
        s.title,
        s.id            
    FROM actors
        INNER JOIN show_characters sc on actors.id = sc.actor_id
        INNER JOIN shows s on s.id = sc.show_id
    WHERE actor_id = %(actor_id)s
    """, {'actor_id': actor_id})


def get_all_actors():
    return data_manager.execute_select("""
    SELECT
        id,
        name
    FROM actors
    ORDER BY name ASC
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
