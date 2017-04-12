import subprocess


process = subprocess.Popen(['java', '-jar', 'java/textProcessor.jar'],
	stdout=subprocess.PIPE)
args = process.stdout.read().decode('utf-8').split()

print("Category:", args[0])
print("Rating:", args[1])
print("Mexico Mentions", args[2])
print("China Mentions", args[3])