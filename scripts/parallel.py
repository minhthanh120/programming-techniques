from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParallelWordCount") \
        .master("spark://localhost:7077")\
        .config("spark.driver.host", "host.docker.internal")\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
    .getOrCreate()
sc = spark.sparkContext # Lấy SparkContext để làm việc với RDD

# Dữ liệu đầu vào
data = ["hello world spark is cool","hello spark patch", "hello spark streaming"]

# 1. Tạo RDD và chia thành 2 partition
rdd = sc.parallelize(data, 2)

# 2. Tách mỗi dòng thành các từ (flatMap)
words = rdd.flatMap(lambda line: line.split(" "))

# 3. Tạo cặp (từ, 1) cho mỗi từ (map)
word_pairs = words.map(lambda word: (word, 1))

# 4. Đếm số lần xuất hiện của mỗi từ (reduceByKey)
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

# 5. Thu thập kết quả về Driver và in ra
results = word_counts.collect()
for word, count in results:
    print(f"{word}: {count}")

spark.stop()