### Hexlet tests and linter status:
[![Actions Status](https://github.com/paalso/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/paalso/python-project-83/actions) 
[![lint](https://github.com/paalso/python-project-83/actions/workflows/lint.yml/badge.svg)](https://github.com/paalso/python-project-83/actions/workflows/lint.yml)

## Level 3 project on [Hexlet](https://ru.hexlet.io/), program [Python developer](https://ru.hexlet.io/programs/python).
### [Анализатор страниц (Page Analyzer)](https://ru.hexlet.io/programs/python/projects/83)

App link: [https://python-project-83-2v62.onrender.com](https://python-project-83-2v62.onrender.com)

### Project description

Page Analyzer is a lightweight SEO tool designed to assess web pages for key SEO elements. It enables users to check URLs, store them in a database, and analyze page content. While its functionality is minimalistic, the application provides essential insights by verifying page accessibility and extracting crucial metadata, including the first-level heading (`<h1>`), page title (`<title>`), and meta description (`<meta name="description">`). All analysis results are securely stored in the database for future reference.

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

#### Useful links
[render.com — Flask app deploy](https://render.com/docs/deploy-flask)

[render.com - Postgres](https://render.com/docs/postgresql-creating-connecting)

[render.com - my dashboard](https://dashboard.render.com/)

When deploying the application on [render.com](https://render.com/), encountered difficulties in the project insallation with `uv`. That's why deployment to render.com is done using these
##### Deployment settings:

Build Command: `pip install -r requirements.txt && psql -a -d $DATABASE_URL -f database.sql`

Start Command: `gunicorn page_analyzer:app`

