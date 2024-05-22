---
marp: true
style: |
    img[alt~="center"] {
      display: block;
      margin: 0 auto;
    }

---
<!-- theme: uncover   -->
<!-- class: invert -->

### Projeto de DW – Estudo de Caso DATASUS
![bg right:50% w:500](photos/cubo-brazil-data-cube-bdc.png)
###### Gustavo Campos, Bruno Moretto, Gabriel Buron, Juan Fricke

---

# Processos de negócios do DATASUS...




---

# Concepção de um plano de projeto

* Uma análise preliminar revelou a extensão considerável e a complexidade do escopo do projeto

* repositório Git central
*controle temporal e espacial sobre o processo de desenvolvimento.*

---

# Vantagens de um repositorio git centralizado

* controle temporal e espacial sobre o processo de desenvolvimento.

* estruturação do projeto

* centrada à automação da coleta dos dados

* facilitar o manuseio das bases utilizadas

---

# Descrição do problema

A partir dos dados representados pelo modelo lógico e que reflete o ambiente OLTP dos sistemas do DATASUS, pretende-se projetar um sistema OLAP para facilitar o processo de análise dos dados e geração de insights.

![:100% w:1000](photos/Roll-up-and-Drill-down-operations.png)

---

![:100% w:800](photos/star-vs-snow.jpg)
Com base nisso, o sistema deverá ser projetado em modelo de estrela ou floco-de-neve, bem como deverá ser capaz de performar consultas OLAP e operações de roll-up e drill-down sobre os dados da base selecionada.

---

# Justificativa



---

# Objetivos

---

# Metodologia

---

# Modelo Dimensional

---

# Um exemplo de Dimensão com Hierarquia

---

# Granularidade do DW (nível de detalhamento)

---

# Exemplificação de operações DRILL DOWN/ROLL UP

---

# Exemplificação de um CUBO DE DADOS (com dados)

--- 

# Exemplificação da geração de relatórios usando ferramenta OLAP

---

![bg center:100% w:700](photos/susgpre.sh-in-action.png)

---

![bg center:100% w:700](photos/First-Version-running.png)

---