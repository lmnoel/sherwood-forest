import subprocess

process = subprocess.Popen(['java', '-jar', 'EOTextProcessor.jar'],
    	stdout=subprocess.PIPE)
args = process.stdout.read().decode('utf-8').split()


i = 0
'''
for something in rating:
    print(something) # this is good
    i = i+1 #thanks

'''

print ("Category",args[0])
print ("Rating",args[1])
print ("Mexico Count",args[2])
print ("China Count",args[3])
