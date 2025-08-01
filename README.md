### Hexlet tests and linter status:
[![lint](https://github.com/paalso/python-project-83/actions/workflows/lint.yml/badge.svg)](https://github.com/paalso/python-project-83/actions/workflows/lint.yml)

## Level 3 project on [Hexlet](https://ru.hexlet.io/), program [Python developer](https://ru.hexlet.io/programs/python).
### [Анализатор страниц (Page Analyzer)](https://ru.hexlet.io/programs/python/projects/83)

App link: [https://paalso.pythonanywhere.com/](https://paalso.pythonanywhere.com/)

### Project description

Page Analyzer is a lightweight SEO tool designed to assess web pages for key SEO elements. It enables users to check URLs, store them in a database, and analyze page content. While its functionality is minimalistic, the application provides essential insights by verifying page accessibility and extracting crucial metadata, including the first-level heading (`<h1>`), page title (`<title>`), and meta description (`<meta name="description">`). All analysis results are securely stored in the database for future reference.

#### Note:
Currently, the project supports only PostgreSQL as the database. The database interaction logic relies on the psycopg2 library and PostgreSQL-specific SQL syntax, so support for other databases like SQLite is not implemented at this stage.

### Project setup

1. Clone the repository

```
git clone git@github.com:paalso/python-project-83.git
```

2. Install uv
```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install the project dependencies using `uv`
```
make install
```

4. Create .env file with required variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
SECRET_KEY=your-secret-key
```

5. Development / Production

Run the development server:
```
make dev
```
or run with `gunicorn`
```
make run
```
### Demo

#### [Railway](https://railway.com) version

Live demo deployed on Railway: 👉 [https://paalso.pythonanywhere.com/](https://python-project-83-production-cd6e.up.railway.app/)

Available until 27 August 2025

At the moment the app is configured to connect to a remote PostgreSQL database hosted on [Supabase](https://supabase.com).

#### [Render](render.com) version:

[https://python-project-83-2v62.onrender.com](https://python-project-83-2v62.onrender.com) - expired :unamused:

When deploying the application on [Render](https://render.com/), encountered difficulties in the project insallation with `uv`. That's why deployment to render.com is done using these

#### Deployment settings:

Build Command: `pip install -r requirements.txt && psql -a -d $DATABASE_URL -f database.sql`

Start Command: `gunicorn page_analyzer:app`

#### Useful links
[render.com — Flask app deploy](https://render.com/docs/deploy-flask)

[render.com - Postgres](https://render.com/docs/postgresql-creating-connecting)

[render.com - my dashboard](https://dashboard.render.com/)
