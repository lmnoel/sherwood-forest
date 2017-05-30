import subprocess


process = subprocess.Popen(['java', '-jar', 'NHTextProcessor.jar'],
	stdout=subprocess.PIPE)
rating = process.stdout.read().decode('utf-8').split()

print(rating)