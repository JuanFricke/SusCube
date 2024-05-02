# SusCube
Analise de dados do sus usando cubo de dados, OLAP e outros conceitos da materia de Big Data, Analytics e Métricas

## Adquirindo os Dados Brutos
> **Requisitos:** python3, wget e unzip.

Começe criando dois diretórios para armazenar os arquivos que serão baixados do DataSus, um para as bases principais e outro para as bases auxiliares:
```sh
$ mkdir data
$ mkdir data/aux
```
Agora use o utilitário **susgrep.sh** para fazer o download de todas as bases de dados necessárias para o SusCube:
```sh
$ ./susgrep.sh data data/aux
```
> A conversão dos arquivos baixados para formatos úteis (como .dbc para .dbf e .cnv para .csv) será feita automaticamente durante a execução do script.

## **Erros comuns no WSL:**
> Pacote unzip não está instalado no sistema
> WSL não reconhece cnv2csv

**Correções:**

```bash
$ sudo apt install unzip
```

```bash
$ dos2unix cnv2csv
```
