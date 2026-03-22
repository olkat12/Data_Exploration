import pandas as pd
import requests
import time

current = pd.read_csv("../data/merged/movieLens.csv")
tmdb_ids = current[current['year'] >= 1990]['tmdbId'].dropna().unique()

API_KEY = ''  # tu trzeba wkleic klucz z dostepu ktory otrzymuje sie na stronie

results = []
people = []
length = len(tmdb_ids)

print(f"Rozpoczynam pobieranie danych dla {length} filmów")

for i, movie_id in enumerate(tmdb_ids):
    print(f"{i+1} / {length}")
    movie_id = int(movie_id)

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US&"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()

            # gatunki, kraje, języki, słowa kluczowe
            genres = [g['name'] for g in data.get('genres', [])]
            countries = [c['name'] for c in data.get('production_countries', [])]
            spoken_langs = [l['name'] for l in data.get('spoken_languages', [])]
            keywords = [k['name'] for k in data.get('keywords', {}).get('keywords', [])]

            tmdbId = data.get('id')
            results.append({
                'tmdbId': tmdbId,
                'title': data.get('title'),
                'budget': data.get('budget'),
                'revenue': data.get('revenue'),
                'release_date': data.get('release_date'),
                'runtime': data.get('runtime'),
                'original_language': data.get('original_language'),
                'popularity': data.get('popularity'),
                'vote_average': data.get('vote_average'),
                'vote_count': data.get('vote_count'),
                'genres': ', '.join(genres),
                'origin_countries': ', '.join(countries),
                'spoken_languages': ', '.join(spoken_langs),
                'keywords': ', '.join(keywords)
            })

            people_url = f"https://api.themoviedb.org/3/movie/{tmdbId}/credits?api_key={API_KEY}&language=en-US"
            response = requests.get(people_url, timeout=15)

            if response.status_code == 200:
                data = response.json()

                # reżyser i scenarzyści
                crew = data.get('crew', [])
                directors = [m for m in crew if m['job'] == 'Director']
                writers = [m for m in crew if m['job'] in ['Writer', 'Screenplay', 'Author', 'Original Story']]

                # obsada (top 5 aktorow)
                cast = data.get('cast', [])
                top_actors = cast[:5]

                for actor in top_actors:
                    people.append({
                        'movie_id': tmdbId,
                        'person_id': actor['id'],
                        'name': actor['name'],
                        'gender': actor['gender'],
                        'known_for_department': actor['known_for_department'],
                        'popularity': actor['popularity'],
                        'job': 'actor'
                    })

                for person in directors + writers:
                    people.append({
                        'movie_id': tmdbId,
                        'person_id': person['id'],
                        'name': person['name'],
                        'gender': person['gender'],
                        'known_for_department': person['known_for_department'],
                        'popularity': person['popularity'],
                        'job': person['job']
                    })

        elif response.status_code == 429:
            # potrzebne ze wzgledu na limit zapytan
            time.sleep(1)

        # kopia zapasowa
        if (i + 1) % 500 == 0:
            temp_df = pd.DataFrame(results)
            temp_df.to_csv('tmdb_backup_partial.csv', index=False)

    except Exception as e:
        print(f"\nBłąd przy ID {movie_id}: {e}")
        continue

# zapis do pliku
tmdb_results_df = pd.DataFrame(results)
tmdb_results_df.to_csv('../data/tmdb/tmdb_data_from_movieLens.csv', index=False)
tmdb_people_df = pd.DataFrame(people)
tmdb_people_df.to_csv('../data/tmdb/tmdb_people_movieLens.csv', index=False)
print(f"\nPobrano dane dla {len(tmdb_results_df)} filmów")
