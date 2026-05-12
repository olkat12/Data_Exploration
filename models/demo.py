import pandas as pd

GENRES = {
    "action",
    "adventure",
    "animation",
    "children",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "family",
    "fantasy",
    "film-noir",
    "history",
    "horror",
    "imax",
    "musical",
    "mystery",
    "romance",
    "sci-fi",
    "thriller",
    "tvmovie",
    "war",
    "western"
}

KEYWORDS = {
    "based_on_book",
    "original",
    "action",
    "violence",
    "funny",
    "true_story",
    "teen",
    "comedy",
    "love",
    "girlie_movie",
    "horror",
    "drama",
    "family",
    "sequel",
    "murder",
    "remake",
    "woman_director",
    "animation",
    "mentor",
    "romantic",
    "predictable",
    "supernatural",
    "independent_film",
    "sports",
    "weird",
    "friendship",
    "chase",
    "relationships",
    "visually_appealing",
    "suspense",
    "romantic_comedy",
    "new_york_city",
    "serial_killer",
    "revenge",
    "musical",
    "high_school",
    "small_town",
    "superhero",
    "alien",
    "biography",
    "fantasy_world"
}

COUNTRIES = {
    "Canada",
    "France",
    "Germany",
    "India",
    "USA",
    "UnitedKingdom",
    "Other"
}

people = pd.read_csv('../data/merged/NEW_clean_data.csv')
for i in range(1, 6):
    counts = people[f'actor{i}_id'].value_counts()
    people[f'actor{i}_movie_count'] = people[f'actor{i}_id'].map(counts)

directors = people[["director_id", "director_name", "director_gender", 'director_movie_count', "director_max_revenue", "director_avg_revenue"]].copy()
director_counts = directors['director_id'].value_counts()
directors['director_movie_count'] = directors['director_id'].map(director_counts)
DIRECTORS = directors.drop_duplicates()

writers = people[["writer_id", "writer_name", "writer_gender", 'writer_movie_count', "writer_max_revenue", "writer_avg_revenue"]].copy()
writer_counts = writers['writer_id'].value_counts()
writers['writer_movie_count'] = writers['writer_id'].map(writer_counts)
WRITERS = writers.drop_duplicates()

actor_columns = [c for c in people.columns if "actor" in c]
actors = people[actor_columns]
actors = actors.drop(["female_actors", "actors_avg_revenue", "actors_max_revenue", "actors_avg_movie_count"], axis=1)

actors_list = []
for i in range(1, 6):
    temp = actors[[
        f"actor{i}_id",
        f"actor{i}_name",
        f"actor{i}_gender",
        f"actor{i}_avg_revenue",
        f"actor{i}_max_revenue",
        f"actor{i}_movie_count"
    ]].copy()

    temp.columns = [
        "actor_id",
        "actor_name",
        "actor_gender",
        "actor_avg_revenue",
        "actor_max_revenue",
        "actor_movie_count"
    ]

    actors_list.append(temp)

actors = pd.concat(actors_list, ignore_index=True)
ACTORS = actors.drop_duplicates()


def adjust_budget(budget, year, base_year=2025):
    cpi = pd.read_excel('../data/cpi.xlsx', skiprows=11)
    cpi = cpi[['Year', 'Annual']].set_index('Year').to_dict()['Annual']
    return round(budget * (cpi[base_year] / cpi[year]), 2)


def add_onehot(df, movie_categories, categories):
    for category in categories:
        if categories == KEYWORDS:
            df[f"kw_{category}"] = int(category in movie_categories)
        else:
            df[category] = int(category in movie_categories)
    return df


def add_people_data(df, data):
    director = DIRECTORS[DIRECTORS['director_name'] == data['director']]
    if not director.empty:
        director = director.iloc[0]
        df['director_movie_count'] = director['director_movie_count']
        df['director_max_revenue'] = director['director_max_revenue']
        df['director_avg_revenue'] = director['director_avg_revenue']
    else:
        df['director_movie_count'] = 0
        df['director_max_revenue'] = 0
        df['director_avg_revenue'] = 0

    writer = WRITERS[WRITERS['writer_name'] == data['writer']]
    if not writer.empty:
        writer = writer.iloc[0]
        df['writer_movie_count'] = writer['writer_movie_count']
        df['writer_max_revenue'] = writer['writer_max_revenue']
        df['writer_avg_revenue'] = writer['writer_avg_revenue']
    else:
        df['writer_movie_count'] = 0
        df['writer_max_revenue'] = 0
        df['writer_avg_revenue'] = 0

    for i in range(5):
        actor = ACTORS[ACTORS['actor_name'] == data['actors'][i]]
        if not actor.empty:
            actor = actor.iloc[0]
            df[f'actor{i+1}_movie_count'] = actor['actor_movie_count']
            df[f'actor{i+1}_max_revenue'] = actor['actor_max_revenue']
            df[f'actor{i+1}_avg_revenue'] = actor['actor_avg_revenue']
            df[f'actor{i+1}_gender'] = actor['actor_gender']
        else:
            df[f'actor{i+1}_movie_count'] = 0
            df[f'actor{i+1}_max_revenue'] = 0
            df[f'actor{i+1}_avg_revenue'] = 0
            df[f'actor{i+1}_gender'] = 0


    df['actors_avg_revenue'] =\
        df[[f'actor{i}_avg_revenue' for i in range(1,6) if f'actor{i}_avg_revenue' ]].mean(axis=1)
    df['actors_max_revenue'] = (
        df[[f'actor{i}_max_revenue' for i in range(1,6) if f'actor{i}_max_revenue']].mean(axis=1))
    df['actors_avg_movie_count'] =\
        df[[f'actor{i}_movie_count' for i in range(1,6)]].mean(axis=1)
    df['female_actors'] = (
            df[[f'actor{i}_gender' for i in range(1,6)]] == 1
    ).sum(axis=1)

    df = df.drop(columns=[f'actor{i}_avg_revenue' for i in range(1, 6)])
    df = df.drop(columns=[f'actor{i}_max_revenue' for i in range(1, 6)])
    df = df.drop(columns=[f'actor{i}_movie_count' for i in range(1, 6)])
    df = df.drop(columns=[f'actor{i}_gender' for i in range(1, 6)])

    return df


