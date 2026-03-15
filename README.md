# Podsumowanie co zrobione (Ola) WAŻNE!
Mamy chyba pobrane wszystkie możliwe dane. Gabi pobrała i połączyła Worldwide Box Office i TMDB (po połączeniu 16822 wiersze). Ja dołączyłam do tego dane z movieLens (po połączeniu 9790 ale tutaj już mamy różne id kompatybilne z innymi plikami. Dla tych ponad 9tys filmów dzięki tmdbId pobrałam informacje o nich przez API z https://developer.themoviedb.org/docs/getting-started. Znajdują się one w **final_tmdb_data.csv** jeszcze z niczym nie łączone. W sumie jest tam 9660 filmów.
**WAŻNE** na tej stronie z API są chyba wszystkie informacje, jakich potrzebujemy. Jest nawet budżet i przychód (bez podziału na domestic i worldwide, jak to było w przypadku Worldwide Box Office). Jeśli stwierdzimy, że nam to wystarcza i nie musimy łączyć jakoś bardzo z innymi, to można by pobrać z tej strony więcej innych filmów. Musimy tu zdecydować, co pobrać z tej strony przez API, bo nie da się pobrać wszystkich filmów, tylko trzeba tam zadać które chcemy pobierać, ja dawałam po prostu konktretne tmdbId.

Jakie info mamy pobrane przez tmdb:
'title', 'budget', 'revenue', 'release_date', 'runtime', 'original_language', 'popularity', 'vote_average', 'vote_count', 'genres, 'origin_countries', 'spoken_languages', 'directors', 'writers', 'cast', 'keywords'

# Zawartość
- data - folder z surowymi danymi
  
    **merged** - tutaj wrzucone jakieś już połączone ramki danych:
     **worldWide_imdb_movieLens_merged.csv**- połączone dane ze źródeł:
      IMDB (https://datasets.imdbws.com/)
      worldwide-box-office (https://www.worldwideboxoffice.com/)
      movieLens (https://grouplens.org/datasets/movielens/latest/)
      Jest tu prawie 10 tysięcy wyników po tych łączeniach

  **tmdb** - tutaj wrzucona csv **final_tmdb_data.csv** pobrana poprzez API ze strony https://developer.themoviedb.org/docs/getting-started
  Pobrane są te filmy, które łączą się przez tmdbId z filmami w ramce worldWide_imdb_movieLens_merged.csv.
  **UWAGA** - Pobierało się to przez API ponad godzine, więc polecam po prostu sobie pobrać tą .csv do siebie, nie wysyłam kodu do pobierania tego
  

    
- data-acquisition - pozyskiwanie surowych danych

  - wbo_data_loader - skrypt do pobierania danych Worldwide Box Office
  - wbo_data_merge.ipynb - notatnik, który wczytuje dane IMDB i łączy je z danymi Worldwide Box Office
  - movielens_data_merge.ipynb - tutaj łączone do IMDB i Worldwide Box Office dane jeszcze z movieLens


# Jak uruchomić
1. Zainstaluj potrzebne pakiety z pliku requirements.txt ``pip install -r requirements.txt``
2. Uruchom skrypt data_loader.py (pobranie danych ze strony https://www.worldwideboxoffice.com/)
3. Pobierz dane ze strony https://datasets.imdbws.com/ i umieść nierozpakowane foldery w folderze data/imdb
4. Uruchom notebook data_aquisition/wbo_data_merge.ipynb - połączenie danych IMDB oraz WorldwideBoxOffice
5. Pobierz dane ml-latest.zip ze strony https://grouplens.org/datasets/movielens/latest/ i umieść je rozpakowane w folderze data/movieLens

