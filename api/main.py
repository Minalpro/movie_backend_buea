from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import query_helpers as helpers
import schemas


api_description = """
Bienvenue dans l'API MovieLens!
Cette API permet d"interagir avec une base de donnees inspiree du celebre jeu de donnees [MovieLens](htps://grouplens.org/datasets/movielens/.)
Elle est ideale pour decouvrir comment fonctionne une API REST avec des donnees de films d'utilisateur, d'evaluations, de tags et de liens externes (IMDB, TMDB).
### Fonctionnalites disponibles:
- Rechercher un film par son ID, ou lister tous les films
- Consulter les evaluations (ratings) par utilisateurs et/ou film
- Acceder aux tags appliques par les utilisateurs sur les films
- Obtenir les liens IMDB / TMDB pour un film
- Voir les statistiques globales sur la base

Tous les endpoints supportent la pagination ('skip', 'limit') et des filtres optionnels selon les cas.
### Bon a savoir:
- Vous pouvez tester tous les endpoints directement via l'interface Swagger "/docs".
- Pour toute erreur (ex: ID inexistant), une reponse claire est retournee avec le bon code HTTP.
"""


#---Initialisation de l'application FastAPI--- #
app = FastAPI(
    title = "MovieLens API",
    description = api_description,
    version = "0.1"
)

#---Dependance pour la session de base de donnees--- #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#---Endpoints pour tester la sante de l'API--- #
@app.get(
    "/",
    summary = "Verification de la sante de l'API",
    description = "Verifie que l'API fonctionne correctement",
    response_description = "Statut de l'API",
    operation_id = "health_check_movies_api",
    tags = ["monitoring"]
)
async def root():
    return{"message": "API MovieLens operationnelle"}

#---Endpoints pour obtenir  un film par son ID--- #
@app.get(
    "/movies/{movie_id}", # /movies/1
    summary = "Obtenir un film par son ID",
    description = "Retourne les informations d'un film en utilisant son 'movieId'.",
    response_description = "Details du film",
    response_model = schemas.MovieDetailed,
    tags = ["films"],
)
def read_movie(movie_id: int = Path(..., description="L'identifiant unique du film"), db: Session=Depends(get_db)):
    movie = helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Film avec l'ID {movie_id} non trouve")
    return movie


#---Endpoints pour obtenir une liste des films (avec pagination et filtres facultatifs title, genre, skip, limit )--- #
@app.get(
    "/movies",
    summary="Lister les fims",
    description="Retourne une liste de films avec pagination et filtres optionnels par titre ou genre.",
    response_description="Liste des films",
    response_model=List[schemas.MovieSimple],
    tags=["films"],
)
def list_movies(
    skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximal de resultats a retourner"),
    title: str = Query(None, description="Filtrer par titre"),
    genre: str = Query(None, description="Filtrer par genre"),
    db: Session = Depends(get_db)
):
    movies = helpers.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return movies

#---Endpoints pour obtenir une evaluation par utilisateur et film---#
@app.get(
    "/ratings/{user_id}/{movie_id}",
    summary="Obtenir une evaluation par utilisateur et film",
    description="Retourne l'evaluation d'un utilisateur pour un film donne",
    response_description="Details de l'evaluation",
    response_model=schemas.RatingSimple,
    tags=["evaluations"],
)
def read_rating(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    db: Session = Depends(get_db)
):
    rating = helpers.get_rating(db, user_id=user_id, movie_id=movie_id)
    if rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune evaluation trouvee pour l'utilisateur {user_id} et le film {movie_id}"
        )
    return rating

#---Endpoint pour obtenir une liste d'evaluation avec films--- #
@app.get(
    "/ratings",
    summary = "Lister les evaluations",
    description = "Retourne une liste d'evaluations avec pagination et filtres optionnels (film, utilisateur, note min)",
    response_description = "Liste des evaluations",
    response_model = List[schemas.RatingSimple],
    tags = ["evaluations"],
)
def list_ratings(
    skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de resultats a retrouver" ),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisation"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Filtrer les notes superieures ou egales a cette valeur"),
    db: Session = Depends(get_db),
):
    ratings = helpers.get_ratings(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id, min_rating=min_rating)
    return ratings

#---Endpoint pour retourner un tag pour un utilisateur et un film donnes avec le texte du tag--- #
@app.get(
    "/tags/{user_id}/{movie_id}/{tag_text}",
    summary="Obtenir un tag specifique",
    description = "Retourne un tag pour un utilisateur et un film donnes avec le texte du tag",
    response_model = schemas.TagSimple,
    tags = ["tags"],
)
def read_tag(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    tag_text: str = Path(..., description="Contenu exacte du tag"),
    db: Session = Depends(get_db)
):
    result = helpers.get_tag(db, user_id=user_id, movie_id=movie_id, tag_text=tag_text)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tag non trouve pour l'utilisateur {user_id}, et le film {movie_id} et le tag {tag_text} "
        )
    return result

#---Endpoint pour retourner une liste de tags avec pagination et filtres facultatifs par utilisateur ou film---#
@app.get(
    "/tags",
    summary = "Lister les tags",
    description = "Retourne une liste de tags avec pagination et filtres facultatifs par utilisateur et film",
    response_description = "Liste des tags",
    response_model = List[schemas.TagSimple],
    tags = ["tags"],
)
def list_tags(
    skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisateur"),
    db: Session = Depends(get_db),
):
    tags = helpers.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)
    return tags

#---Endpoint pour retourner les identifiants IMDB et TMDB pour un film donne---#
@app.get(
    "/links/{movie_id}",
    summary = "Obtenir le lien d'un film",
    description = "Retourne les identifiants IMDB et TMDB pour un film donne",
    response_model = schemas.LinkSimple,
    tags = ["links"],
)
def read_link(
    movie_id: int = Path(..., description="ID du film"),
    db: Session = Depends(get_db)
):
    result = helpers.get_link(db, movie_id=movie_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Aucun lien trouve pour le film {movie_id}")
    return result

#---Endpoint pour retourner une liste paginee des identifiants IMDB et TMDB---#
@app.get(
    "/links",
    summary = "Lister les liens des films",
    description = "Retourne une liste paginee des identifiants IMDB et TMDB de tous les films.",
    response_description = "Liste des liens des films",
    response_model = List[schemas.LinkSimple],
    tags = ["links"],
)
def list_links(
    skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
    db: Session = Depends(get_db)
):
    return helpers.get_links(db, skip=skip, limit=limit)

#---Endpoint pour obtenir des statisques sur la base de donnees---#
@app.get(
    "/analytics",
    summary = "Obtenir des statiaques",
    description = """
    Retourne un resume analytique de la base de donnees:
    - Nombre total de films
    - Nombre total d'evaluations
    - Nombre total de tags
    - Nombre de liens vers IMDB/TMDB
    """,   
    response_model = schemas.AnalyticsResponse,
    tags = ["analytics"]
)
def get_analytics(db: Session = Depends(get_db)):
    movie_count = helpers.get_movie_count(db)
    rating_count = helpers.get_rating_count(db)
    tag_count = helpers.get_tag_count(db)
    link_count = helpers.get_link_count(db)
    
    return schemas.AnalyticsResponse(
        movie_count=movie_count,
        rating_count=rating_count,
        tag_count=tag_count,
        link_count=link_count
    )

