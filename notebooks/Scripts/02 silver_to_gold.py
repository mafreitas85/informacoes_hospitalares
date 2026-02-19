import sys
sys.path.append("/home/jovyan/work/Scripts")

import os
usuario = os.getenv("POSTGRES_USER")
senha = os.getenv("POSTGRES_PASSWORD")
url = os.getenv("POSTGRES_URL")

from spark_session import create_spark_session
spark = create_spark_session()

from pyspark.sql import functions as F
from pyspark.sql.types import DateType, IntegerType

ano = "2025"
silver_path = f"s3a://datalake/silver/sih_sus"      
municipio_path = f"s3a://datalake/Auxiliar/Tabela_municipio.csv"
cids_path = f"s3a://datalake/Auxiliar/cid_descricao_comuns.csv" 


df_municipio = spark.read.csv(municipio_path,header=True,sep=";",encoding="UTF-8")
df_cid = spark.read.csv(cids_path,header=True,sep=";",encoding="UTF-8")

df_cid_sel = df_cid.select('SUBCAT','DESCRICAO')

df_silver = spark.read.format("delta").load(silver_path)

df_municipio = df_municipio.select(
    F.substring(F.col("Código IBGE"),1,6).alias("codigo_ibge"),
    F.col("Município").alias("municipio"),
    
)

# Seleção e renomeação de colunas principais
df_gold = df_silver.select(    
    F.col("ano_competencia"),
    F.col("mes_competencia"),
    F.col("uf"),
    F.col("municipio_id").alias("cod_municipio_residencia"),
    F.col("idade").cast(IntegerType()).alias("idade"),
    F.col("sexo"),
    F.to_date("data_internacao", "yyyyMMdd").alias("data_internacao"),
    F.to_date("data_saida", "yyyyMMdd").alias("data_saida"),
    F.col("cid_principal"),
    F.col("valor_total").cast("double").alias("valor_total"),
    F.col("morte")
)

# Criação de colunas derivadas
df_gold = df_gold.withColumn("ano_internacao", F.year("data_internacao")) \
                 .withColumn("mes_internacao", F.month("data_internacao")) \
                 .withColumn("dias_internacao",F.datediff(F.col("data_saida"), F.col("data_internacao"))) \
                 .withColumn(
                     "faixa_etaria",
                     F.when(F.col("idade") < 1, "Menor de 1 ano")
                      .when(F.col("idade") < 5, "1-4 anos")
                      .when(F.col("idade") < 10, "5-9 anos")
                      .when(F.col("idade") < 20, "10-19 anos")
                      .when(F.col("idade") < 60, "20-59 anos")
                      .otherwise("60+ anos")
                 )

df_gold = df_gold.join(
    df_cid_sel,
    df_gold.cid_principal == df_cid.SUBCAT,
    "left"
).withColumnRenamed("DESCRICAO", "descricao_cid")


df_enriquecido = df_gold.join(df_municipio, df_gold.cod_municipio_residencia == df_municipio.codigo_ibge, "left")


df_enriquecido.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("ano_competencia", "mes_competencia") \
    .option("overwriteSchema", "true") \
    .save("s3a://datalake/gold/sih_sus/")


postgres_host = os.getenv("POSTGRES_HOST")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")

url = f"jdbc:postgresql://{postgres_host}:5432/{postgres_db}"
tabela = "sih_sus_gold"

print("Iniciando carga no PostgreSQL...")

(
    df_enriquecido
    .repartition(4)
    .write
    .format("jdbc")
    .option("url", url)
    .option("dbtable", tabela)
    .option("user", postgres_user)
    .option("password", postgres_password)
    .option("driver", "org.postgresql.Driver")
    .option("batchsize", 10000)
    .mode("overwrite")
    .save()
)

print("Carga no PostgreSQL concluída com sucesso.")

spark.stop()
