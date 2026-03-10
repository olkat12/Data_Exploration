# Zawartość
- data - folder z surowymi danymi
  - imdb - dane ze źródła IMDB (https://datasets.imdbws.com/)
  - worldwide-box-office - dane ze źródła https://www.worldwideboxoffice.com/
- data-acquisition - pozyskiwanie surowych danych
  - data_loader - skrypt do pobierania danych Worldwide Box Office
  - data_merge.ipynb - notatnik, który wczytuje dane IMDB i łączy je z danymi Worldwide Box Office

# Jak uruchomić
1. Zainstaluj potrzebne pakiety z pliku requirements.txt ``pip install -r requirements.txt``
2. Uruchom skrypt data_loader.py (pobranie danych ze strony https://www.worldwideboxoffice.com/)
3. Pobierz dane ze strony https://datasets.imdbws.com/ i umieść nierozpakowane foldery w folderze data/imdb
4. Uruchom notebook data_aquisition/data_merge.ipynb - połączenie danych IMDB oraz WorldwideBoxOffice
