from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from src.catalog import TMDBError, fetch_catalog, get_recommendations

load_dotenv()

st.set_page_config(
    page_title="Layar — Temukan film berikutnya",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

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


def show_movie_card(movie: dict, rank: int | None = None) -> None:
    image = poster_url(movie.get("poster_path"))
    if image:
        st.image(image, width="stretch")
    else:
        st.markdown(
            '<div style="height:270px;border-radius:14px;background:linear-gradient(145deg,#25233c,#182c31);'
            'display:grid;place-items:center;font-size:3rem">🎞️</div>',
            unsafe_allow_html=True,
        )
    title = movie.get("title") or "Tanpa judul"
    heading = f"{rank:02d} · {title}" if rank else title
    st.markdown(f'<div class="movie-title">{heading}</div>', unsafe_allow_html=True)
    release = movie.get("release_date") or "Tanggal rilis belum tersedia"
    rating = movie.get("vote_average")
    rating_text = f"★ {rating:.1f}" if isinstance(rating, (float, int)) and rating else "Belum ada rating"
    st.markdown(f'<div class="movie-meta">{release} &nbsp; · &nbsp; {rating_text}</div>', unsafe_allow_html=True)
    genres = movie.get("genres", [])
    if genres:
        pills = "".join(f'<span class="pill">{genre}</span>' for genre in genres[:3])
        st.markdown(pills, unsafe_allow_html=True)
    overview = movie.get("overview") or "Sinopsis belum tersedia."
    with st.expander("Lihat sinopsis"):
        st.write(overview)


def main() -> None:
    st.sidebar.markdown("## 🎬 LAYAR")
    st.sidebar.caption("RUANG KECIL UNTUK PECINTA FILM")
    st.sidebar.markdown("---")
    api_key = os.getenv("TMDB_API_KEY", "").strip()
    if not api_key:
        st.error("Kunci API belum ditemukan. Tambahkan `TMDB_API_KEY` ke file `.env`, lalu jalankan ulang aplikasi.")
        st.code("TMDB_API_KEY=isi_api_key_tmdb_anda", language="text")
        st.stop()

    with st.spinner("Mengambil pilihan film terbaru..."):
        try:
            movies, genres = fetch_catalog(api_key)
        except TMDBError as exc:
            st.error(f"Tidak dapat memuat katalog TMDB: {exc}")
            st.info("Periksa koneksi internet dan kunci API di file `.env`, lalu coba muat ulang aplikasi.")
            st.stop()

    if not movies:
        st.warning("Belum ada film trending untuk ditampilkan. Coba lagi nanti.")
        st.stop()

    st.sidebar.markdown("### Sesuaikan pilihan")
    selected_genres = st.sidebar.multiselect("Genre", options=genres, placeholder="Semua genre")
    sort_by = st.sidebar.selectbox("Urutkan", ["Sedang populer", "Rating tertinggi", "Terbaru"])
    st.sidebar.markdown("---")
    st.sidebar.caption("Data film dan poster disediakan oleh TMDB.")

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Malam ini, pilih cerita baru</div>
            <h1>Film bagus.<br>Lebih mudah ditemukan.</h1>
            <p>Jelajahi film yang sedang ramai dibicarakan, lalu temukan tontonan serupa dari genre yang kamu suka.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    movie_df = pd.DataFrame(movies)
    visible = movie_df
    if selected_genres:
        visible = visible[visible["genres"].apply(lambda items: any(g in items for g in selected_genres))]
    if sort_by == "Rating tertinggi":
        visible = visible.sort_values("vote_average", ascending=False)
    elif sort_by == "Terbaru":
        visible = visible.sort_values("release_date", ascending=False)
    else:
        visible = visible.sort_values("popularity", ascending=False)

    average_rating = movie_df["vote_average"].replace(0, pd.NA).mean()
    metrics = st.columns(3)
    metrics[0].metric("Film trending", len(movie_df))
    metrics[1].metric("Pilihan genre", len(genres))
    metrics[2].metric("Rata-rata rating", f"{average_rating:.1f} / 10" if pd.notna(average_rating) else "—")

    st.markdown('<h2 class="section-title">Sedang ramai ditonton <span style="color:#72e5c2">✦</span></h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-subtitle">{len(visible)} film pilihan minggu ini, dikurasi untuk layar berikutnya.</p>', unsafe_allow_html=True)
    if visible.empty:
        st.info("Belum ada film dalam genre ini. Coba pilih genre lain.")
    else:
        for start in range(0, min(len(visible), 12), 4):
            row = visible.iloc[start : start + 4]
            columns = st.columns(4, gap="medium")
            for column, (_, movie) in zip(columns, row.iterrows()):
                with column:
                    show_movie_card(movie.to_dict())

    st.markdown('<h2 class="section-title">Cocok dengan seleramu <span style="color:#a78bfa">✧</span></h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Pilih satu film — kami carikan cerita dengan genre yang mirip.</p>', unsafe_allow_html=True)
    choices = {f"{movie['title']} · {movie['release_date'] or 'Tahun tidak tersedia'}": movie["id"] for movie in movies}
    selected_label = st.selectbox("Film yang kamu suka", list(choices), label_visibility="collapsed")
    recommendations = get_recommendations(movies, choices[selected_label], limit=4)
    if recommendations:
        for start in range(0, len(recommendations), 4):
            columns = st.columns(4, gap="medium")
            for index, (column, movie) in enumerate(zip(columns, recommendations[start : start + 4]), start=start + 1):
                with column:
                    show_movie_card(movie, index)
    else:
        st.info("Belum ada film serupa yang dapat ditampilkan.")

    st.markdown('<h2 class="section-title">Peta popularitas</h2>', unsafe_allow_html=True)
    chart_data = visible.head(10).sort_values("popularity", ascending=True)
    if not chart_data.empty:
        chart = px.bar(
            chart_data,
            x="popularity",
            y="title",
            orientation="h",
            color="vote_average",
            color_continuous_scale=["#6251a8", "#72e5c2"],
            labels={"popularity": "Popularitas", "title": "", "vote_average": "Rating"},
            template="plotly_dark",
        )
        chart.update_layout(
            height=max(300, len(chart_data) * 43),
            margin=dict(l=0, r=10, t=12, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(title="Rating"),
        )
        chart.update_traces(marker_line_width=0, hovertemplate="%{y}<br>Popularitas %{x:.1f}<extra></extra>")
        st.plotly_chart(chart, width="stretch")

    st.markdown(
        '<p style="text-align:center;color:#77758d;font-size:.78rem;margin:3rem 0 1rem">'
        'Dibuat untuk malam film yang lebih seru · Data dari TMDB</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
