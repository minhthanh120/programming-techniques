from pyspark.sql import SparkSession
import logging
logging.getLogger("py4j").setLevel(logging.ERROR)
logging.getLogger("pyspark").setLevel(logging.ERROR)

spark = SparkSession.builder.remote("sc://localhost:15002")\
.getOrCreate()

    #.config("spark.jars", "./mssql-jdbc-7.0.0.jre8.jar")\
#spark.conf.set("spark.sql.repl.eagerEval.enabled", True) # Property used to format output tables better
print(spark.version)

db = 'xomdata_dataset'
schema= 'adventure_works'
table = 'products'
url = f"jdbc:sqlserver://217.15.160.238:1433;databaseName={db}"
df = spark.read\
    .format("jdbc") \
    .option("url", url)\
    .option("dbtable",f"{schema}.{table}")\
    .option("user", "dingjonghan")\
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")\
    .option("password", "uJx4LzbCU@").load()

df.printSchema()
df.show(5,truncate= False)