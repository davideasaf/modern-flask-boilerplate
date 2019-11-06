"tasks to be invoked via Invoke python"
import os
from invoke import task


def get_db_url(ctx) -> str:
    """Get db url with local heroku setup

    Args:
        ctx (Context): Invoke context

    Returns:
        str: connection string for db
    """
    return ctx.run(
        "heroku config:get DATABASE_URL -a pydata-effortless-rest-flask"
    ).stdout.strip()


@task
def start(ctx, wsgi_server=False, config_name="dev", host="127.0.0.1"):
    """Start the backend as a dev server or production ready gunicorn server"""
    if wsgi_server:
        ctx.run(
            f"""gunicorn --bind {host}:5000 --workers 2 "app:create_app('{config_name}')" """,
            pty=True,
            echo=True,
        )
        return

    ctx.run(
        f"""
        export DATABASE_URL={get_db_url(ctx)} &&
        export FLASK_ENV=development &&
        export FLASK_APP="app:create_app('{config_name}')" &&
        flask run --host={host}
        """,
        pty=True,
        echo=True,
    )


@task
def save_dependencies(ctx):
    """Dump dependencies as config files"""
    ctx.run(
        "pip freeze > requirements.txt && conda env export > environment.yml",
        pty=True,
        echo=True,
    )


@task
def init_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app

    os.environ["DATABASE_URL"] = get_db_url(ctx)

    app = create_app(config_name)
    db.drop_all(app=app)
    db.create_all(app=app)


@task
def seed_db(ctx, config_name="dev"):
    """Initialize Database"""
    from app import db, create_app, guard
    from app.models import User

    os.environ["DATABASE_URL"] = get_db_url(ctx)
    app = create_app(config_name)

    with app.app_context():
        db.session.add(
            User(
                username="admin",
                password=guard.hash_password("password"),
                roles="admin",
            )
        )
        db.session.add(User(username="user", password=guard.hash_password("pass")))
        db.session.commit()


@task
def postman_dump(ctx, config_name="dev", output_path=None):
    from flask import json
    from app import create_app, api

    app = create_app(config_name)

    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = None

    with app.app_context():
        app.config["SERVER_NAME"] = "flask:5000"
        data = api.as_postman(urlvars=urlvars, swagger=swagger)

    if output_path:
        with open(output_path, "w") as new_file:
            new_file.write(json.dumps(data))
            return

    print(json.dumps(data))
