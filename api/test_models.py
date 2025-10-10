# %%
from database import SessionLocal
from models import Movie, Rating, Tag, Link

db = SessionLocal()

# %%
# Test la recuperation de quelques films
movies = db.query(Movie).limit(10).all()


for movie in movies:
    print(f"ID: {movie.movieId}, Titre: {movie.title}, Genres: {movie.genres}")
else:
    print("No movies found.")

# %%
# Recuperer les films dont le genre est 'action'
action_movies = db.query(Movie).filter(Movie.genres.contains("Action")).limit(5).all()

for movie in action_movies:
    print(f"ID: {movie.movieId}, Titre: {movie.title}, Genres: {movie.genres}")
else:
    print("No action movies found.")

# %%
# Tester la recuperation de quelques evaluations (ratings)
ratings = db.query(Rating).limit(5).all()

for rating in ratings:
    print(f"UserID: {rating.userId}, MovieID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}")
else:
    print("No ratings found.")
# %%
# recuperer les films dont la note est superieur ou egale a 4.0
high_rated_movies = (
    db.query(Movie.title, Rating.rating)
    .join(Rating)
    .filter(Rating.rating >= 4.0)
    .limit(5)
    .all()

)

for title, rating in high_rated_movies:
    print(f"Titre: {title}, Rating: {rating}")
# %%
# tester la recuperation des tags associes aux films
tags = db.query(Tag).limit(5).all()

for tag in tags:
    print(f"UserID: {tag.userId}, MovieID: {tag.movieId}, Tag: {tag.tag}, Timestamp: {tag.timestamp}")

# %%
# Tester la classe link
links = db.query(Link).limit(5).all()

for link in links:
    print(f"MovieID: {link.movieId}, IMDB ID: {link.imdbId}, TMDB ID: {link.tmdbId}")
# %%
# Fermer la session
db.close()
# %%
