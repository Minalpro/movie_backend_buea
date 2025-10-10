# %%
from database import SessionLocal
from query_helpers import *

db = SessionLocal()
# %%
movie = get_movie(db, movie_id = 5)
print(movie.title, movie.genres)

db.close()

# %%
movies = get_movies(db, limit = 5)
for film in movies:
    print(f"ID: {film.movieId}, Titre:{film.title}, Genres:{film.genres}")

db.close()
# %%
rating = get_rating(db, movie_id=1, user_id= 1)
print(f"User ID: {rating.userId}, Movie ID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}")

db.close()
# %%
ratings = get_ratings(db, min_rating=3.5, limit=10, user_id=1)
for eval in ratings:
    print(f"ID: {eval.movieId}, Note: {eval.rating}")

db.close()
# %%
tag = get_tag(db, user_id=2, movie_id=60756, tag_text="funny")
print(f"User ID: {tag.userId}, Movie ID: {tag.movieId}, Tag: {tag.tag}")

db.close()

# %%
n_movie = get_movie_count(db)
print(f"Nombre de films: {n_movie}")

db.close()
# %%
n_rating = get_rating_count(db)
print(f"Nombre d'evaluations: {n_rating}")

db.close()
# %%
n_tag = get_tag_count(db)
print(f"Nombre de tags: {n_tag}")

db.close()
# %%
n_link = get_link_count(db)
print(f"Nombre de liens: {n_link}")

db.close()
# %%
