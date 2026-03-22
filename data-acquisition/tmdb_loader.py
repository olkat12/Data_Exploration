import pandas as pd
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

current = pd.read_csv("../data/merged/movieLens.csv")
tmdb_ids = current[current['year'] >= 1990]['tmdbId'].dropna().unique()

API_KEY = ''  # tu trzeba wkleic klucz z dostepu ktory otrzymuje sie na stronie

movies = []
people = []

def fetch_movie_details(tmdb_id):
    movie_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=en-US&append_to_response=keywords,credits"

    while True:
        r = requests.get(movie_url, timeout=15)
        if r.status_code == 429:
            time.sleep(1)
            continue
        elif r.status_code != 200:
            return None, None
        else:
            break

    movie_json = r.json()

    budget = movie_json.get('budget')
    revenue = movie_json.get('revenue')
    countries = ', '.join([c['name'] for c in movie_json.get('production_countries', [])])
    spoken_langs = ', '.join([l['name'] for l in movie_json.get('spoken_languages', [])])
    runtime = movie_json.get('runtime')
    keywords = [k['name'] for k in movie_json.get('keywords', {}).get('keywords', [])]

    movie_dict = {
        'tmdbId': tmdb_id,
        'title': movie_json.get('title'),
        'budget': budget,
        'revenue': revenue,
        'release_date': movie_json.get('release_date'),
        'runtime': runtime,
        'original_language': movie_json.get('original_language'),
        'popularity': movie_json.get('popularity'),
        'vote_average': movie_json.get('vote_average'),
        'vote_count': movie_json.get('vote_count'),
        'genres': ', '.join(g['name'] for g in movie_json.get('genres', [])),
        'origin_countries': countries,
        'spoken_languages': spoken_langs,
        'keywords': ', '.join(keywords)
    }

    people_list = []
    credits = movie_json.get('credits', {})
    crew = credits.get('crew', [])
    directors = [m for m in crew if m['job'] == 'Director']
    writers = [m for m in crew if m['job'] in ['Writer', 'Screenplay', 'Author', 'Original Story']]
    cast = credits.get('cast', [])[:5]  # top 5 aktorów

    for actor in cast:
        people_list.append({
            'movie_id': tmdb_id,
            'person_id': actor['id'],
            'name': actor['name'],
            'gender': actor['gender'],
            'known_for_department': actor['known_for_department'],
            'popularity': actor['popularity'],
            'job': 'actor'
        })

    for person in directors + writers:
        people_list.append({
            'movie_id': tmdb_id,
            'person_id': person['id'],
            'name': person['name'],
            'gender': person['gender'],
            'known_for_department': person['known_for_department'],
            'popularity': person['popularity'],
            'job': person['job']
        })

    return movie_dict, people_list


def get_movie_data(date_from, date_to, max_movies=500):
    results_temp = []
    people_temp = []

    total_pages = 1000
    i = 0

    for page in range(1, min(total_pages, 500) + 1):
        if i >= max_movies:
            break

        url = (
            f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&"
            f"language=en-US&primary_release_date.gte={date_from}&primary_release_date.lte={date_to}&page={page}"
        )

        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 429:
                time.sleep(1)
                continue
            elif r.status_code != 200:
                continue

            discover_data = r.json()
            if total_pages == 1000:
                total_pages = discover_data.get("total_pages", 1)

            tmdb_ids_batch = [m['id'] for m in discover_data.get('results', [])]

            # ThreadPoolExecutor do równoległego pobierania szczegółów filmów
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(fetch_movie_details, tmdb_id): tmdb_id for tmdb_id in tmdb_ids_batch}

                for future in as_completed(futures):
                    movie_dict, people_list = future.result()
                    if movie_dict is None:
                        continue
                    results_temp.append(movie_dict)
                    people_temp.extend(people_list)
                    i += 1

        except Exception as e:
            print("Błąd requestu:", e)
            continue

    return results_temp, people_temp


for year in range(1990, 2026):
    print(f"Rok: {year}")
    movies_temp1, people_temp1 = get_movie_data(f'{year}-01-01', f'{year}-06-30')
    movies_temp2, people_temp2 = get_movie_data(f'{year}-07-01', f'{year}-12-31')

    movies.extend(movies_temp1)
    movies.extend(movies_temp2)
    people.extend(people_temp1)
    people.extend(people_temp2)

tmdb_movies_df = pd.DataFrame(movies)
tmdb_movies_df.to_csv('../data/tmdb/tmdb_data.csv', index=False)
tmdb_people_df = pd.DataFrame(people)
tmdb_people_df.to_csv('../data/tmdb/tmdb_people.csv', index=False)
