from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from src.catalog import TMDBError, fetch_catalog, get_recommendations

load_dotenv()

st.set_page_config(
    page_title="Layar — Discover your next film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGES = {
    "English": {
        "app_tagline": "A LITTLE SPACE FOR FILM LOVERS",
        "language": "Language",
        "filters": "Personalize your picks",
        "genre": "Genres",
        "all_genres": "All genres",
        "sort": "Sort by",
        "sort_popular": "Most popular",
        "sort_rating": "Top rated",
        "sort_newest": "Newest",
        "tmdb_credit": "Film data and posters provided by TMDB.",
        "missing_key": "API key not found. Add `TMDB_API_KEY` to your `.env` file, then restart the app.",
        "key_placeholder": "enter_your_tmdb_api_key",
        "loading": "Finding the latest picks...",
        "catalog_error": "Could not load the TMDB catalog.",
        "tmdb_request_error": "The request to TMDB failed.",
        "tmdb_response_error": "TMDB returned an unreadable response.",
        "tmdb_format_error": "TMDB returned data in an invalid format.",
        "connection_help": "Check your internet connection and `.env` API key, then try again.",
        "empty_catalog": "No trending films are available right now. Please try again later.",
        "hero_eyebrow": "Tonight, find a new story",
        "hero_title": "Great films.<br>Easier to find.",
        "hero_description": "Explore what's trending, then discover your next watch based on the genres you love.",
        "metric_movies": "Trending films",
        "metric_genres": "Genres to explore",
        "metric_rating": "Average rating",
        "trending_title": "Trending right now",
        "trending_subtitle": "{count} films making waves this week, picked for your next movie night.",
        "no_genre_movies": "No films match these genres. Try a different selection.",
        "no_release_date": "Release date unavailable",
        "not_rated": "Not rated yet",
        "no_overview": "No synopsis available.",
        "overview": "Read synopsis",
        "recommend_title": "Made for your taste",
        "recommend_subtitle": "Pick a film and we'll find stories with similar genres.",
        "choose_film": "Choose a film you like",
        "unknown_year": "Year unavailable",
        "no_recommendations": "There are no similar films to show yet.",
        "popularity_map": "Popularity map",
        "popularity": "Popularity",
        "rating": "Rating",
        "footer": "Made for better movie nights · Film data by TMDB",
    },
    "Indonesia": {
        "app_tagline": "RUANG KECIL UNTUK PECINTA FILM",
        "language": "Bahasa",
        "filters": "Sesuaikan pilihan",
        "genre": "Genre",
        "all_genres": "Semua genre",
        "sort": "Urutkan",
        "sort_popular": "Sedang populer",
        "sort_rating": "Rating tertinggi",
        "sort_newest": "Terbaru",
        "tmdb_credit": "Data film dan poster disediakan oleh TMDB.",
        "missing_key": "Kunci API belum ditemukan. Tambahkan `TMDB_API_KEY` ke file `.env`, lalu jalankan ulang aplikasi.",
        "key_placeholder": "isi_api_key_tmdb_anda",
        "loading": "Mengambil pilihan film terbaru...",
        "catalog_error": "Tidak dapat memuat katalog TMDB.",
        "tmdb_request_error": "Permintaan ke TMDB gagal.",
        "tmdb_response_error": "TMDB mengirim respons yang tidak dapat dibaca.",
        "tmdb_format_error": "Format respons TMDB tidak valid.",
        "connection_help": "Periksa koneksi internet dan kunci API di file `.env`, lalu coba muat ulang aplikasi.",
        "empty_catalog": "Belum ada film trending untuk ditampilkan. Coba lagi nanti.",
        "hero_eyebrow": "Malam ini, pilih cerita baru",
        "hero_title": "Film bagus.<br>Lebih mudah ditemukan.",
        "hero_description": "Jelajahi film yang sedang ramai dibicarakan, lalu temukan tontonan serupa dari genre yang kamu suka.",
        "metric_movies": "Film trending",
        "metric_genres": "Pilihan genre",
        "metric_rating": "Rata-rata rating",
        "trending_title": "Sedang ramai ditonton",
        "trending_subtitle": "{count} film pilihan minggu ini, dikurasi untuk layar berikutnya.",
        "no_genre_movies": "Belum ada film dalam genre ini. Coba pilih genre lain.",
        "no_release_date": "Tanggal rilis belum tersedia",
        "not_rated": "Belum ada rating",
        "no_overview": "Sinopsis belum tersedia.",
        "overview": "Lihat sinopsis",
        "recommend_title": "Cocok dengan seleramu",
        "recommend_subtitle": "Pilih satu film — kami carikan cerita dengan genre yang mirip.",
        "choose_film": "Film yang kamu suka",
        "unknown_year": "Tahun tidak tersedia",
        "no_recommendations": "Belum ada film serupa yang dapat ditampilkan.",
        "popularity_map": "Peta popularitas",
        "popularity": "Popularitas",
        "rating": "Rating",
        "footer": "Dibuat untuk malam film yang lebih seru · Data dari TMDB",
    },
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #f3f1ff;
        --muted: #aaa8c2;
        --panel: #17172a;
        --line: rgba(190, 178, 255, .13);
        --violet: #a78bfa;
        --mint: #72e5c2;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 80% 0%, rgba(100, 73, 180, .22), transparent 34%),
            radial-gradient(ellipse at 0% 30%, rgba(24, 135, 122, .11), transparent 32%),
            #0c0c17;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141424 0%, #10101c 100%);
        border-right: 1px solid var(--line);
    }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.035em; }
    .hero {
        padding: 2.1rem 2.3rem 2rem;
        margin: .6rem 0 1.7rem;
        border: 1px solid var(--line);
        border-radius: 26px;
        background: linear-gradient(115deg, rgba(31, 29, 54, .96), rgba(22, 37, 47, .84));
        box-shadow: 0 24px 80px rgba(0,0,0,.2);
        position: relative;
        overflow: hidden;
    }
    .hero:after {
        content: '✦';
        position: absolute;
        right: 7%; top: 8%;
        font-size: 8rem;
        color: rgba(167,139,250,.12);
    }
    .eyebrow {
        color: var(--mint);
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
    }
    .hero h1 { font-size: clamp(2.4rem, 5vw, 4.2rem); line-height: 1.03; margin: .7rem 0; }
    .hero p { max-width: 600px; color: #c4c1d7; font-size: 1.03rem; margin: 0; }
    .section-title { margin: 1.8rem 0 .2rem; }
    .section-subtitle { color: var(--muted); margin: 0 0 1rem; }
    .movie-title { font-family: 'Space Grotesk', sans-serif; font-weight: 600; margin: .6rem 0 .2rem; }
    .movie-meta { color: var(--muted); font-size: .83rem; }
    .pill {
        display: inline-block;
        margin: .35rem .25rem .15rem 0;
        padding: .25rem .62rem;
        border: 1px solid var(--line);
        border-radius: 999px;
        color: #d6d0ff;
        font-size: .72rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(23,23,42,.76);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }
    div[data-testid="stMetricLabel"] { color: var(--muted); }
    .stButton button, .stDownloadButton button {
        border-radius: 999px;
        border: 1px solid rgba(167,139,250,.38);
        background: rgba(167,139,250,.14);
        color: var(--ink);
    }
    .stButton button:hover { border-color: var(--mint); color: var(--mint); }
    section[data-testid="stSidebar"] .stCaption { color: var(--muted); }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


def poster_url(path: str | None) -> str | None:
    return f"https://image.tmdb.org/t/p/w500{path}" if path else None


def show_movie_card(movie: dict, text: dict[str, str], rank: int | None = None) -> None:
    image = poster_url(movie.get("poster_path"))
    if image:
        st.image(image, width="stretch")
    else:
        st.markdown(
            '<div style="height:270px;border-radius:14px;background:linear-gradient(145deg,#25233c,#182c31);'
            'display:grid;place-items:center;font-size:3rem">🎞️</div>',
            unsafe_allow_html=True,
        )
    title = movie.get("title") or "Untitled"
    heading = f"{rank:02d} · {title}" if rank else title
    st.markdown(f'<div class="movie-title">{heading}</div>', unsafe_allow_html=True)
    release = movie.get("release_date") or text["no_release_date"]
    rating = movie.get("vote_average")
    rating_text = f"★ {rating:.1f}" if isinstance(rating, (float, int)) and rating else text["not_rated"]
    st.markdown(f'<div class="movie-meta">{release} &nbsp; · &nbsp; {rating_text}</div>', unsafe_allow_html=True)
    genres = movie.get("genres", [])
    if genres:
        pills = "".join(f'<span class="pill">{genre}</span>' for genre in genres[:3])
        st.markdown(pills, unsafe_allow_html=True)
    overview = movie.get("overview") or text["no_overview"]
    with st.expander(text["overview"]):
        st.write(overview)


def main() -> None:
    language_name = st.session_state.get("language", "English")
    text = LANGUAGES[language_name]
    st.sidebar.markdown("## 🎬 LAYAR")
    st.sidebar.caption(text["app_tagline"])
    language_name = st.sidebar.selectbox(
        text["language"],
        options=list(LANGUAGES),
        key="language",
    )
    text = LANGUAGES[language_name]
    st.sidebar.markdown("---")
    api_key = os.getenv("TMDB_API_KEY", "").strip()
    if not api_key:
        st.error(text["missing_key"])
        st.code(f"TMDB_API_KEY={text['key_placeholder']}", language="text")
        st.stop()

    tmdb_language = "id-ID" if language_name == "Indonesia" else "en-US"
    with st.spinner(text["loading"]):
        try:
            movies, genres = fetch_catalog(api_key, language=tmdb_language)
        except TMDBError as exc:
            error_messages = {
                "Permintaan ke TMDB gagal.": text["tmdb_request_error"],
                "TMDB mengirim respons yang tidak dapat dibaca.": text["tmdb_response_error"],
                "Format respons TMDB tidak valid.": text["tmdb_format_error"],
                "Daftar film trending dari TMDB tidak valid.": text["tmdb_format_error"],
            }
            st.error(f"{text['catalog_error']} {error_messages.get(str(exc), str(exc))}")
            st.info(text["connection_help"])
            st.stop()

    if not movies:
        st.warning(text["empty_catalog"])
        st.stop()

    st.sidebar.markdown(f"### {text['filters']}")
    selected_genres = st.sidebar.multiselect(text["genre"], options=genres, placeholder=text["all_genres"])
    sort_by = st.sidebar.selectbox(
        text["sort"],
        [text["sort_popular"], text["sort_rating"], text["sort_newest"]],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(text["tmdb_credit"])

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{text["hero_eyebrow"]}</div>
            <h1>{text["hero_title"]}</h1>
            <p>{text["hero_description"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    movie_df = pd.DataFrame(movies)
    visible = movie_df
    if selected_genres:
        visible = visible[visible["genres"].apply(lambda items: any(g in items for g in selected_genres))]
    if sort_by == text["sort_rating"]:
        visible = visible.sort_values("vote_average", ascending=False)
    elif sort_by == text["sort_newest"]:
        visible = visible.sort_values("release_date", ascending=False)
    else:
        visible = visible.sort_values("popularity", ascending=False)

    average_rating = movie_df["vote_average"].replace(0, pd.NA).mean()
    metrics = st.columns(3)
    metrics[0].metric(text["metric_movies"], len(movie_df))
    metrics[1].metric(text["metric_genres"], len(genres))
    metrics[2].metric(text["metric_rating"], f"{average_rating:.1f} / 10" if pd.notna(average_rating) else "—")

    st.markdown(f'<h2 class="section-title">{text["trending_title"]} <span style="color:#72e5c2">✦</span></h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-subtitle">{text["trending_subtitle"].format(count=len(visible))}</p>', unsafe_allow_html=True)
    if visible.empty:
        st.info(text["no_genre_movies"])
    else:
        for start in range(0, min(len(visible), 12), 4):
            row = visible.iloc[start : start + 4]
            columns = st.columns(4, gap="medium")
            for column, (_, movie) in zip(columns, row.iterrows()):
                with column:
                    show_movie_card(movie.to_dict(), text)

    st.markdown(f'<h2 class="section-title">{text["recommend_title"]} <span style="color:#a78bfa">✧</span></h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-subtitle">{text["recommend_subtitle"]}</p>', unsafe_allow_html=True)
    choices = {
        f"{movie['title']} · {movie['release_date'] or text['unknown_year']}": movie["id"]
        for movie in movies
    }
    selected_label = st.selectbox(text["choose_film"], list(choices), label_visibility="collapsed")
    recommendations = get_recommendations(movies, choices[selected_label], limit=4)
    if recommendations:
        for start in range(0, len(recommendations), 4):
            columns = st.columns(4, gap="medium")
            for index, (column, movie) in enumerate(zip(columns, recommendations[start : start + 4]), start=start + 1):
                with column:
                    show_movie_card(movie, text, index)
    else:
        st.info(text["no_recommendations"])

    st.markdown(f'<h2 class="section-title">{text["popularity_map"]}</h2>', unsafe_allow_html=True)
    chart_data = visible.head(10).sort_values("popularity", ascending=True)
    if not chart_data.empty:
        chart = px.bar(
            chart_data,
            x="popularity",
            y="title",
            orientation="h",
            color="vote_average",
            color_continuous_scale=["#6251a8", "#72e5c2"],
            labels={"popularity": text["popularity"], "title": "", "vote_average": text["rating"]},
            template="plotly_dark",
        )
        chart.update_layout(
            height=max(300, len(chart_data) * 43),
            margin=dict(l=0, r=10, t=12, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(title=text["rating"]),
        )
        chart.update_traces(
            marker_line_width=0,
            hovertemplate=f"%{{y}}<br>{text['popularity']} %{{x:.1f}}<extra></extra>",
        )
        st.plotly_chart(chart, width="stretch")

    st.markdown(
        '<p style="text-align:center;color:#77758d;font-size:.78rem;margin:3rem 0 1rem">'
        f'{text["footer"]}</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
