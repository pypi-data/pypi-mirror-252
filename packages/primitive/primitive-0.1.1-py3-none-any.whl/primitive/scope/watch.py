""" Watch filesystem for changes and manage simulation data """
import click
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scope.simulator import Simulator

class Handler(FileSystemEventHandler):
	def __init__(self, ask):
		self.ask = ask
		self.simulator = Simulator()

	def on_any_event(self, event):
		if event.is_directory: return None

		if event.event_type == 'created' or event.event_type == 'modified' or event.event_type == 'deleted':
			# If we recognize a file has changed, prompt user to run simulation
			click.echo(f"File {event.src_path} has changed. ", nl=False)
			if self.ask:
				click.echo(f"Press enter to start simulation.")
				input()
			
			click.echo(f"Running simulation...")

class DirectoryWatch:
	def __init__(self, path, ask):
		self.path = path
		self.ask = ask
		self.observer = Observer()
	
	def run(self):
		event_handler = Handler(self.ask)
		self.observer.schedule(event_handler, self.path, recursive = True)
		self.observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			self.observer.stop()
			print("Observer Stopped")

		self.observer.join()