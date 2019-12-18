# CSC 369 - Lab 08
# Markelle Kelly
# mkelly23@calpoly.edu

from pyspark.sql.types import *
def main():
	import pyspark
	import pyspark.sql.functions as F
	from pyspark.sql.window import Window
	import sys
	spark = pyspark.sql.SparkSession.builder.getOrCreate()
	# only print errors, no info lines
	spark.sparkContext.setLogLevel("OFF")

	try:
		k = sys.argv[1]
		distancesFilePath = sys.argv[2]
	except:
		print("Must have k and distances path as a command line argument")
		sys.exit(0)

	wineFilePath = "/data/winequality-red-fixed.csv"

	distancesSchema = StructType([
		StructField("id",IntegerType(),True),
		StructField("id2",IntegerType(),True),
		StructField("distance",FloatType(),True),
	])

	wineSchema = StructType([
        StructField("fixedAcidity", FloatType(), True),
        StructField("volatileAcidity", FloatType(), True),
        StructField("citricAcid", FloatType(), True),
        StructField("residualSugar", FloatType(), True),
        StructField("chlorides", FloatType(), True),
        StructField("freeSulfurDioxide", FloatType(), True),
        StructField("totalSulfurDioxide", FloatType(), True),
        StructField("density", FloatType(), True),
        StructField("pH", FloatType(), True),
        StructField("sulphates", FloatType(), True),
        StructField("alcohol", FloatType(), True),
        StructField("quality", FloatType(), True)
    ])

	distances = spark.read.csv(
		distancesFilePath,
		distancesSchema
	)

	wine = spark.read.csv(
	    wineFilePath,
	    wineSchema,
	    header='true'
	).withColumn("id", F.monotonically_increasing_id())

	broadcastK = spark.sparkContext.broadcast(k)

	wine = wine.select("id","quality")

	distancesRDD = distances.rdd.flatMap(lambda x: [((x['id'],x['id2']), x['distance']), ((x['id2'],x['id']), x['distance'])])
	wineRDD = wine.rdd.map(lambda x: (x[0],x[1]))
	wineRDDWithIds = wineRDD.cartesian(wineRDD)\
		.filter(lambda x: x[0][0]!=x[1][0]) \
		.map(lambda x: ((x[0][0],x[1][0]),(x[0][1],x[1][1])))\
		.join(distancesRDD)\
		.map(lambda x: ((x[0][0], x[1][0][0]), (x[0][1], x[1][0][1], x[1][1])))
	#wineRDDWithIds: ((id, trueQual), (neighborId, neighborQual, distance))

	topKById = wineRDDWithIds.groupByKey()\
		.map(lambda x: (
			x[0], 
			sorted(list(x[1]),
				key=(lambda x: (x[2], x[0]))
			)[0:5]
			))
	#topKById: ((id, trueQual), [(neighborId, neighborQual, distance), ... k of these])

	def getQual(x):
		qualCounts = {}
		for data in x[1]:
			nQual = data[1]
			if nQual in qualCounts:
				qualCounts[nQual] = qualCounts[nQual]+1
			else:
				qualCounts[nQual] = 1
		maxCounts={k:v for k, v in qualCounts.items() if v==max(qualCounts.values())}
		maxQual = min(maxCounts)
		return((x[0], maxQual))

	def restructure(x):
		return (x[0][0], x[0][1], x[1])

	predicted = topKById.map(getQual)\
		.map(restructure).toDF()\
		.withColumnRenamed('_1','id')\
		.withColumnRenamed('_2','true-quality')\
		.withColumnRenamed('_3','predicted-quality')

	def accurate(x):
		out = 1 if x['predicted-quality']==x['true-quality'] else 0
		return (out)

	acc = predicted.rdd.map(accurate).collect()
	accuracyScore = sum(acc)/len(acc)

	confusion = predicted.groupBy(F.col('true-quality'),F.col('predicted-quality'))\
		.agg(F.count('id').alias('count')).orderBy('true-quality','predicted-quality')

	
	#predicted.write.csv('knn-wines.out')
	confusion.show(24)
	print("Accuracy: ",accuracyScore)


if __name__ == "__main__":
	main()
