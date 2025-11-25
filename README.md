# restapi-flask

Backend-only Flask implementation for authentication endpoints.

Structure mirrors `project-A`'s Login module but using Flask blueprints.

Endpoints (prefix `/auth`):
- `POST /auth/login` -> {"username": "..", "password": ".."}
- `POST /auth/register` -> {"id": int, "username": "..", "phone": .., "email": "..", "password": ".."}
- `GET /auth/get_user/<id>`
- `POST /auth/updateP` -> {"id": int, "username": "..", "phone": .., "email": "..", "password": ".."}

DB connection: `Modulos/db.py` uses `mysql-connector-python` and expects a MySQL DB named `project` as in `project-A`.

Run:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
