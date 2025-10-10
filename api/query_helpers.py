""" SQLAlchemy Query Functions for MovieLens API"""
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import Optional

import models

# ---Films--- #
def get_movie(db: Session, movie_id: int):
    """ Recupere un film par son ID. """
    return db.query(models.Movie).filter(models.Movie.movieId == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 100, title: str = None, genre: str = None):
    """ Recupere une liste de films avec filtres optionnels. """
    query = db.query(models.Movie)
    
    if title:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(models.Movie.genres.ilike(f"%{genre}%"))
    return query.offset(skip).limit(limit).all()

# ---Evaluations--- #
def get_rating(db: Session, user_id: int, movie_id: int):
    """ Recupere une evaluation en fonction du couple (userId, movieId). """
    return db.query(models.Rating).filter(
        models.Rating.userId == user_id,
        models.Rating.movieId == movie_id
    ).first()

def get_ratings(db: Session, skip: int = 0, limit: int = 100, movie_id: int = None, user_id: int = None, min_rating: float = None):
    """ Recupere une liste d'evaluations avec filtres optionnels. """
    query = db.query(models.Rating)

    if movie_id:
        query = query.filter(models.Rating.movieId == movie_id)
    if user_id:
        query = query.filter(models.Rating.userId == user_id)
    if min_rating: # Filtre optionnel pour les evaluations minimales
        query = query.filter(models.Rating.rating >= min_rating) 

    return query.offset(skip).limit(limit).all()

# ---Tags--- #
def get_tag(db: Session, user_id: int, movie_id: int, tag_text: str):
    """ Recupere un tag par userId, movieId et le texte du tag. """
    return (
        db.query(models.Tag)
        .filter(
            models.Tag.userId == user_id,
            models.Tag.movieId == movie_id,
            models.Tag.tag == tag_text
        )
        .first()
    )

def get_tags(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        movie_id: Optional[int] = None,
        user_id: Optional[int] = None,
):
  """ Recupere une liste de tags avec filtres optionnels. """
  query = db.query(models.Tag)

  if movie_id is not None:
        query = query.filter(models.Tag.movieId == movie_id)
  if user_id is not None:
        query = query.filter(models.Tag.userId == user_id)
  return query.offset(skip).limit(limit).all()

# ---Liens--- #
def get_link(db: Session, movie_id: int):
    """ Recupere un lien IMDB et TMDB associe a un film specifique. """
    return db.query(models.Link).filter(models.Link.movieId == movie_id).first()

def get_links(db: Session, skip: int = 0, limit: int = 100):    
    """ Recupere une liste pagine de liens IMDB et TMBD de films. """
    return db.query(models.Link).offset(skip).limit(limit).all()

# ---Requetes analytiques--- #
def get_movie_count(db: Session):
    """ Recupere le nombre total de films. """
    return db.query(models.Movie).count()

def get_rating_count(db: Session):
    """ Recupere le nombre total d'evaluations. """
    return db.query(models.Rating).count()

def get_tag_count(db: Session):
    """ Recupere le nombre total de tags. """
    return db.query(models.Tag).count()

def get_link_count(db: Session):
    """ Recupere le nombre total de liens. """
    return db.query(models.Link).count()    
      
        