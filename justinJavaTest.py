import subprocess
import os


process = subprocess.Popen(['java', '-jar', 'javb/textProcessor.jar'],
	stdout=subprocess.PIPE)
args = process.stdout.read().decode('utf-8').split()

print("Category:", args[0])
print("Rating:", args[1])
print("Mexico Mentions:", args[2])
print("China Mentions:", args[3])