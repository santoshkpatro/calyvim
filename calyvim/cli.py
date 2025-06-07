import typer
from pathlib import Path
from datetime import datetime
from calyvim.conf import settings
import sqlite3
import sys

cli = typer.Typer()


@cli.command()
def new(name: str = typer.Argument(None)):
    """Create a new Calyvim app (in current dir if no name given)"""
    project_path = Path(name) if name else Path(".")

    if name and project_path.exists():
        typer.echo("🚫 Project already exists.")
        raise typer.Exit(1)

    # Create folders
    (project_path / "app" / "controllers").mkdir(parents=True, exist_ok=True)
    (project_path / "app" / "views" / "home").mkdir(parents=True, exist_ok=True)
    (project_path / "config" / "db").mkdir(parents=True, exist_ok=True)
    (project_path / "public").mkdir(parents=True, exist_ok=True)

    # urls.py
    (project_path / "urls.py").write_text(
        "from calyvim.router import Router\n\n"
        "router = Router()\n"
        "router.get('/', to='home#index')\n"
    )

    # core.py (default config)
    (project_path / "core.py").write_text(
        "from calyvim.app import Calyvim\n\n" "app = Calyvim()\n"
    )

    # HomeController
    home_controller_code = (
        "from calyvim.controller import CalyController\n\n"
        "class HomeController(CalyController):\n"
        "    async def index(self, request):\n"
        "        self.assign('message', 'Welcome to Calyvim!')\n"
        "        # return None to trigger default view rendering\n"
    )
    (project_path / "app" / "controllers" / "home_controller.py").write_text(
        home_controller_code
    )

    # View: home/index.html
    index_html = (
        "<h1>{{ message }}</h1>\n" "<p>This is the homepage rendered by Calyvim.</p>\n"
    )
    (project_path / "app" / "views" / "home" / "index.html").write_text(index_html)

    typer.echo(f"✅ Created Calyvim project at: {project_path.resolve()}")
    typer.echo("🚀 Run it with: uvicorn core:app --reload")


@cli.command()
def generate(type: str, name: str):
    """Generate controller or other component"""
    if type == "controller":
        path = Path("app/controllers") / f"{name}_controller.py"
        class_name = name.capitalize()
        stub = (
            "from calyvim.controller import CalyController\n\n"
            f"class {class_name}Controller(CalyController):\n"
            "    async def index(self, request):\n"
            f"        self.assign('message', '{class_name} index')\n"
        )
        path.write_text(stub)
        typer.echo(f"✅ Created controller: {path}")
    else:
        typer.echo("❌ Unknown type. Try: controller")


@cli.command()
def create_migration(name: str):
    """Create a new SQL migration file in config/db/migrations/"""
    migrations_path = Path("config/db/migrations")
    migrations_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{name}.sql"
    filepath = migrations_path / filename

    filepath.write_text("-- Write your SQL migration here\n")
    typer.echo(f"✅ Created migration: {filepath}")


@cli.command()
def setup_database():
    """Ensure schema_migrations table exists in the database"""
    sys.path.insert(0, str(Path().resolve()))  # Make local modules importable

    settings.configure("config.settings")  # Lazy load config module

    # Access DATABASE from settings safely
    db_settings = getattr(settings, "DATABASE")
    db_path = db_settings.get("NAME", "db.sqlite3")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version BIGINT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()

    typer.echo(f"✅ Ensured schema_migrations table exists in {db_path}")


@cli.command()
def migrate():
    """Apply pending migrations from config/db/migrations"""
    settings.configure("config.settings")

    db_settings = getattr(settings, "DATABASE")
    db_path = db_settings.get("NAME", "db.sqlite3")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Ensure schema_migrations table exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version BIGINT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Get already applied versions
    cursor.execute("SELECT version FROM schema_migrations")
    applied_versions = {row[0] for row in cursor.fetchall()}

    # Read migration files
    migrations_dir = settings.BASE_DIR / "config" / "db" / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    for file in migration_files:
        filename = file.name
        try:
            version_str = filename.split("_")[0]
            version = int(version_str)
        except (IndexError, ValueError):
            typer.echo(f"⚠️ Skipping invalid filename: {filename}")
            continue

        if version in applied_versions:
            continue

        sql = file.read_text()
        try:
            cursor.executescript(sql)
            cursor.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)", (version,)
            )
            conn.commit()
            typer.echo(f"✅ Applied {filename}")
        except Exception as e:
            conn.rollback()
            typer.echo(f"❌ Failed to apply {filename}: {e}")
            break

    conn.close()


if __name__ == "__main__":
    cli()
