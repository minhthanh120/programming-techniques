from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParallelWordCount") \
        .master("spark://localhost:7077")\
        .config("spark.driver.host", "host.docker.internal")\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
    .getOrCreate()
sc = spark.sparkContext

# Dữ liệu bạn muốn chia sẻ: một map tra cứu
states = {"NY": "New York", "CA": "California", "TX": "Texas"}

# 1. Tạo Broadcast Variable trên Driver
broadcast_states = sc.broadcast(states)

# Dữ liệu cần xử lý
data = ["NY", "TX", "CA", "NY", "DT", "DT"]
rdd = sc.parallelize(data)

# Sử dụng broadcast variable bên trong một transformation
# Mỗi executor sẽ truy cập bản sao cục bộ của broadcast_states
def get_full_state_name(abbr):
    # .value để lấy dữ liệu từ bên trong broadcast variable
    return broadcast_states.value.get(abbr, "Unknown")

full_names_rdd = rdd.map(get_full_state_name)

print(full_names_rdd.collect())
# Kết quả: ['New York', 'Texas', 'California', 'New York']

spark.stop()