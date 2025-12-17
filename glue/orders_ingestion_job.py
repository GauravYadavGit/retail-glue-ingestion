from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import StringType
import sys

# --------------------------------------------------
# Job init
# --------------------------------------------------
args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_BUCKET", "SOURCE_KEY"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --------------------------------------------------
# Dynamic paths from EventBridge
# --------------------------------------------------
SOURCE_BUCKET = args["SOURCE_BUCKET"]
SOURCE_KEY = args["SOURCE_KEY"]

RAW_PATH = f"s3://{SOURCE_BUCKET}/{SOURCE_KEY}"
PROCESSED_PATH = "s3://my-retail-glue-demo-ap-south-1/processed/orders/"

print("🚀 Glue job started")
print(f"📥 Triggered file: {RAW_PATH}")
print(f"📤 Processed path: {PROCESSED_PATH}")

# --------------------------------------------------
# Read ONLY the triggered RAW file
# --------------------------------------------------
raw_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": [RAW_PATH]},
)

record_count = raw_dyf.count()
print(f"📊 Raw record count = {record_count}")

# --------------------------------------------------
# IMPORTANT: DO NOT EXIT EARLY
# --------------------------------------------------
if record_count == 0:
    print("✅ No records found in file. Safe no-op run.")
else:
    raw_df = raw_dyf.toDF()

    # --------------------------------------------------
    # Schema normalization
    # --------------------------------------------------
    if "coupon" not in raw_df.columns:
        raw_df = raw_df.withColumn("coupon", F.lit(None).cast(StringType()))

    df = (
        raw_df.withColumn("order_ts", F.to_timestamp("order_ts"))
        .withColumn("order_date", F.to_date("order_ts"))
        .withColumn("ingestion_ts", F.current_timestamp())
    )

    # --------------------------------------------------
    # Deduplication (latest order per order_id)
    # --------------------------------------------------
    window = Window.partitionBy("order_id").orderBy(F.col("order_ts").desc())

    dedup_df = (
        df.withColumn("rn", F.row_number().over(window))
        .filter(F.col("rn") == 1)
        .drop("rn")
    )

    # --------------------------------------------------
    # Upsert logic (insert + update)
    # --------------------------------------------------
    try:
        existing_df = spark.read.parquet(PROCESSED_PATH)
        print("📂 Existing processed data found")

        inserts_df = dedup_df.join(
            existing_df.select("order_id"),
            on="order_id",
            how="left_anti",
        )

        updates_df = (
            dedup_df.alias("n")
            .join(existing_df.alias("e"), on="order_id", how="inner")
            .filter(F.col("n.order_ts") > F.col("e.order_ts"))
            .select("n.*")
        )

        final_df = inserts_df.unionByName(updates_df)

    except Exception as e:
        print("📂 No existing processed data found")
        final_df = dedup_df

    write_count = final_df.count()
    print(f"✍️ Writing {write_count} records")

    (final_df.write.mode("append").partitionBy("order_date").parquet(PROCESSED_PATH))

# --------------------------------------------------
# ALWAYS COMMIT
# --------------------------------------------------
print("✅ Job committing")
job.commit()
print("🎉 Job completed successfully")
