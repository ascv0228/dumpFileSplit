import os, sys
from mylib import *

ObjectName = "com.softstargames.shadow"
# 原始檔案位置
origFolder = "C:/Users/123/Documents/XuanZhi9/Pictures/dump2"
# origFolder = "C:/Users/123/Documents/XuanZhi9/Pictures/dumpOrg"

# 各檔案的所有分區 # 請依序
# Partition = {
#     "libil2cpp.so":["7ffe15b85000-7ffe20000000", "7fff35900000-7fff38a31000", 
#                     "7fff38a31000-7fff38a32000", "7fff38a32000-7fff3f2bf000", "7fff3f2ce000-7fff3fd8b000"],
#     "global-metadata.dat" : ["7ffe7ef00000-7ffe80000000"]
# }
Partition = createPartitionFromReadMapFile(origFolder, ObjectName, ["libil2cpp.so", "global-metadata.dat"])
print(Partition)

# 輸出資料夾
outputFolder = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "out", ObjectName)

# 原始檔案的排序
origFileNames = [_ for _ in os.listdir(origFolder) if _.endswith(".bin") and _.startswith(ObjectName)]
origFileNames.sort(key=lambda x: int(x.split("-")[1], 16))

# 尋找分區的檔案
def FilterDumperFile(name: str, byteRange_start, byteRange_end):
    try:
        if name.endswith(".bin") and name.startswith(ObjectName):
            FileRange = [int(_, 16) for _ in name[name.index('-')+1:name.index('.bin')].split('-')]
            if FileRange[0] <= byteRange_start and FileRange[1] >= byteRange_end:
                return True
        
    except:
        return False
    return False

# 創建資料夾
if not os.path.isdir(outputFolder):
    os.makedirs(outputFolder, mode=0o777)


for fname in Partition:
    output = bytearray() 
    for byteRange in Partition[fname]:
        byteRange_start, byteRange_end = [int(_, 16) for _ in byteRange.split('-')] # 分區轉數字
        targetFile = [ _ for _ in origFileNames if FilterDumperFile(_, byteRange_start, byteRange_end)] # 分區的檔案
        if len(targetFile) == 0:
            print(byteRange, "not in any file.")
            continue
        print(byteRange, "in", targetFile)

        for tf in targetFile:
            with open(os.path.join(origFolder, tf), 'rb') as f:
                fileRange_start = int(tf[tf.index('-')+1:tf.index('.bin')].split('-')[0], 16)
                data = f.read()[byteRange_start - fileRange_start: byteRange_end-fileRange_start]
                output.extend(bytearray(data))
            print(byteRange, "length of data:", len(data)) # 各分區的長度

    # 新建檔案與輸出
    with open(os.path.join(outputFolder, fname), 'wb') as outputFile:
        outputFile.write(output)
        print(fname, "length:", len(output), "\n")


