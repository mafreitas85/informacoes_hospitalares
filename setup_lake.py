import os
import boto3

# Variáveis de ambiente
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USER = os.getenv("MINIO_ROOT_USER")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

BUCKET = "datalake"

print("Conectando ao MinIO...")

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_USER,
    aws_secret_access_key=MINIO_PASSWORD
)

# Criar bucket se não existir
try:
    s3.head_bucket(Bucket=BUCKET)
    print("Bucket já existe.")
except:
    print("Criando bucket...")
    s3.create_bucket(Bucket=BUCKET)

# Criar estrutura lógica
prefixos = [
    "bronze/",
    "silver/",
    "gold/",
    "Auxiliar/"
]

for prefixo in prefixos:
    s3.put_object(Bucket=BUCKET, Key=prefixo)
    print(f"Estrutura criada: {prefixo}")

# Upload arquivos auxiliares
print("Enviando arquivos auxiliares...")

arquivos_aux = [
    ("auxiliar/Tabela_municipio.csv", "Auxiliar/Tabela_municipio.csv"),
    ("auxiliar/cid_descricao_comuns.csv", "Auxiliar/cid_descricao_comuns.csv"),
]

for origem, destino in arquivos_aux:
    if os.path.exists(origem):
        s3.upload_file(origem, BUCKET, destino)
        print(f"Enviado: {destino}")
    else:
        print(f"Arquivo não encontrado: {origem}")

print("Setup finalizado com sucesso.")

