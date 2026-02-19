# Informações Hospitalares – Pipeline de Engenharia de Dados

Projeto completo de engenharia de dados utilizando dados públicos do SIH-SUS (Sistema de Informações Hospitalares do SUS).

O projeto implementa uma arquitetura moderna baseada em Data Lake com camadas **Bronze, Silver e Gold**, utilizando Docker para garantir reprodutibilidade do ambiente.

---

## Objetivo

Construir um pipeline completo de dados que:

- Realiza download automatizado dos dados do SIH

- Armazena os dados brutos na camada Bronze (MinIO)

- Realiza transformações com Spark (Silver)

- Aplica enriquecimentos e modelagem analítica (Gold)

- Publica dados no PostgreSQL

- Disponibiliza visualização via Metabase

---

## 🧱 Arquitetura

SIH (Download)
      ↓
Bronze (MinIO - Parquet)
      ↓
Silver (Delta Lake particionado por ano/mês)
      ↓
Gold (Delta Lake modelado para análise)
      ↓
PostgreSQL
      ↓
Metabase Dashboard

## Stack Utilizada

- Apache Spark 3.5

- Delta Lake

- MinIO (S3 Compatible)

- PostgreSQL

- Metabase

- Docker & Docker Compose

- PySpark

- boto3

## 📁 Estrutura do Projeto

```
Informacoes_hospitalares/
├── notebooks/              # Scripts PySpark (.ipynb)
├── .env                    # Configuração
├── docker-compose.yml      # Infraestrutura local
├── data/                   # Arquivos auxiliares (ex: CSV de CID-10)
├── docs/                   # Print do dashboard
└── README.md               # Este arquivo
```

---

## ▶️ Como Executar Localmente

> Pré-requisitos:
> 
> - Docker e Docker Compose
> - Git
> - PySpark (caso rode localmente fora do container)



1. **Clone o repositório:**

```bash
git clone https://github.com/mafreitas85/Informacoes_hospitalares.git
cd Informacoes_hospitalares
```

2. **Suba o ambiente:**

```bash
docker compose up -d
```

Isso irá subir:

- Spark Master

- Spark Worker

- MinIO

- PostgreSQL

- Metabase



3. **Acesse os serviços:**
   
   
- **MinIO**: http://localhost:9001  
  Login: `admin` | Senha: `SenhaForte123!`

- **Metabase**: http://localhost:3000  
  Login: definido na primeira configuração

- **PostgreSQL**: `localhost:5432`  
  Usuário: `admin` | Senha: `SenhaForte123!` | Banco: `my_database`



4. **Preparar o Data Lake**

        Execute dentro do container do Jupyter:

```bash
docker exec -it spark_jupyter bash
python Scripts/setup_lake.pyIsso irá:
```

- Criar bucket datalake

- Criar estrutura Bronze/Silver/Gold

- Enviar arquivos auxiliares



5. **Download dos Dados**
   
   ```bash
   python Scripts/download_sih.py
   ```

Isso fará:

- Download dos dados SIH

- Envio automático para a camada Bronze



6. **Processamento Bronze → Silver**

```bash
python Scripts/01_bronze_to_silver.py
```

Gera:

- Delta Lake particionado por ano e mês



7. **Processamento Silver → Gold**

```bash
python Scripts/02_silver_to_gold.py
```

Gera:

- Dataset enriquecido

- Escrita na camada Gold

- Publicação no PostgreSQL



## 📊 Dashboard

O dashboard foi criado no Metabase, explorando os principais motivos de internação no estado de SP.

> 📷 Um print do dashboard será incluído na pasta `/docs`.



Link metabase: http://localhost:3000



Configure conexão PostgreSQL:

- Host: postgres_lab

- Porta: 5432

- Banco: postgres

- Usuário: admin

- Senha: SenhaForte123!

---

## 👤 Autor

**Marcos Freitas Alves**  
[LinkedIn](https://www.linkedin.com/in/marcos-freitas-alves)

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT.