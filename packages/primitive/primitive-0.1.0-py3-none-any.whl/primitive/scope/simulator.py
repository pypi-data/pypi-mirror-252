""" Run simulation to generate a new vcd file. """
import subprocess

class Simulator:

	def __init__(self):
		pass

	def run(self):
		subprocess.run(["iverilog", "-o", "test", "test.v"])
		subprocess.run(["vvp", "test"])
	