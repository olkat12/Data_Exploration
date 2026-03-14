# Zawartość
- data - folder z surowymi danymi
  
    **merged** - tutaj wrzucone jakieś już połączone ramki danych:
     **worldWide_imdb_movieLens_merged.csv**- połączone dane ze źródeł:
      IMDB (https://datasets.imdbws.com/)
      worldwide-box-office (https://www.worldwideboxoffice.com/)
      movieLens (https://grouplens.org/datasets/movielens/latest/)
      Jest tu około 6 tysięcy wyników po tych łączeniach

  **tmdb** - tutaj wrzucona csv **final_tmdb_data.csv** pobrana poprzez API ze strony https://developer.themoviedb.org/docs/getting-started
  Pobrane są te filmy, które łączą się przez tmdbId z filmami w ramce worldWide_imdb_movieLens_merged.csv.
  Pobierało się to przez API ponad godzine, więc polecam po prostu sobie pobrać tą .csv do siebie, nie wysyłam kodu do pobierania tego
  

    
- data-acquisition - pozyskiwanie surowych danych

  - data_loader - skrypt do pobierania danych Worldwide Box Office
  - data_merge.ipynb - notatnik, który wczytuje dane IMDB i łączy je z danymi Worldwide Box Office
  - other_datasets_merge.ipynb - tutaj łączone do IMDB i Worldwide Box Office dane jeszcze z movieLens


# Jak uruchomić
1. Zainstaluj potrzebne pakiety z pliku requirements.txt ``pip install -r requirements.txt``
2. Uruchom skrypt data_loader.py (pobranie danych ze strony https://www.worldwideboxoffice.com/)
3. Pobierz dane ze strony https://datasets.imdbws.com/ i umieść nierozpakowane foldery w folderze data/imdb
4. Uruchom notebook data_aquisition/data_merge.ipynb - połączenie danych IMDB oraz WorldwideBoxOffice

5. Pobierz dane ml-latest.zip ze strony https://grouplens.org/datasets/movielens/latest/ i umiećś je rozpakowane w folderze data/movieLens
6. Pobierz dane final_tmdb_data.csv z tego githuba i umieść w folderze data/tmdb
7. Tak samo pobierz dane worldWide_imdb_movieLens_merged.csv z tego githuba i umieść w folderze data/merged

