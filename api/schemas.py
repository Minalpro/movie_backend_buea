from pydantic import BaseModel
from typing import Optional, List

# ---Schemas secondaires--- #

class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True

class LinkBase(BaseModel):
    imdbId: Optional[str]
    tmdbId: Optional[str]

    class Config:
        orm_mode = True

# ---Schema principal pour Movie--- #
class MovieBase(BaseModel):
    movieId: int
    title: str
    genres: Optional[str] = None

    class Config:
        orm_mode = True

class MovieDetailed(MovieBase):
    ratings: List[RatingBase] = []
    tags: List[TagBase] = []
    link: Optional[LinkBase] = None

    class Config:
        orm_mode = True

# ---Schemas pour liste de films (sans details imbriques)--- #
class MovieSimple(MovieBase):
    movieId: int
    title: str
    genres: Optional[str] = None

    class Config:
        orm_mode = True

# ---Pour les endpoints de /ratings et /tags si appeles seuls--- #
class RatingSimple(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    class Config:
        orm_mode = True
    
class TagSimple(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class Config:
        orm_mode = True
    
class LinkSimple (BaseModel):
    movieId: int
    imdbId: Optional[str]
    tmdbId: Optional[str]

    class Config:
        orm_mode = True

class AnalyticsResponse(BaseModel):
    movie_count: int
    rating_count: int
    tag_count: int
    link_count: int

    class Config:
        orm_mode = True
