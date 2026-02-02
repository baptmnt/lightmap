# lightmap
weee weee baguette


# Backend

## Démarrer le développement

### PostgreSQL instance

Run : 
```bash
sudo docker run --name postgres -e POSTGRES_PASSWORD={pass} -e POSTGRES_USER={user} -e POSTGRES_DB=lightmap -p 5432:5432 -d --restart unless-stopped postgres
```

### Python

Créer un environnement virtuel dans `/back` :
```bash
py/python/python -m venv .venv && source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

### Remplir le .env

`DATABASE_URL=postgresql://{user}:{pass}@localhost:5432/lightmap`

### Migrations et données initiales

Pour créer les tables dans la DB, lancer :
```bash
alembic upgrade head
```

Puis initialiser les données avec :
```bash
py seed_data.py
```

### Lancer le serveur

```bash
py app.py
```

### Documentation

Aller vers la [documentation](http://localhost:5000/api/v1/docs) (une fois l'appli lancée)