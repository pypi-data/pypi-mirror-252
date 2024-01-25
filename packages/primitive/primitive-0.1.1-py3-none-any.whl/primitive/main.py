import click
from scope import DirectoryWatch

@click.group()
def cli():
    pass

# Watch filesystem for changes
@cli.command()
@click.option('--path', default='.', help='Path to watch for changes.')
@click.option('--ask', default=False, help='Ask before running simulation.')
def watch(path, ask):
	click.echo(f"Watching {path} for changes")
	watcher = DirectoryWatch(path, ask)
	watcher.run()

if __name__ == '__main__':
    cli()