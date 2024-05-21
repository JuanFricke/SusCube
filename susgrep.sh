#! /usr/bin/bash

# Requisitos: python3, wget, unzip 

# Checa e avisa o usuario do correto uso das flags
if [ "$#" -ne 2 ]
then
    echo "Uso: ./susgrep out_dir/ out_aux_dir/"
    exit 1
fi

shopt -s extglob

TOP_DIR=$(dirname "$(realpath "$0")")
DATA_DIR="${1%/}"
AUX_DIR="${2%/}"

DATASUS_FTP="ftp://ftp.datasus.gov.br"

SIASUS_DIR=$DATASUS_FTP/dissemin/publicos/SIASUS
ATDRS_DIR=$SIASUS_DIR/200801_/Dados
ATDRS_AUX_DIR=$SIASUS_DIR/200801_/Auxiliar

# Lista de arquivos auxiliares em .cnv
aux_files_cnv=(
    "rs_divadm.cnv"  # Algo de regioes administrativas
    "rs_micibge.cnv" # Codigo de microregioes
    "rs_macsaud.cnv" # Macroregioes de saude???
    "rs_municip.cnv" # Municipios
    "rs_regmetr.cnv" # Regioes metropolitanas
    "rs_regsaud.cnv" # Regioes de saude???

    "CARATER.CNV"    # Tem ate coisas de acidente aqui, olha so!
    "CODOCO.CNV"     # Algo sobre aprovamento de valores e producoes
    "COMPLEX.CNV"    # Complexidade
    "ESFERA.CNV"     # Esfera federal, estadual, estabelecimento privado, etc...
    "MED_ONC.CNV"    # Medicamentos (oncologicos?)
    "MOTSAIPE.CNV"   # Motivo de alta ou algo assim
    "PT_TABBA.CNV"   # Algo sobre comorbidade
    "QDT_TRAN.CNV"   # Transplantado
    "RACA_COR.CNV"   # Cor
    "REGRA_C.cnv"    # Regra contratual
    "SEXO.CNV"       # Sexo
    "TP_APAC.CNV"    # Tipo de APAC
    "TP_ATEND.CNV"   # Tipo de atendimento
    "TP_DROGA.cnv"   # Tipo de droga (droga mesmo, nao remedio)
    "TP_ESTAB.CNV"   # Tipo de estabelecimento de saude
    "UF.CNV"         # Estado brasileiro
    "UFNACIO.CNV"    # Pais
    "atd_acevas.cnv" # Tipo acesso vascular
    "atd_caract.cnv" # Carater do tratamento
    "atd_dtcli.cnv"  # ?
    "atd_dtpdr.cnv"  # ??
    "atd_seapto.cnv" # Apto pra transplante
    "atd_sittra.cnv" # Situacao de tratamento

    # Talvez esses sejam uteis pra fazer o cubo de dados???
    "ANO.CNV"
    "ANOMESC.CNV"
)

# Lista de arquivos auxiliares em .dbf
aux_files_dbf=(
    "CADGERRS.dbf"      # CNESBR so que com mais detalhes (aparentemente)
    "INE_EQUIPE_RS.dbf" # Equipes de funcionarios da saude???
    "CBO.dbf"           # Codigo de ocupacao (profissao)
    "CNESBR.dbf"        # Codigo de estabelecimento de saude
    "HUF_FILIAL.dbf"    # Hospital universitario
    "HUF_MEC.dbf"       # Hospital universitario ++
    "S_CID.DBF"         # Codigo internacional de doencas
    "S_CLASSEN.dbf"     # Algo relacionado ao tipo de atendimento...?
    "S_FORNEC.DBF"      # Fornecedor de equipamentos medicos, talvez seja interessante!
    "TB_FORMA.DBF"      # Algo relacinado a medicamentos???
    "TB_SIGTAW.dbf"     # Algo relacionado a cobrancas ou pagamentos???
    "TB_SUBGR.DBF"      # Subgrupos
    "TP_FINAN.dbf"      # Financiamento???
    "tp_find.dbf"       # Parece ser um complementar para o TB_SIGTAW
)

cd $AUX_DIR

echo "Baixando arquivos auxiliares..."
wget -q $ATDRS_AUX_DIR/TAB_SIA.zip

echo "Descompactando arquivos auxiliares..."
unzip -q TAB_SIA.zip

# Removendo arquivos extras e inuteis :)
echo "Limpando o lixo..."
rm TAB_SIA.zip
rm *.def # *.!(DBF|dbf|CNV|cnv)
rm *.DEF
rm -r DADOS
rm -r Docs

cd "$TOP_DIR"

# Convertendo os arquivos .cnv solicitados
for file in "${aux_files_cnv[@]}"; do
    cur_file_path=$AUX_DIR/CNV/$file
    echo "Convertendo $cur_file_path para .csv..."
    ./cnv2csv $cur_file_path 
done

cd $AUX_DIR/CNV

# Removendo os .cnv que sobraram
echo "Limpando o lixo..."
rm *.cnv && rm *.CNV
cd ..
mv CNV CSV

cd $TOP_DIR/$AUX_DIR/DBF

# Removendo os .dbf nao utilizados
all_dbfs=($(find ./ -type f -name "*.dbf"))
all_dbfs+=($(find ./ -type f -name "*.DBF"))
for file in "${all_dbfs[@]}"; do
    if ! [[ "./${aux_files_dbf[@]}" =~ "$file" ]];
    then
        rm "$file"
    fi
done

cd "$TOP_DIR"

#
# Lista arquivos baseado em um intervalo de tempo
# no padrao usado pelo DATSUS 
#
# params: prefixo, inicio, fim, sufixo
#
function datesus_aamm() {
    for i in $(eval echo {$2..$3}); do
        for j in {1..12}; do
            # Ano
            file=$1${i:2:4}

            # Mes
            if [ $j -lt 10 ] 
            then
                file=$file"0$j"
            else
                file=$file$j
            fi

            echo $file$4
        done
    done
}

# https://gist.github.com/hrwgc/7455343
# function validate_url() {
  # if [[ `wget -S --spider $1  2>&1 | grep '200'` ]]; then echo "true"; fi
# }

cd $DATA_DIR

# Intervalo de tempo dos dados
from=2014 
to=2024

# TODO: So aceita arquivos com ext .dbc e nao .DBC
for file in $(datesus_aamm ATDRS $from $to .dbc); do
    # Checa se o arquivo existe, visto que algum
    # mes pode ainda nao ter dados
    # if `validate_url $DNRS_DIR/$file > /dev/null`;
    # then 
        # continue 
    # fi

    echo "Baixando $file..."
    wget -q $ATDRS_DIR/$file

    # O arquivo nao existe
    if [ $? -ne 0 ]; then
        echo "Arquivo $file nao encontrado! Continuando..."
        continue
    fi

    # blast-dbf cortesia de: 
    # https://github.com/eaglebh/blast-dbf
    echo "Convertendo $file para .dbf..."
    eval "'$TOP_DIR/blast-dbf' $file ${file%.*}.dbf"
done

echo "Limpando o lixo..."
rm *.dbc # && rm *.DBC

echo "Finalizado com sucesso!"
