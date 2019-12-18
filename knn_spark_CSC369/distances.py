# Markelle Kelly
# mkelly23@calpoly.edu
import pyspark
from pyspark.sql.types import *
from pyspark.sql.functions import *
import math

def distance(x):
  colnames = ['fixed-acidity', 'volatile-acidity','citric-acid','residual-sugar',
  'chlorides','free-sulfur-dioxide','total-sulfur-dioxide','density', 
  'pH','sulphates', 'alcohol']
  dist=0
  for col in colnames:
    a=col+"1"
    b=col+"2"
    dist = dist + ((x[a] - x[b])*(x[a] - x[b]))
  dist = math.pow(dist,0.5)
  return (x["id1"],x["id2"],dist)

def standardize(x):
  colnames = ['fixed-acidity', 'volatile-acidity','citric-acid','residual-sugar',
  'chlorides','free-sulfur-dioxide','total-sulfur-dioxide','density', 
  'pH','sulphates', 'alcohol']
  result = []
  for col in colnames:
    a=col+"1"
    mean = "mean-"+col
    std = "std-"+col
    res1 = (x[a] - x[mean])/x[std]
    result.append(res1)
  result.append(x["quality1"])
  return result

def standardize2(x):
  colnames = ['fixed-acidity', 'volatile-acidity','citric-acid','residual-sugar',
  'chlorides','free-sulfur-dioxide','total-sulfur-dioxide','density', 
  'pH','sulphates', 'alcohol']
  result = []
  for col in colnames:
    a=col+"2"
    mean = "mean-"+col
    std = "std-"+col
    res2 = (x[a] - x[mean])/x[std]
    result.append(res2)
  result.append(x["quality"])
  return result

def toCSVLine(data):
  return ','.join(str(d) for d in data)

schema1 = StructType([
  StructField('fixed-acidity1', FloatType(), True),
  StructField('volatile-acidity1', FloatType(), True),
  StructField('citric-acid1', FloatType(), True),
  StructField('residual-sugar1', FloatType(), True),
  StructField('chlorides1', FloatType(), True),
  StructField('free-sulfur-dioxide1', FloatType(), True),
  StructField('total-sulfur-dioxide1', FloatType(), True),
  StructField('density1', FloatType(), True),
  StructField('pH1', FloatType(), True),
  StructField('sulphates1', FloatType(), True),
  StructField('alcohol1', FloatType(), True),
  StructField('quality1', FloatType(), False)])
schema2 = StructType([
  StructField('fixed-acidity2', FloatType(), True),
  StructField('volatile-acidity2', FloatType(), True),
  StructField('citric-acid2', FloatType(), True),
  StructField('residual-sugar2', FloatType(), True),
  StructField('chlorides2', FloatType(), True),
  StructField('free-sulfur-dioxide2', FloatType(), True),
  StructField('total-sulfur-dioxide2', FloatType(), True),
  StructField('density2', FloatType(), True),
  StructField('pH2', FloatType(), True),
  StructField('sulphates2', FloatType(), True),
  StructField('alcohol2', FloatType(), True),
  StructField('quality', FloatType(), False)])
sc = pyspark.SparkContext().getOrCreate()
spark = pyspark.sql.SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

wine1a = spark.read.csv("/data/winequality-red-fixed.csv",schema1,header=True)
meanstd = wine1a.agg(mean('fixed-acidity1').alias("mean-fixed-acidity"), 
  mean('volatile-acidity1').alias("mean-volatile-acidity"),
  mean('citric-acid1').alias("mean-citric-acid"),
  mean('residual-sugar1').alias("mean-residual-sugar"),
  mean('chlorides1').alias("mean-chlorides"),
  mean('free-sulfur-dioxide1').alias("mean-free-sulfur-dioxide"),
  mean('total-sulfur-dioxide1').alias("mean-total-sulfur-dioxide"),
  mean('density1').alias("mean-density"),
  mean("pH1").alias("mean-pH"), 
  mean('sulphates1').alias("mean-sulphates"),
  mean('alcohol1').alias("mean-alcohol"),
  stddev('fixed-acidity1').alias("std-fixed-acidity"), 
  stddev('volatile-acidity1').alias("std-volatile-acidity"),
  stddev('citric-acid1').alias("std-citric-acid"),
  stddev('residual-sugar1').alias("std-residual-sugar"),
  stddev('chlorides1').alias("std-chlorides"),
  stddev('free-sulfur-dioxide1').alias("std-free-sulfur-dioxide"),
  stddev('total-sulfur-dioxide1').alias("std-total-sulfur-dioxide"),
  stddev('density1').alias("std-density"),
  stddev("pH1").alias("std-pH"), 
  stddev('sulphates1').alias("std-sulphates"),
  stddev('alcohol1').alias("std-alcohol")
)
wine1b= wine1a.crossJoin(meanstd).rdd.map(standardize).toDF(schema1)
wine1 = wine1b.withColumn("id1", monotonically_increasing_id()).withColumn("distance",lit(0))
wine2a = spark.read.csv("/data/winequality-red-fixed.csv",schema2,header=True)
wine2b = wine2a.crossJoin(meanstd).rdd.map(standardize2).toDF(schema2)
wine2 = wine2b.withColumn("id2", monotonically_increasing_id())
rows1 = wine1.join(wine2, wine1.id1 < wine2.id2)
rows=rows1.rdd.map(distance).toDF()

#lines = rows.map(toCSVLine)
rows.write.csv('distances.csv')


