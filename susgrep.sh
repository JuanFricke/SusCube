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
PARS_DIR=$SIASUS_DIR/200801_/Dados

SINASC_DIR=$DATASUS_FTP/dissemin/publicos/SINASC
SINASC_AUX_DIR=$SINASC_DIR/1996_/Auxiliar
DNRS_DIR=$SINASC_DIR/1996_/Dados/DNRES

# Lista de arquivos auxiliares em .cnv
aux_files_cnv=(
    "CID1017.cnv"    # Doencas
    "escmaepil.CNV"  # Escolaridade da mae
    "REGIAO.CNV"     # Regioes
    "MESORS.CNV"     # Mesoregioes
    "MICRORS.CNV"    # Microregioes
    "UF.CNV"         # Estados
    "MUNICRS.CNV"    # Municipios
    "GESTACAO.CNV"   # Tempo de gestacao
    "GRAVIDEZ.CNV"   # Tipo de gravidez
    "KOTELCHUCK.CNV" # Qualidade do prenatal
    "NATURAL.CNV"    # Pais natural
    "NOTIF98.CNV"    # Doencas de feto???
    "OBPARTO.CNV"    # Obito no parto
    "ob_ocorreu.CNV" # Detalhes sobre obito
    "OCUPACAO.CNV"   # Ocupacao (CBO???)
    "SGRPOCUP.CNV"   # Ocupacao por grupo
    "PARTO.CNV"      # Tipo de parto
    "PESO1.CNV"      # Peso bebe
    "PRENATAL.CNV"   # Numero de consultas pre
    "RACA.CNV"       # Raca
    # "ROBSON.CNV"   # ROBSON!
    "SITCONJU.CNV"   # Estado civil da mae
    "TPFUNC.CNV"     # Tipo do medico no parto?
)

# Lista de arquivos auxiliares em .dbf
aux_files_dbf=(
    "CNESDN22.DBF"   # Estabelecimentos de saude
)

cd $AUX_DIR

echo "Baixando arquivos auxiliares..."
wget -q $SINASC_AUX_DIR/NASC_NOV_TAB.zip

echo "Descompactando arquivos auxiliares..."
unzip -q NASC_NOV_TAB.zip

# Removendo arquivos extras e inuteis :)
echo "Limpando o lixo..."
rm NASC_NOV_TAB.zip
rm *.!(DBF|dbf|CNV|cnv)

cd "$TOP_DIR"

# Convertendo os arquivos .cnv solicitados
for file in "${aux_files_cnv[@]}"; do
    cur_file_path=$AUX_DIR/$file
    echo "Convertendo $cur_file_path para .csv..."
    ./cnv2csv $cur_file_path 
done

cd $AUX_DIR

# Removendo os .cnv que sobraram
echo "Limpando o lixo..."
rm *.cnv && rm *.CNV

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
# function datesus() {
    # for i in $(eval echo {$2..$3}); do
        # for j in {1..12}; do
            # file=$1$i
            # if [ $j -lt 10 ] 
            # then
                # file=$file"0$j"
            # else
                # file=$file$j
            # fi

            # echo $file$4
        # done
    # done
# }

#
# Lista arquivos baseado em um intervalo de tempo
# no padrao usado pelo DATSUS 
#
# params: prefixo, inicio, fim, sufixo
#
function datesus() {
    for i in $(eval echo {$2..$3}); do
        echo $1$i$4
    done
}

# https://gist.github.com/hrwgc/7455343
# function validate_url() {
  # if [[ `wget -S --spider $1  2>&1 | grep '200'` ]]; then echo "true"; fi
# }

cd $DATA_DIR

# Intervalo de tempo dos dados
from=2013 
to=2022

# TODO: So aceita arquivos com ext .dbc e nao .DBC
for file in $(datesus DNRS $from $to .dbc); do
    # Checa se o arquivo existe, visto que algum
    # mes pode ainda nao ter dados
    # if `validate_url $DNRS_DIR/$file > /dev/null`;
    # then 
        # continue 
    # fi

    echo "Baixando $file..."
    wget -q $DNRS_DIR/$file

    # blast-dbf cortesia de: 
    # https://github.com/eaglebh/blast-dbf
    echo "Convertendo $file para .dbf..."
    eval "'$TOP_DIR/blast-dbf' $file ${file%.*}.dbf"
done

echo "Limpando o lixo..."
rm *.dbc # && rm *.DBC

echo "Finalizado com sucesso!"
