import os
def createPartitionFromReadMapFile(origFolder, ObjectName, parts):
    Partition = {}
    for i in parts: Partition[i] = []
    mapFile = os.path.join(origFolder, f"{ObjectName}-maps.txt")
    with open(mapFile, 'r') as readFile:
        lines = readFile.readlines()
        for line in lines:
            for part in parts:
                if part in line:
                    Partition[part].append(line.split(' ')[0])

    return Partition