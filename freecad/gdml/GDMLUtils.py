def newTempFileName():
    import os,time
    formatstr='fc-%05d-%06d-%06d'
    count = 0
    while True:
        count+=1
        yield formatstr % (os.getpid(),int(time.time()*100) % 1000000,count)


def getTempFileName(filePath, outputExt):
    import os, tempfile

    keepName = False
    if os.path.isfile(filePath):
       dir1=tempfile.gettempdir()
       if keepName:
            outputfilename=os.path.join(dir1,'%s.%s' % (os.path.split(\
                    filePath)[1].rsplit('.',1)[0],outputExt))
       else:
           newFN = newTempFileName()
           print(f"Temp dir{dir1} file name {next(newFN)} {outputExt}")
           n = next(newFN)
           #outputfilename=os.path.join(dir1,'%s.%s' % next(newFN),outputExt)
           #outputfilename=os.path.join(dir1,'%s.%s' % n )
           #outputfilename=os.path.join(dir1, n + outputExt)
           outputfilename=os.path.join(dir1, next(newFN)  + outputExt)

       return outputfilename
