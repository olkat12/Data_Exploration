import pandas as pd
import requests
import time
from tqdm import tqdm

current = pd.read_csv("../data/merged/worldWide_imdb_movieLens_merged.csv")
tmdb_ids = current['tmdbId'].dropna().unique()

API_KEY = ''  # tu trzeba wkleic klucz z dostepu ktory otrzymuje sie na stronie

results = []

print(f"Rozpoczynam pobieranie danych dla {len(tmdb_ids)} filmów")


for i, movie_id in enumerate(tqdm(tmdb_ids)):
    tmdb_id_int = int(movie_id)
    
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id_int}?api_key={API_KEY}&language=en-US&append_to_response=credits,keywords"
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # gatunki, kraje, języki
            genres = [g['name'] for g in data.get('genres', [])]
            countries = [c['name'] for c in data.get('production_countries', [])]
            spoken_langs = [l['name'] for l in data.get('spoken_languages', [])]
            
            # reżyser i scenarzyści
            crew = data.get('credits', {}).get('crew', [])
            directors = [m['name'] for m in crew if m['job'] == 'Director']
            writers = [m['name'] for m in crew if m['job'] in ['Writer', 'Screenplay', 'Author', 'Original Story']]
            
            # obsada (top 5 aktorow)
            cast = data.get('credits', {}).get('cast', [])
            top_actors = [m['name'] for m in cast[:5]]
            
            # slowa kluczowe
            keywords = [k['name'] for k in data.get('keywords', {}).get('keywords', [])]
            
            results.append({
                'tmdbId': movie_id,
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
                'directors': ', '.join(directors),
                'writers': ', '.join(writers),
                'cast': ', '.join(top_actors),
                'keywords': ', '.join(keywords)
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
tmdb_results_df.to_csv('missing_tmdb_data.csv', index=False)

print(f"\nPobrano dane dla {len(tmdb_results_df)} filmów")

