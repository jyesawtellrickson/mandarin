# Technology

The codebase is primarily Python.

The web app framework used is Flask.

The database is SQL Alchemy.

Docs managed with Sphinx.

Bootstrap for css.

## Development

Use venv
```source venv/bin/activate```

Run the server with:
```python main.py```

Develop analytics with:
```jupyter lab```

Website located at
http://127.0.0.1:5000/song_list

### Working with DB

```python
from main import app
app.app_context().push()

from website import db

from website.models import Snippet, Translation, Stat
Snippet.query.limit(10).all()
```
