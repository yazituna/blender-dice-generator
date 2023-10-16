import os
from os import listdir
from os.path import isfile, join

for k in range(6):
    mypath = 'D:/projects/blender/setup-production-01/rendered-' + str(i+1) + '-cropped/' 
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    lenfile = len(onlyfiles)

    print(lenfile)
    print(onlyfiles[3])
    for i in range(lenfile):
        oldname = onlyfiles[i]
        # i+101, i+201 etc.
        newname = "{:06d}".format(i+301) + oldname
        print(newname)
        os.rename(mypath + oldname, mypath + newname)
