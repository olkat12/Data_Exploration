
import pandas as pd
import requests
import time

# bierzemy te id filmów, gdzie nam brakuje keywords/director/writer
df = pd.read_csv('data/merged/merged_data.csv')
API_KEY = ''  #  tutaj trzeba wkleić klucz ze strony tmdb

missing_mask = df['keywords'].isna() | df['director_id'].isna() | df['writer_id'].isna()
movies_to_fetch = df[missing_mask]['tmdbId'].dropna().unique()

print(f"Do pobrania z API: {len(movies_to_fetch)} filmów.")

results = []

for i, tmdb_id in enumerate(movies_to_fetch):
    tmdb_id = int(tmdb_id)
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&append_to_response=keywords,credits"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            movie_info = {'tmdbId': tmdb_id}
            
            # keywords
            kw_data = data.get('keywords', {}).get('keywords', [])
            if kw_data:
                movie_info['keywords'] = ', '.join([k['name'] for k in kw_data])

            # crew
            crew = data.get('credits', {}).get('crew', [])
            
            directors = [c for c in crew if c.get('job') == 'Director']
            if directors:
                best_director = max(directors, key=lambda x: x.get('popularity', 0))
                movie_info['director_id'] = best_director.get('id')
                movie_info['director_name'] = best_director.get('name')
                movie_info['director_popularity'] = best_director.get('popularity')
                movie_info['director_gender'] = best_director.get('gender')

            writers = [c for c in crew if c.get('job') in ['Writer', 'Screenplay', 'Author', 'Original Story']]
            if writers:
                best_writer = max(writers, key=lambda x: x.get('popularity', 0))
                movie_info['writer_id'] = best_writer.get('id')
                movie_info['writer_name'] = best_writer.get('name')
                movie_info['writer_popularity'] = best_writer.get('popularity')
                movie_info['writer_gender'] = best_writer.get('gender')
                

            results.append(movie_info)
            
        elif response.status_code == 429:
            print("Limit zapytań! Czekam 2 sekundy...")
            time.sleep(2)
            
    except Exception as e:
        print(f"Błąd przy ID {tmdb_id}: {e}")
        
    if (i + 1) % 100 == 0:
        print(f"Pobrano {i + 1} / {len(movies_to_fetch)}...")
        pd.DataFrame(results).to_csv('missing_data.csv', index=False)
    
    time.sleep(0.05)

pd.DataFrame(results).to_csv('missing_data.csv', index=False)
print("\nGotowe")

