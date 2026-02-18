import os
from pyspark.sql import SparkSession

from spark_session import create_spark_session
spark = create_spark_session()

ano = "2025"
bronze_path = f"s3a://datalake/bronze/sih_sus/{ano}/*.parquet"               
silver_path = f"s3a://datalake/silver/sih_sus/"

df_raw = spark.read.parquet(bronze_path)

# Selecionar colunas específicas
df_sel = df_raw.select("UF_ZI", "ANO_CMPT","MES_CMPT","MUNIC_RES", "SEXO", "IDADE", "DIAG_PRINC", "VAL_TOT", "MORTE","DT_INTER","DT_SAIDA")

df_sel = (
    df_sel
    .withColumnRenamed("UF_ZI", "uf")
    .withColumnRenamed("ANO_CMPT", "ano")
    .withColumnRenamed("MES_CMPT", "mes")
    .withColumnRenamed("MUNIC_RES", "municipio_id")
    .withColumnRenamed("SEXO", "sexo")
    .withColumnRenamed("IDADE", "idade")   
    .withColumnRenamed("DIAG_PRINC", "cid_principal")    
    .withColumnRenamed("VAL_TOT", "valor_total")
    .withColumnRenamed("MORTE", "morte")
    .withColumnRenamed("DT_INTER", "data_internacao")
    .withColumnRenamed("DT_SAIDA", "data_saida")    
)


try:
    df_sel.write.format("delta") \
        .mode("overwrite") \
        .partitionBy("ano", "mes") \
        .save(silver_path)
except Exception as e:
    print("Erro:", e)
