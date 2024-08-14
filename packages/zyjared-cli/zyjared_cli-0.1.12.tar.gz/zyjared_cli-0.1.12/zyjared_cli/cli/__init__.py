from .app import app
from .clean import clean
from .config import config
from .push import push
from .version import app as app_version


__all__ = [
    'app',
]


app.add_typer(app_version, name='version')
