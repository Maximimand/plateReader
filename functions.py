import sys

def existingFile(plate, filepath):
    with open(filepath, "r+") as f:
        fContents = f.readlines()
        fContents.append(str(len(fContents)) + ". " + plate)
        for line in fContents:
            f.write(line )
        



sys.modules[__name__] = existingFile

def newFile(plate):
    gaming = 2
    with open("licensePlates.txt", "w") as w:
        w.write(plate)



sys.modules[__name__] = newFile

