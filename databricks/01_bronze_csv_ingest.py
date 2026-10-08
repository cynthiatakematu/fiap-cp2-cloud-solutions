from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, TimestampType, LongType
)
from pyspark.sql import Row
from datetime import datetime

dbutils.widgets.text("input_file_path", "")
input_file_path = dbutils.widgets.get("input_file_path")

if not input_file_path:
    raise ValueError("Parâmetro input_file_path não informado.")

file_name = input_file_path.split("/")[-1]

audit_rows = [Row(
    data_processamento=str(datetime.now()),
    arquivo_origem=file_name,
    caminho_arquivo=input_file_path,
    status="sucesso"
)]

spark.createDataFrame(audit_rows).write.mode("append").saveAsTable("INPE.bronze.auditoria_ingestao")

schema = StructType([
    StructField("id", StringType()),
    StructField("lat", DoubleType()),
    StructField("lon", DoubleType()),
    StructField("data_hora_gmt", TimestampType()),
    StructField("satelite", StringType()),
    StructField("municipio", StringType()),
    StructField("estado", StringType()),
    StructField("pais", StringType()),
    StructField("municipio_id", LongType()),
    StructField("estado_id", LongType()),
    StructField("pais_id", LongType()),
    StructField("numero_dias_sem_chuva", LongType()),
    StructField("precipitacao", DoubleType()),
    StructField("risco_fogo", DoubleType()),
    StructField("bioma", StringType()),
    StructField("frp", DoubleType()),
])

df_bronze = (
    spark.read
    .option("header", True)
    .option("encoding", "UTF-8")
    .schema(schema)
    .csv(input_file_path)
)

display(df_bronze)
df_bronze.printSchema()

df_bronze.write.format("delta").mode("overwrite") \
    .saveAsTable("INPE.bronze.focos_raw")
