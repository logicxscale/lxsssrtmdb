<div align="center">

# 🎬 LAYAR
### Find your next film. Discover a story worth staying in for.

A little space to explore trending films, browse by genre, and find recommendations
that match your taste — all in one polished Streamlit app.

**English** · [Bahasa Indonesia](README.id.md) &nbsp;•&nbsp; **TMDB Trending** &nbsp;•&nbsp; **Genre recommendations**

</div>

---

> Built with **Vibe Coding**: AI-assisted development guided by human direction, review, and iteration.

## ✨ About Layar

Layar brings you weekly trending films from **The Movie Database (TMDB)** and helps you:

- Explore films with posters, synopses, and ratings.
- Filter by genre and sort by popularity, rating, or release date.
- Find similar films using **TF-IDF** genre vectors and **cosine similarity**.
- Compare film popularity in an interactive chart.
- Switch the app and TMDB catalog between **English** and **Indonesian**.

> Film data and images are provided by [TMDB](https://www.themoviedb.org/).
> Layar is an independent project and is not affiliated with TMDB.

## 🎨 The experience

A dark, cinematic interface with violet and mint accents, poster cards, sidebar filters,
and an interactive popularity chart.

## 🚀 Get started

### 1. Prerequisites

- Windows 10/11
- Python **3.10 or newer**
- An active TMDB API key

Create or manage your API key through your [TMDB account settings](https://www.themoviedb.org/settings/api).

### 2. Get the project

If the project is already on your computer, open PowerShell in its folder. To clone the
repository, use the URL provided by your team:

```powershell
git clone <REPOSITORY-URL>
cd <PROJECT-FOLDER>
```

### 3. Create and activate the virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Your PowerShell prompt should now show `(.venv)`. If Windows blocks script execution,
allow activation for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

You can also run commands without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### 4. Install dependencies

With `.venv` activated:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Configure your API key

Create a local `.env` file from the template, then add your own key:

```powershell
Copy-Item .env.example .env
notepad .env
```

Your `.env` should contain:

```dotenv
TMDB_API_KEY=your_tmdb_api_key_here
```

Do **not** commit or share `.env`. It is excluded from Git by `.gitignore`. If a key has
ever been exposed publicly, revoke it and create a new one in TMDB.

### 6. Run the app

```powershell
python -m streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`. The app defaults
to **English**; use the language selector in the sidebar to switch to **Indonesia**.

## 🧭 Project structure

```text
.
├── app.py                         # Streamlit UI, language, filters, and charts
├── src/
│   ├── __init__.py
│   └── catalog.py                 # TMDB access and genre recommendations
├── .streamlit/
│   └── config.toml                # Streamlit theme and configuration
├── .env.example                   # Local configuration template (no active key)
├── .gitignore                     # Excludes .env, .venv, and caches
├── requirements.txt               # Application dependencies
├── README.md                      # English developer guide (default)
├── README.id.md                   # Indonesian developer guide
└── LXS-Simple-System-Recomendations-TMDB.ipynb
                                  # Original exploration notebook
```

Never add `.venv/`, `.env`, `__pycache__/`, or local secrets to the repository.

## ⚙️ How it works

1. The app reads `TMDB_API_KEY` from the environment or `.env`.
2. `src/catalog.py` fetches the movie genres and weekly trending titles from TMDB.
3. Responses are normalized and cached by Streamlit for one hour.
4. Genre lists are transformed with TF-IDF and compared using cosine similarity.
5. `app.py` presents the catalog, recommendations, filters, and charts in the selected language.

The language selection also sets TMDB's response language: `en-US` for English and `id-ID`
for Indonesian. Cached catalog data is separate for each API key and language. Use Streamlit's
**Rerun** control to refresh before the cache expires.

## 👩‍💻 Contributing

### Where to make changes

| To change... | Start here |
| --- | --- |
| Page layout, language, filters, or charts | `app.py` |
| TMDB endpoints, movie data, or catalog cache | `src/catalog.py` |
| Recommendation scoring | `get_recommendations()` in `src/catalog.py` |
| Global theme colors | `.streamlit/config.toml` and the CSS in `app.py` |
| Project dependencies | `requirements.txt` |

### Adding a dependency

Add new libraries, with a suitable version range, to `requirements.txt`, then install them
in your active environment:

```powershell
python -m pip install -r requirements.txt
```

Do not rely on packages installed only on your machine; other developers should be able to
recreate the environment from the manifest.

### Validate your changes

Run syntax and dependency checks:

```powershell
python -m compileall app.py src
python -m pip check
```

Then launch the app and verify that:

1. The page loads without exceptions.
2. English and Indonesian both work, including the hero header.
3. Genre filters and each sorting option behave as expected.
4. Recommendations never include the selected film.
5. Empty data and API errors are explained clearly.

Before opening a pull request, describe your changes and how you tested them, update the
dependency manifest if needed, and check that `.env` and other secrets are not staged.

## ♻️ Rebuild the environment

If the virtual environment is broken or needs a fresh install, recreate `.venv` and restore
the dependencies from the manifest:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `Remove-Item` command above targets **only this project's `.venv` folder**. It does not
delete project files or your local `.env`.

## 🩺 Troubleshooting

| Issue | What to check |
| --- | --- |
| API key not found | Make sure `.env` is in the project root and contains `TMDB_API_KEY=...`. |
| TMDB rejects the request | Check the API key, your internet connection, and your TMDB account. |
| A poster is missing | Some films do not have posters; check your internet connection as well. |
| A package cannot be imported | Activate the correct `.venv`, then run `python -m pip install -r requirements.txt`. |
| Streamlit is not found | Install dependencies, then run `python -m streamlit run app.py`. |
| The catalog or genres look unchanged | The catalog is cached for up to one hour; use **Rerun** or restart the app. |

## 📄 Licensing and attribution

Review TMDB's terms and licensing requirements before distributing this application.
Movie posters, metadata, and film details are provided by TMDB; this project does not
store or claim ownership of that content.

---

<div align="center">

Made for better movie nights. 🍿

</div>
