import typer
from cli.commands import analyze, data

app = typer.Typer()

app.command()(analyze.run_analysis)
app.command()(data.manage_data)

if __name__ == "__main__":
    app()