moduleNames = ['sys', 'os', 're', 'unittest'] 
m = map(__import__, moduleNames)
print(sys.path)