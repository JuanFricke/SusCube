# 1. Concepção do projeto:
## 1.1 Concepção de um plano de projeto
## 1.2 Descrição do problema
> A partir dos dados representados pelo modelo lógico e que reflete o ambiente OLTP dos sistemas do DATASUS, pretende-se projetar um sistema OLAP para facilitar o processo de geração de informações.
> A base de dados definida pelo Professor foi < ----- >
## 1.3 Justificativa

## 1.4 Objetivos
> Este estudo de caso tem como objetivo principal desenvolver uma solução de apoio a decisões para os gestores de saúde pública.
## 1.4 Metodologia
> Foi decidido pelo grupo que todo o trabalho seria feito por tecnologias diferentes devido a ser muito trabalhoso virtualizar uma imagem de _Windows_ 7 no sistema operacional _Linux_ e utilizar tecnologias legado.
> Portanto por foi escolhido que 
> - _Python_ para o processamento de dados e automação do processo de criação do banco de dados
> - _Duck DB_ como Banco de dados por suas otimizações para _OLAP_
> - _Pandas_ como Biblioteca que lida com organização de dados para a geração de relatórios
## 1.6 Cronograma
# 2. Implementação do Plano de Projeto proposto – critérios técnicos
## 2.1 Povoar o DW com dados
> Nesta etapa foi utilizado um <code> _Shell Script_ </code> para fazer o Download de todos os arquivos DBC e CNV do banco, para posteriormente ser convertido de DBC para DBF e os arquivos de CNV para CSV via um _Script_ em _Python_,
> Após o Download e as Conversões dos arquivos será feito a conversão de DBF para CSV e em seguida dado o Upload para o banco de dados via _Script_ de _Python_
## 2.2 Modelo Dimensional
## 2.3 Um exemplo de Dimensão com Hierarquia
## 2.4 Granularidade do DW (nível de detalhamento)
## 2.5 Exemplificação de operações DRILL DOWN/ROLL UP
## 2.6 Exemplificação de um CUBO DE DADOS (com dados)
## 2.7 Exemplificação da geração de relatórios usando o Excel (ou outra ferramenta) como ferramenta OLAP

# 3. Entrega
## 3.1 Entrega do projeto escrito, considerando os itens a e b
## 3.2 Apresentação do projeto e socialização dos resultados