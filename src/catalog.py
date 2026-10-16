from __future__ import annotations

from typing import Any

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

TMDB_BASE_URL = "https://api.themoviedb.org/3"


class TMDBError(RuntimeError):
    """Raised when TMDB does not return a usable catalog response."""


def _get_json(endpoint: str, api_key: str) -> dict[str, Any]:
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/{endpoint}",
            params={"api_key": api_key},
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise TMDBError("Permintaan ke TMDB gagal.") from exc
    try:
        payload = response.json()
    except requests.JSONDecodeError as exc:
        raise TMDBError("TMDB mengirim respons yang tidak dapat dibaca.") from exc
    if not isinstance(payload, dict):
        raise TMDBError("Format respons TMDB tidak valid.")
    return payload


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_catalog(api_key: str) -> tuple[list[dict[str, Any]], list[str]]:
    genre_payload = _get_json("genre/movie/list", api_key)
    trending_payload = _get_json("trending/movie/week", api_key)
    genre_map = {
        genre["id"]: genre["name"]
        for genre in genre_payload.get("genres", [])
        if isinstance(genre, dict) and "id" in genre and "name" in genre
    }
    results = trending_payload.get("results", [])
    if not isinstance(results, list):
        raise TMDBError("Daftar film trending dari TMDB tidak valid.")

    movies = []
    for movie in results:
        if not isinstance(movie, dict):
            continue
        movie_genres = [genre_map[genre_id] for genre_id in movie.get("genre_ids", []) if genre_id in genre_map]
        movies.append(
            {
                "id": movie.get("id"),
                "title": movie.get("title") or "Tanpa judul",
                "overview": movie.get("overview") or "",
                "release_date": movie.get("release_date") or "",
                "popularity": float(movie.get("popularity") or 0),
                "vote_average": float(movie.get("vote_average") or 0),
                "poster_path": movie.get("poster_path"),
                "genres": movie_genres,
            }
        )
    return movies, sorted(genre_map.values())


def get_recommendations(
    movies: list[dict[str, Any]],
    selected_id: int,
    limit: int = 4,
) -> list[dict[str, Any]]:
    if len(movies) < 2:
        return []

    genre_lists = [movie.get("genres") or [] for movie in movies]
    if not any(genre_lists):
        return []

    vectorizer = TfidfVectorizer(
        tokenizer=lambda genres: genres,
        preprocessor=lambda genres: genres,
        token_pattern=None,
        lowercase=False,
    )
    matrix = vectorizer.fit_transform(genre_lists)
    similarities = cosine_similarity(matrix)
    selected_index = next((i for i, movie in enumerate(movies) if movie.get("id") == selected_id), None)
    if selected_index is None:
        return []

    ranked = sorted(
        (
            (index, score)
            for index, score in enumerate(similarities[selected_index])
            if index != selected_index
        ),
        key=lambda item: (item[1], movies[item[0]].get("popularity", 0)),
        reverse=True,
    )
    return [movies[index] for index, _ in ranked[:limit]]
