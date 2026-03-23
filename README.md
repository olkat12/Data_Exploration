# Zawartość
- data - folder z surowymi danymi
  
   - imdb - dane z IMDB (https://datasets.imdbws.com/)
   - movieLens - dane z Movie Lens (https://grouplens.org/datasets/movielens/latest/)
   - tmdb - dane pobrane ze strony TMDB (https://developer.themoviedb.org/reference/discover-movie)
   - cpi.xlsx - dane o inflacji w USA w latach 1990-2025 (https://data.bls.gov/timeseries/CUUR0000SA0)
   - merged - połączone dane

    
- data-acquisition - pozyskiwanie surowych danych

  - wbo_data_loader.py - skrypt do pobierania danych Worldwide Box Office (już nie wykorzystywany)
  - imdb_data.ipynb - notatnik, który wczytuje dane IMDB i je przetwarza (plik wynikowy to data/merged/imdb.csv oraz directors_named.csv i writers_named.csv)
  - movieLens.ipynb - przetwarzane i łączone dane z MovieLens (plik wynikowy to data/merged/movieLens.csv)
  - tmdb_loader_from_movieLens.py - skrypt do pobierania danych ze strony TMDB powiązanych ze źródeł movieLens (filmy - tmdb/tmdb_data_from_movieLens.csv, ludzie - tmdb/tmdb_people_movieLens.csv)
  - tmdb_loader.py - skrypt do pobierania danych ze strony TMDB, które nie znalazły się w bazie MovieLens - pobieranie po 1000 najpopularniejszych filmów z lat 1990-2025, które nie znalazły się w bazie MovieLens (filmy - tmdb/tmdb_data.csv, ludzie - tmdb/tmdb_people.csv)
  - data_merge.ipynb - łączenie danych TMDB o filmach i ludziach, movieLens oraz o inflacji, wstępne przetwarzanie (plik wynikowy to merged/merged_data.csv)

Jakie info mamy pobrane przez tmdb:
'title', 'budget', 'revenue', 'release_date', 'runtime', 'original_language', 'popularity', 'vote_average', 'vote_count', 'genres, 'origin_countries', 'spoken_languages', 'directors', 'writers', 'cast', 'keywords'

### Uwagi
- dane z IMDB pokrywają się z danymi MovieLens oraz TMDB, dlatego nie są używane
- wybrane zostały filmy z lat 1990-2025
- dane pieniężne (budget i revenue) zostały ujednolicone pod względem inflacji z 2025 roku
- w sumie wszystkich filmów jest ponad 74 tys., jednak ze znanym przychodem jest tylko ok. 14 tys. ...

# Jak uruchomić
1. Zainstaluj potrzebne pakiety z pliku requirements.txt ``pip install -r requirements.txt``
2. Pobierz dane ml-latest.zip ze strony https://grouplens.org/datasets/movielens/latest/ i umieść je rozpakowane w folderze data/movieLens
3. Uruchom notebook data_aquisition/movieLens_data.ipynb
4. Uruchom notebook data_aquisition/data_merge.ipynb (data/merged/merged_data.csv to plik z połączonymi wszystkimi danymi)

### Nie jest konieczne, ale można
- Pobierz dane ze strony https://datasets.imdbws.com/ i umieść nierozpakowane foldery w folderze data/imdb, aby uruchomić skrypt data_aquisition/imdb_data.ipynb 
- Uruchomienie skryptów data_aquisition/tmdb_loder.py oraz data_aquisition/tmdb_loder_from_movieLens.py pozwala na pobranie danych TMDB

