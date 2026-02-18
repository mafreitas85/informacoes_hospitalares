import os
import glob
import boto3
from pysus import SIH

ANO = 2025
vUF = "SP"
bucket = "datalake"
bronze_prefix = f"bronze/sih_sus/{ANO}/"
base_path = "/home/jovyan/pysus"

def conectar_minio():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD")
    )

def baixar_sih():
    print("Baixando dados SIH...")
    sih = SIH().load() 
    files = sih.get_files("RD", uf=vUF, year=ANO)
    sih.download(files)     
    print("Download concluído.")

def enviar_para_bronze(s3):
    arquivos = glob.glob(f"{base_path}/**/*.parquet",recursive=True)
    print(f"{len(arquivos)} arquivos encontrados.")

    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            caminho_relativo = os.path.relpath(arquivo, base_path)
            destino = bronze_prefix + caminho_relativo.replace("\\", "/")

            s3.upload_file(arquivo, bucket, destino)
            print(f"✔ Enviado: {caminho_relativo}")

if __name__ == "__main__":
    s3 = conectar_minio()
    baixar_sih()
    enviar_para_bronze(s3)
    print("Processo finalizado com sucesso.")
