-- Criação das Dimensões

-- Dimensão Data
CREATE VIEW Dim_Data AS
WITH datas_join AS (
	SELECT DISTINCT ap_cmp AS data, 'cmp'
	FROM main.atdrs
	UNION
	SELECT DISTINCT ap_mvm AS data, 'mvm'
	FROM main.atdrs
)
SELECT DISTINCT 
	data AS data_completa,
	CAST(SUBSTR(DATA, 1, LENGTH(DATA) - 2) AS INT) AS ano,
	CAST(FLOOR((CAST(SUBSTR(data, LENGTH(data) - 1) AS INT) + 2)/3) AS INT) AS trimestre,
	CAST(SUBSTR(data, LENGTH(data) - 1) AS INT) AS mes
FROM datas_join
ORDER BY data;

-- Dimensão Estabelecimento
CREATE VIEW Dim_Estabelecimento AS
WITH temp_estab AS (
	SELECT DISTINCT
		CONCAT(ap_coduni, ap_tpups) AS id,
		ap_coduni AS id_estab, 
		ap_tpups AS id_tipo_estab
	FROM main.atdrs
)
SELECT 
	te.id,
	tp_e.descr AS DESCRICAO_ESTAB,
	cad.*
FROM temp_estab AS te
LEFT JOIN main.cadgerrs AS cad
	ON te.id_estab = cad.CNES
LEFT JOIN main.TP_ESTAB  AS tp_e
	ON te.id_tipo_estab = tp_e.codigo;

-- Dimensão Geografia
CREATE VIEW Dim_Geografia AS
SELECT 
	mun.codigo AS id,
	mun.descr AS municipio,
	mic.descr AS microrregiao,
	mac.descr AS macrorregiao
FROM main.rs_municip AS mun
LEFT JOIN main.rs_micibge AS mic
	ON CAST(mun.codigo AS varchar) = mic.codigo
LEFT JOIN main.rs_macsaud AS mac
	ON mun.codigo = mac.codigo;

-- Dimensão Saida
CREATE VIEW Dim_Saida AS
SELECT DISTINCT
    CONCAT(ap_motsai, ap_alta, ap_obito, ap_encerr, ap_perman, ap_transf) AS Saida_ID,
    ap_motsai, ap_alta, ap_obito, ap_encerr, ap_perman, ap_transf
FROM main.atdrs;

-- Dimensão CID
CREATE VIEW Dim_CID AS
SELECT DISTINCT *
FROM main.s_cid;

-- Criação da Tabela de Fatos
CREATE VIEW Fato_Dialise AS
SELECT 
	--Dimensoes
	atdrs.ap_mvm AS data_processamento,
	atdrs.ap_cmp AS data_atendimento,
	CONCAT(atdrs.ap_coduni, atdrs.ap_tpups) AS id_estabelecimento,
	atdrs.ap_ufmun AS mun_estabelecimento,
	atdrs.ap_munpcn AS mun_paciente,
	CONCAT(atdrs.ap_motsai, atdrs.ap_alta, atdrs.ap_obito, atdrs.ap_encerr, atdrs.ap_perman, atdrs.ap_transf) AS id_saida,
	atdrs.ap_cidpri AS id_CID_principal,
	atdrs.ap_cidsec AS id_CID_secundario,
	atdrs.ap_cidcas AS id_CID_causa_associada,
	
	--Valores do fato registrados na tabela
	(atdrs.ap_ufmun <> atdrs.ap_munpcn) AS invasao_municipal,
	ap_vl_ap AS valor_aprovado,
	atd_maisne AS dialise_recorrente,
	
	--Valores do fato de outras tabelas
	atdcaract.descr AS caracteristica_tratamento,
	TPAPAC.descr AS tipo_APAC,
	idade.descr AS idade_paciente,
	sexo.descr AS sexo_paciente,
	raca_cor.descr AS raca_cor_paciente,
	sit_ini.descr AS situacao_inicial,
	sit_tra.descr AS situacao_transplante,
	se_apto.descr AS se_apto_transplante
FROM main.atdrs AS atdrs
LEFT JOIN main.atd_caract AS atdcaract
	ON atdrs.atd_caract = atdcaract.codigo
LEFT JOIN main.TP_APAC AS TPAPAC
	ON atdrs.ap_tpapac = TPAPAC.codigo
LEFT JOIN main.IDADE AS idade
	ON atdrs.ap_nuidade = CAST(idade.codigo AS INT)
LEFT JOIN main.SEXO AS sexo
	ON atdrs.ap_sexo = sexo.codigo
LEFT JOIN main.RACA_COR AS raca_cor
	ON atdrs.ap_racacor = raca_cor.codigo
LEFT JOIN main.atd_sitini AS sit_ini
	ON atdrs.atd_sitini = sit_ini.codigo
LEFT JOIN main.atd_sittra AS sit_tra
	ON atdrs.atd_sittra = sit_tra.codigo
LEFT JOIN main.atd_seapto AS se_apto
	ON atdrs.atd_seapto = se_apto.codigo;
