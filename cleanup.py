import os, time, shutil

smashdir = "C:\\smashdir\\"
days = 2


now = time.time()
lastdate = days * 86400


for f in os.listdir(smashdir):
    path = os.path.join(smashdir, f)
    if os.stat(path).st_mtime < now - lastdate:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            print "Clean up failed: Unrecognizable file: " + path
            exit(1)

exit(0)
