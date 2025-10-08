from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParallelWordCount") \
        .master("spark://localhost:7077")\
        .config("spark.driver.host", "host.docker.internal")\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
    .getOrCreate()
sc = spark.sparkContext # Lấy SparkContext để làm việc với RDD
# 1. Khởi tạo một biến Python thông thường trên Driver

lines_rdd = sc.parallelize([
    "Đây là dòng 1",
    "",
    "Đây là dòng 3",
    "   ", # Dòng này cũng được coi là trống nếu ta strip()
    "Đây là dòng 5",
    ""
])
# 2. Cố gắng tăng biến đếm bên trong một tác vụ phân tán
def check_line(line):
    local_count = 0
    if len(line.strip()) == 0:
        local_count += 1
    return local_count

# Spark sẽ cố gắng chạy hàm này trên các Executor
normal_counter = lines_rdd.map(check_line).reduce(lambda a,b:a+b)

# 3. In kết quả trên Driver
print(f"Giá trị cuối cùng của biến đếm thông thường: {normal_counter}")
blank_lines_counter = sc.accumulator(0)


# 2. Sử dụng Accumulator bên trong một tác vụ song song (ở đây là forEach)
def count_blanks(line):
    if len(line.strip()) == 0:
        # Chỉ có thể .add() vào accumulator
        blank_lines_counter.add(1)

# forEach là một ACTION, Spark sẽ thực thi và tính toán
lines_rdd.foreach(count_blanks)

# 3. Chỉ Driver mới có thể đọc giá trị cuối cùng
print("="*30)
print(f"Tổng số dòng trống là: {blank_lines_counter.value}")
print("="*30)
spark.stop()