def add_top_people_data(df, actors, director, writer):
    actors = pd.DataFrame({"actors": actors})
    director = pd.DataFrame({"director": [director]})
    writer = pd.DataFrame({"writer": [writer]})

    top_actors = pd.read_csv('../data/top_people/top100_actors.csv')['Name'].to_list()
    top_actors_today = pd.read_csv('../data/top_people/top100_actors_today.csv')['Name'].to_list()
    top_actors_all = set(top_actors + top_actors_today)
    top_directos = pd.read_csv('../data/top_people/top_directors.csv')['Name'].to_list()
    top_writers = pd.read_csv('../data/top_people/top_writers.csv')['Name'].to_list()

    df['top_actors_number'] = (actors).isin(top_actors_all).sum(axis=1)

    df['top_director_number'] = director.isin(top_directos).astype(int)
    df['top_writer_number'] = writer.isin(top_writers).astype(int)

    df['top_actors'] = (actors).isin(top_actors_all).any(axis=1)

    df['top_director'] = director.isin(top_directos)
    df['top_writer'] = writer.isin(top_writers)

    df['top_people_number'] = df['top_actors_number'] + df['top_director_number'] + df['top_writer_number']
    df['top_people'] = df['top_actors'] | df['top_director'] | df['top_writer']

    df.drop(columns=['top_actors_number', 'top_director_number', 'top_writer_number', 'top_actors', 'top_director', 'top_writer', 'top_people'], inplace=True)
    return df


def transform_data(data):
    df = pd.DataFrame(
        columns=['runtime', 'year', 'quarter'],
        data=[[data['runtime'], data['year'], data['quarter']]],
    )
    df['budget_adjusted'] = adjust_budget(data['budget'], data['year'])
    df['lang_en'] = int(data['original_language'] == 'en')
    df['lang_other'] = int(data['original_language'] != 'en')

    df = add_people_data(df, data)
    df = add_top_people_data(df, data['actors'], data['director'], data['writer'])

    valid_genres = [g for g in data['genres'] if g in GENRES]
    valid_keywords = [k for k in data['keywords'] if k in KEYWORDS]

    df = add_onehot(df, data['country'], COUNTRIES)
    df = add_onehot(df, valid_genres, GENRES)
    df = add_onehot(df, valid_keywords, KEYWORDS)

    df = df[['runtime', 'year', 'budget_adjusted', 'quarter',
       'director_movie_count', 'writer_movie_count', 'actors_avg_movie_count',
       'writer_avg_revenue', 'writer_max_revenue', 'director_avg_revenue',
       'director_max_revenue', 'actors_avg_revenue', 'actors_max_revenue',
       'female_actors', 'top_people_number', 'action', 'adventure',
       'animation', 'children', 'comedy', 'crime', 'documentary', 'drama',
       'family', 'fantasy', 'film-noir', 'history', 'horror', 'imax',
       'musical', 'mystery', 'romance', 'sci-fi', 'thriller', 'tvmovie', 'war',
       'western', 'lang_en', 'lang_other', 'Canada', 'France', 'Germany',
       'India', 'Other', 'USA', 'UnitedKingdom', 'kw_based_on_book',
       'kw_original', 'kw_action', 'kw_violence', 'kw_funny', 'kw_true_story',
       'kw_teen', 'kw_comedy', 'kw_love', 'kw_girlie_movie', 'kw_horror',
       'kw_drama', 'kw_family', 'kw_sequel', 'kw_murder', 'kw_remake',
       'kw_woman_director', 'kw_animation', 'kw_mentor', 'kw_romantic',
       'kw_predictable', 'kw_supernatural', 'kw_independent_film', 'kw_sports',
       'kw_weird', 'kw_friendship', 'kw_chase', 'kw_relationships',
       'kw_visually_appealing', 'kw_suspense', 'kw_romantic_comedy',
       'kw_new_york_city', 'kw_serial_killer', 'kw_revenge', 'kw_musical',
       'kw_high_school', 'kw_small_town', 'kw_superhero', 'kw_alien',
       'kw_biography', 'kw_fantasy_world']]

    return df

import pickle
def predict(raw_data, model_path="../models/model_rf.pickle"):

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    transformed_data = transform_data(raw_data)
    return model.predict(transformed_data)[0]


if __name__ == '__main__':
    input = {
        "runtime": 102,
        "year": 2013,
        "quarter": 4,
        "budget": 150000000,
        "genres": ["children", "animation", "family", "fantasy"],
        "keywords": ["love", "fantasy_world", "relationships", "family", "original"],
        "original_language": "en",
        "country": "USA",
        "director": "Chris Buck",
        "writer": "Jennifer Lee",
        "actors": ["Josh Gad", "Kristen Bell", "Kristen Bell", "Idina Menzel", "Josh Gad"],
    }
    print(predict(input))
