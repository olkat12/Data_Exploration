# Zawartość
- data - folder z surowymi danymi
  
   - movieLens - dane z Movie Lens (https://grouplens.org/datasets/movielens/latest/)
   - tmdb - dane pobrane ze strony TMDB (https://developer.themoviedb.org/reference/discover-movie)
   - cpi.xlsx - dane o inflacji w USA w latach 1950-2025 (https://data.bls.gov/timeseries/CUUR0000SA0)
   - merged - połączone dane:
      - merged_data.csv - po prostu surowe ale już połączone dane, dalej przekazywane do czyszczenia
      - clean_data.csv ( troche czyszczone dane, używane w notatniku first_data_analysis.ipynb)
      - **NEW_clean_data.csv** (bazują na clean_data, ale już mają wyrzucone braki w danych, starsze filmy itp. **To jest nasza NAJNOWSZA ramka używana w NEW_visualization.ipynb**)

    
- data-acquisition - pozyskiwanie surowych danych

  - movieLens.ipynb - przetwarzane i łączone dane z MovieLens (plik wynikowy to data/merged/movieLens.csv)
  - tmdb_loader_from_movieLens.py - skrypt do pobierania danych ze strony TMDB powiązanych ze źródeł movieLens (filmy - tmdb/tmdb_data_from_movieLens.csv, ludzie - tmdb/tmdb_people_movieLens.csv)
  - tmdb_loader.py - skrypt do pobierania danych ze strony TMDB, które nie znalazły się w bazie MovieLens - pobieranie po 1-2 tys. najpopularniejszych filmów z lat 1950-2025, które nie znalazły się w bazie MovieLens (filmy - tmdb/tmdb_data.csv, ludzie - tmdb/tmdb_people.csv)
  - missing_data_loader.py - skrypt do pobierania dancyh których nam jeszcze brakowało (rezultatem data/tmdb_missing.csv)
  - data_merge.ipynb - łączenie danych TMDB o filmach i ludziach, movieLens oraz o inflacji, wstępne przetwarzanie (plik wynikowy to merged/merged_data.csv)

- data-cleaning - czyszczenie danych
  - cleaning.ipynb - plik z wstępnym czyszczeniem danych, zakończony już, rezultatem jest /merged/clean_data.csv
  - **NEW_cleaning.ipynb** - tutaj do kontynuacji. Nasze najnowsze dane czyszczone bez braków, bez starych filmów itp  - wykorzystujemy je w nowych wizualizacjach, **do kontynuowania tutaj** rezultatem jest /merged/NEW_clean_data.csv oraz /merged/data_coded.csv gdzie już kodujemy kolumny 0-1


- data-visualization - wizualizacja i analizy
  - first_data_analysis.ipynb - to stare wizualizacje dla wszystkich danych trochę wyczyszczonych, na ramce clean_data.csv
  - NEW_visualization.ipynb - tutaj już wizualizacje na ramce NEW_cleaning.ipynb czyli nasze najnowsze, **do kontynuowania tutaj**


Jakie info mamy pobrane przez tmdb:
'title', 'budget', 'revenue', 'release_date', 'runtime', 'original_language', 'popularity', 'vote_average', 'vote_count', 'genres, 'origin_countries', 'spoken_languages', 'directors', 'writers', 'cast', 'keywords'

### Uwagi
- wybrane zostały filmy z lat 1950-2025
- dane pieniężne (budget i revenue) zostały ujednolicone pod względem inflacji z 2025 roku
- w sumie wszystkich filmów jest ponad 415 tys., jednak ze znanym przychodem jest tylko ok. 20 tys. ...

# Jak uruchomić
1. Zainstaluj potrzebne pakiety z pliku requirements.txt ``pip install -r requirements.txt``
2. Zainstaluj Git Large File Storage (https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)
   - jakby pliki pobrały się nieprawidłowo, to w git bash należy wpisać komendę: ``git lfs pull``
3. Pobierz dane ml-latest.zip ze strony https://grouplens.org/datasets/movielens/latest/ i umieść je rozpakowane w folderze data/movieLens
5. Uruchom notebook data_aquisition/movieLens_data.ipynb - wynikiem plik movieLens.csv
6. Uruchom notebook data_aquisition/data_merge.ipynb (data/merged/merged_data.csv to plik z połączonymi wszystkimi danymi) (może się wykonywać kilka minut) wynikiem jest plik merged_data.csv
7. Uruchom notebook data-cleaning/cleaning - to plik, w którym robimy czyszczenie na ramce merged_data.csv uzyskanej po puszczeniu notebooka w poprzednim punkcie. Na razie nie skończone - od tego miejsca kontynuować. Wynikami pliki clean_data.csv oraz data_coded.csv
8. Jeśli chcesz przejść do części z wykresami i analizą danych to uruchom data-visualization/first_data_analysis.ipynb. Tu wykonujemy wykresy i analizy dla ramki wyczyszczonej w punkcie 7 (clean_data.csv)

### Nie jest konieczne, ale można
- Uruchomienie skryptów data_aquisition/tmdb_loder.py oraz data_aquisition/tmdb_loder_from_movieLens.py pozwala na pobranie danych TMDB

