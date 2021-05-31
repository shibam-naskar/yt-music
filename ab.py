import os

mydir = "."
filelist = [ f for f in os.listdir(mydir) if f.endswith(".mp3") ]
for f in filelist:
    os.remove(os.path.join(mydir, f))