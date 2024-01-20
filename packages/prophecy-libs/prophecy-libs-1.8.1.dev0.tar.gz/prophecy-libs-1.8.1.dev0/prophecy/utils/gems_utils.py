
def concatenateFiles(spark, format, mode, inputDir, outputFileName, deleteTempPath=True, fileFormatHasHeaders=True):
    jvm = spark.sparkContext._jvm
    jvm.io.prophecy.gems.datasetSpec.concatenateFiles(spark, format, mode, inputDir, outputFileName, deleteTempPath, fileFormatHasHeaders)

