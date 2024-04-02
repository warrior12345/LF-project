import chardet

with open("Testing_ANSI.dat","rb") as f:
    data = f.read(500)

detection = chardet.detect(data)

enc1 = detection['encoding']

print(enc1)
