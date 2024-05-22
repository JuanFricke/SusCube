# 1. Concepção do projeto:
## 1.1 Concepção de um plano de projeto
> Para planejar a execução do projeto, optou-se por uma abordagem mais flexível e adaptativa. Uma análise preliminar revelou a extensão considerável e a complexidade do escopo do projeto, tornando-o desafiador para uma mensuração precisa.

> Logo, ao invés de ser feito um planejamento prévio completo para o projeto, a alternativa que foi encontrada para organizar o desenvolvimento foi a criação de um repositório Git central. Nesse repositório foi armazenado todo o progresso do projeto, o que ajudou a manter um controle temporal e espacial sobre o o processo de desenvolvimento. 

> Além disso, isso também se mostrou de grande utilidade na questão da estruturação do projeto, já que tornou obrigatória a busca por uma abordagem mais centrada à automatização, para fazer a coleta dos dados. Isso foi feito a fim de otimizar o uso de espaço, além de facilitar o manuseio das bases utilizadas.
## 1.2 Descrição do problema
> A partir dos dados representados pelo modelo lógico e que reflete o ambiente OLTP dos sistemas do DATASUS, pretende-se projetar um sistema OLAP para facilitar o processo de análise dos dados e geração de insights.

> Com base nisso, o sistema deverá ser projetado em modelo de estrela ou floco-de-neve, bem como deverá ser capaz de performar consultas OLAP e operações de roll-up e drill-down sobre os dados da base selecionada.
## 1.3 Justificativa
> O uso de conceitos de ciência de dados em cenários que não sejam comerciais tem se mostrado muito eficaz ultimamente. Nesses casos, vale ressaltar as aplicações em que a implementação de sistemas de Big Data se sobressaem, como é o caso de cenários de análise de dados de saúde pública.

> Tendo isso em mente, o projeto englobará a implementação de um data warehouse simples para a base de dados de APAC de Tratamento Dialítico. Nesse contexto, também serão geradas algumas consultas OLAP que possam fornecer insights relevantes, a fim de explicitar a utilidade de tal serviço para aprimorar políticas públicas, ou procedimentos, relacionadas à saúde renal.

> Isso se aplica muito bem levando em conta a região da cidade de Ijuí, a qual possui estabelecimentos de saúde que podem ser considerados de referência, tanto regional como estadual, em questão de tratamentos renais e de suas causas associadas.
## 1.4 Objetivos
> Este estudo de caso tem como objetivo principal desenvolver uma solução de apoio a decisões para os gestores de saúde pública.
## 1.4 Metodologia
> Foi decidido pelo grupo que todo o trabalho seria feito por tecnologias diferentes devido a ser muito trabalhoso virtualizar uma imagem de _Windows_ 7 no sistema operacional _Linux_ e utilizar tecnologias legado.
> Portanto por foi escolhido que 
> - _Python_ para o processamento de dados e automação do processo de criação do banco de dados
> - _Duck DB_ como Banco de dados por suas otimizações para _OLAP_
> - _Pandas_ como Biblioteca que lida com organização de dados para a geração de relatórios
## 1.5 Cronograma
> !!! Não temos então acho q da pra ignorar esse topico
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