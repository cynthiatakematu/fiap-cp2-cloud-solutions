# fiap-cp2-cloud-solutions

Checkpoint 02 – Cloud Solutions (FIAP): pipeline Databricks que carrega CSVs de focos de queimadas do INPE em um Azure Database for MySQL Flexible Server.

Baseado em [rksakai/QueimadasINPE-Databricks](https://github.com/rksakai/QueimadasINPE-Databricks).

## Estrutura

```text
.github/workflows/terraform-apply.yml   # workflow manual que provisiona o MySQL
infra/                                  # Terraform (MySQL Flexible Server + banco + firewall)
databricks/
├── 01_bronze_csv_ingest.py             # CSV do volume -> inpe.bronze.focos_raw
├── 02_silver_standardize_quality.py    # limpeza/qualidade -> inpe.silver.queimadas_focos
└── 03_gold_publish_mysql.py            # agregações -> tabelas gold_* no MySQL
```

## Pré-requisitos

Backend do Terraform (criar uma vez, no Azure Cloud Shell):

```bash
az group create -n rg-tfstate -l eastus
az storage account create -n stfiapcp2cloudsolutions -g rg-tfstate -l eastus --sku Standard_LRS
az storage container create -n tfstate --account-name stfiapcp2cloudsolutions
```

Secrets do repositório (*Settings → Secrets and variables → Actions*):

| Secret | Conteúdo |
|---|---|
| `AZURE_CREDENTIALS` | saída de `az ad sp create-for-rbac --name sp-fiap-cp2-cloud-solutions --role Contributor --scopes /subscriptions/<SUBSCRIPTION_ID> --json-auth` |
| `MYSQL_ADMIN_PASSWORD` | senha do administrador do MySQL |

## Execução

1. *Actions → provision-mysql-queimadas → Run workflow*.
2. No Databricks, criar o catálogo `inpe`, os schemas `bronze`, `silver`, `gold` e o volume `inpe.bronze.arquivo`.
3. Criar um notebook por script de `databricks/`. No notebook Gold, preencher `mysql_host` e `mysql_password` (não versionar a senha).
4. Criar o job `fiap-cp2-cloud-solutions` com as tasks `bronze → silver → gold`, parâmetro `input_file_path = {{job.trigger.file_arrival.location}}` na task bronze e trigger *File arrival* em `/Volumes/inpe/bronze/arquivo/`.
5. Subir, um por vez, três CSVs de <https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/> no volume.
6. Conferir no MySQL: `SHOW TABLES;` e `SELECT COUNT(*)` de cada tabela `gold_*`.
