import typer
from pathlib import Path

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
    (project_path / "static").mkdir(parents=True, exist_ok=True)

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


if __name__ == "__main__":
    cli()
