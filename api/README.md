# MovieLens API

Bienvenu dans l'API **MovieLens** une API RESTful developpee avec **FASTAPI** pour explorer la base de donnees MovieLens. Elle vous permet d'interroger des informations sur les films, les evaluations, les utilisateurs, les tags et les liens vers des bases de donnees externes (IMDB, TMDB).

## Fonctionnalites principales

- Rechercher des films par titre, genre, ou ID
- Consultation des evaluations par utilisateurs et par film
- Gestion des tags associes aux films
- Recuperation des identifiants IMDB/TMDB
- Statistiques globales de la base

---

## Prerequis

- Python >= 3.12
- Un client HTTP comme `httpx` ou `requests`

Installation rapide de `httpx`:

```PowerShell
pip install httpx
```

---

## Demarrer avec l'API

L'API est accessible a l'adresse suivante:

```
http://localhost:8000
```

L'interface Swagger est disponible ici:

```
http://localhost:8000/docs
```

---

## Endpoints essentiels

|Methodes | URL                                | Description |
|---------|------------------------------------|-------------|
| GET     | `/`                                | Verifie le bon fonctionnement de l'API |
| GET     | `/movies`                          | Liste paginee des films avec filtres |
| GET     | `/movies/{movie_id}`               | Detail d'un film |
| GET     | `/ratings`                         | Liste paginee des evaluations |
| GET     | `/ratings/{user_id}/{movie_id}`    | Evaluation d'un film par un utilisateur|
| GET     | `tags`                             | Liste des tags |
| GET     | `tags/{user_id}/{movie_id}/{tag}`  | Detail d'un tag |
| GET     | `/links`                           | Liste des identifiants IMDB/TMDB |
| GET     | `/links/{movie_id}`                | Identifiants pour un film donne |
| GET     | `/analytics`                       | Statistiques de la base |
 
---

## Exemple d'utilisation avec `httpx`

### Lister les films

```python
import httpx

response = httpx.get("http://localhost:8000/movies", params={"limit": 5})
print(response.json())
```

### Obtenir un film specifique

```python
movie_id = 1
response = httpx.get(f"http://localhost:8000/movie/{movie_id}")
print(response.json())
```

### Rechercher les evaluations pour un film donne

```python
response = httpx.get(f"http://localhost:8000/ratings", params={"movie_id": 1})
print(response.json())
```

### Recuperer un tag specifique

```python
response = httpx.get(f"http://localhost:8000/tags/5/1/superbe")
print(response.json())
```

### Obtenir des statistiques globales

```python
response = httpx.get(f"http://localhost:8000/analytics")
print(response.json())
```

---

## Conditions d'utilisation

- Cette API est concue a des fins pedagogiques et experimentales.
- Merci de ne pas effectuer d'appels massifs sans controle et frequence (rate-limiting non implemente pour l'instant).
- Vous pouvez l'integrer a des notebooks ou projets de dataviz pour visualiser les donnees de MovieLens.

---

## Contribuer

Les contributions sont les bienvenus !

- Corriger des bugs
- Ameliorer les performances des requetes
- Ajouter de nouveaux endpoints
- Rendre l"API disponible sur un hebergeur public

---

## Ressources utiles

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentation technique: disponible via Swagger
- Base de donnees MovieLens: [http://grouplens.org/datasets/movielens/](http://grouplens.org/datasets/movielens/)

---

## Software Development Kit (SDK)

*A venir*

----

## URL publique (cloud) de l'API

*A venir*

## Auteur

developpe par [Alphonse Minoue](https://linkedin.com/in/minouealphonse/) en FastAPI.

---

## Licence

Ce projet est sous licence MIT.
