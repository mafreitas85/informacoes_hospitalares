# Informações Hospitalares – Pipeline de Engenharia de Dados

Projeto de engenharia de dados utilizando dados públicos do SIH-SUS (Sistema de Informações Hospitalares do SUS).

O projeto implementa uma arquitetura baseada em Data Lake com camadas **Bronze, Silver e Gold**, utilizando Docker para garantir reprodutibilidade do ambiente.

---

## Objetivo

Construir um pipeline de dados que:

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

- MinIO (S3 Compatível)

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

Obs: Na primeira execução pode demorar alguns minutos, até baixar todas as imagens.



**Execução dos Scripts**    

3. Os scripts devem ser executador no jupyterLab.

Acesse: http://localhost:8888/lab ou http://127.0.0.1:8888/lab



**Preparar o Data Lake**

      No jupyterLab abra um terminal e execute:

```bash
python work/Scripts/setup_lake.py
```

Isso irá:

- Criar bucket datalake

- Criar estrutura Bronze/Silver/Gold

- Enviar arquivos auxiliares

![Imagem](/home/marcos/Downloads/OneDrive_1_22-02-2026/01.PNG)



Estrutura de pasta criada no MinIO : [http://localhost:9001](http://localhost:9001) ou [http://127.0.0.1:9001](http://127.0.0.1:9001) Login: `admin` | Senha: `SenhaForte123!  



5. **Download dos Dados**
   
   ```bash
   python work/Scripts/00_download_sih.py
   ```

Isso fará:

- Download dos dados SIH

- Envio automático para a camada Bronze



Download deve demorar alguns minutos, ao término será possível visualizar os arquivos parquet's na camada bronze.



![Imagem](/home/marcos/Downloads/OneDrive_1_22-02-2026/2.PNG)



6. **Processamento Bronze → Silver**

```bash
python work/Scripts/01_bronze_to_silver.py
```

Gera:

- Delta Lake particionado por ano e mês



7. **Processamento Silver → Gold**

```bash
python work/Scripts/02_silver_to_gold.py
```

Gera:

- Dataset enriquecido

- Escrita na camada Gold

- Publicação no PostgreSQL

## 📊 Dashboard

O dashboard foi criado no Metabase, explorando os principais motivos de internação no estado de SP.



![Imagem](/home/marcos/Downloads/OneDrive_1_22-02-2026/Dashboard.png)





Obs: A pasta metabase_data não carreguei para o repositório.

Acesse o metabase no link abaixo, siga os passos e fique a vontade para criar seu próprio Dashboard!! :) 



Link metabase: http://localhost:3000



Configuração metabase

-   Preencha com seus dados, nome, e-mail e etc...

-   Defina uma senha
  
  

Configure conexão PostgreSQL:

- Host: postgres_lab

- Porta: 5432

- Banco: postgres

- Usuário: admin

- Senha: SenhaForte123!



Logo que conectado no postgres, por default o metabase já oferece uma análise nos dados do banco.

![](/home/marcos/snap/marktext/9/.config/marktext/images/2026-02-22-21-42-55-image.png)



---

## 👤 Autor

**Marcos Freitas Alves**  
[LinkedIn](https://www.linkedin.com/in/marcos-freitas-alves)

---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT.