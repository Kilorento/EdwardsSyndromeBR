# Alterações por célula

Lista de todas as células alteradas depois das extrações independentes. Cada linha traz o valor anterior, o valor novo e o critério aplicado. A versão em planilha é `alteracoes_por_celula.csv`.

**Duas bases distintas:**

- **Base final (`julgados.csv`):** é a extração do Claude depois das decisões do pesquisador. É a base de análise.
- **Comparação entre extratores:** usa os valores independentes de cada extrator. As alterações I1 e I2 foram feitas só ali, sobre as extrações do Gemini e do Manus, e não alteram a base final.

## Critérios

| Código | Critério | Decidido por | Células |
|---|---|---|---|
| R1 | Resultado duplo ou múltiplo no mesmo acórdão → Parcialmente provido (todos falsos positivos). | Pesquisador | 5 |
| R2 | Indeferimento do pedido por decisão: o pedido liminar é o próprio objeto da ação → Liminar indeferida. | Pesquisador | 1 |
| R3 | Inadmissão de recurso especial na origem → Não conhecido. | Pesquisador | 1 |
| R5 | Competência declinada → Não conhecido; ligado ao julgado de mérito do mesmo processo (J053). | Pesquisador | 1 |
| R6 | Novo valor de via_processual: quem aciona o tribunal busca impedir a interrupção (MP ou terceiros pelo nascituro) → Impugnação da autorização. | Pesquisador | 6 |
| R7 | Novo valor de via_processual: MS contra hospital ou médico que se recusa a fazer o procedimento → Autorização prévia contra hospital ou médico. | Pesquisador | 1 |
| Ab | HC de 1º grau cujo dispositivo diz "julgo procedente" → Procedente (termo do dispositivo). | Pesquisador | 1 |
| Ac | Acórdão que concede a ordem liminarmente → Liminar deferida (mesmo valor dos acórdãos que concedem liminar; contado como resultado favorável em efeito_pratico). | Pesquisador | 2 |
| V1 | Processo de cobertura por plano de saúde, ainda que falso positivo → Autorização prévia contra operadora de plano. | Pesquisador | 2 |
| V2 | Ação indenizatória ligada à gestação ou ao diagnóstico → Demanda indenizatória conexa (correção de inconsistência do extrator, aprovada pelo pesquisador). | Pesquisador | 4 |
| X1 | Despacho sem conteúdo decisório não é julgado: retirado da base e mantido em documentos_de_contexto.csv, ligado ao J013. | Pesquisador | 1 |
| A1 | Nova coluna art128_I: como o julgador tratou o art. 128, I, do CP (Aplicado · Afastado · Remetido ao médico · Risco discutido sem o artigo · Mencionado sem exame · Não mencionado · Não acessível). | Pesquisador | 1 |
| EP | Nova coluna efeito_pratico (Autoriza · Nega · Sem efeito · Não aplicável): efeito da decisão sobre a interrupção, independentemente do rótulo processual. | Pesquisador | 1 |
| I1 | Nas extrações das IAs: momento_idade_gestacional = "Não especificado" sem idade gestacional informada → Não consta (sem IG não há momento). | Pesquisador | 78 |
| I2 | Nas extrações das IAs: "Autorização prévia contra o Estado" em alvará, HC ou MS contra ato judicial → sem polo passivo (o Estado não é réu). | Pesquisador | 78 |
| RA | Conversão dos fundamento_* para três valores: Sim → Acolhe; Não → Não enfrenta (julgados fora da lista de releitura). | Pesquisador | 1 |
| RF | Releitura no corpus: o julgador examinou o fundamento e o afastou → Rejeita. | Pesquisador (regra); Extrator (leitura) | 59 |
| RP | Convenção da releitura: risco à vida remetido ao médico, com carência de ação → Rejeita. | Extrator (convenção), aceita pelo pesquisador em 14/10; a situação fica explícita na coluna art128_I (Remetido ao médico) | 2 |
| CE | comparacao_com_anencefalia: Equipara sempre que o julgado aplica a ADPF 54 por analogia; Distingue quando recusa a analogia. | Pesquisador (regra); Extrator (leitura) | 8 |
| CP | comparacao_com_anencefalia: analogia direta reconhecida em julgado cuja razão principal é outra (art. 128, I). | Pesquisador (regra da analogia direta); Extrator (leitura) | 1 |


## Células

| # | Base | Julgado | Campo | Antes | Depois | Critério |
|---|---|---|---|---|---|---|
| 1 | Claude (base final) | J002 | `provimento` | REPORTAR | Parcialmente provido | R1 |
| 2 | Claude (base final) | J003 | `provimento` | REPORTAR | Parcialmente provido | R1 |
| 3 | Claude (base final) | J047 | `provimento` | REPORTAR | Parcialmente provido | R1 |
| 4 | Claude (base final) | J059 | `provimento` | REPORTAR | Parcialmente provido | R1 |
| 5 | Claude (base final) | J114 | `provimento` | REPORTAR | Parcialmente provido | R1 |
| 6 | Claude (base final) | J004 | `provimento` | REPORTAR | Liminar indeferida | R2 |
| 7 | Claude (base final) | J008 | `provimento` | REPORTAR | Não conhecido | R3 |
| 8 | Claude (base final) | J054 | `provimento` | REPORTAR | Não conhecido | R5 |
| 9 | Claude (base final) | J013 | `via_processual` | REPORTAR | Impugnação da autorização | R6 |
| 10 | Claude (base final) | J041 | `via_processual` | REPORTAR | Impugnação da autorização | R6 |
| 11 | Claude (base final) | J053 | `via_processual` | Autorização prévia sem polo passivo | Impugnação da autorização | R6 |
| 12 | Claude (base final) | J054 | `via_processual` | Autorização prévia sem polo passivo | Impugnação da autorização | R6 |
| 13 | Claude (base final) | J129 | `via_processual` | Autorização prévia sem polo passivo | Impugnação da autorização | R6 |
| 14 | Claude (base final) | J130 | `via_processual` | Autorização prévia sem polo passivo | Impugnação da autorização | R6 |
| 15 | Claude (base final) | J072 | `via_processual` | REPORTAR | Autorização prévia contra hospital ou médico | R7 |
| 16 | Claude (base final) | J077 | `provimento` | Ordem concedida | Procedente | Ab |
| 17 | Claude (base final) | J124 | `provimento` | Ordem concedida | Liminar deferida | Ac |
| 18 | Claude (base final) | J116 | `provimento` | Ordem concedida | Liminar deferida | Ac |
| 19 | Claude (base final) | J002 | `via_processual` | Menção incidental | Autorização prévia contra operadora de plano | V1 |
| 20 | Claude (base final) | J003 | `via_processual` | Menção incidental | Autorização prévia contra operadora de plano | V1 |
| 21 | Claude (base final) | J047 | `via_processual` | Menção incidental | Demanda indenizatória conexa | V2 |
| 22 | Claude (base final) | J059 | `via_processual` | Menção incidental | Demanda indenizatória conexa | V2 |
| 23 | Claude (base final) | J113 | `via_processual` | Menção incidental | Demanda indenizatória conexa | V2 |
| 24 | Claude (base final) | J114 | `via_processual` | Menção incidental | Demanda indenizatória conexa | V2 |
| 25 | Claude (base final) | J012 | `(linha inteira)` | julgado | documento de contexto | X1 |
| 26 | Claude (base final) | (todos) | `art128_I` | (coluna nova) | preenchida por leitura | A1 |
| 27 | Claude (base final) | (todos) | `efeito_pratico` | (coluna nova) | preenchida por regra | EP |
| 28 | Claude (base final) | J004 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 29 | Claude (base final) | J004 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 30 | Claude (base final) | J005 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 31 | Claude (base final) | J011 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 32 | Claude (base final) | J014 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 33 | Claude (base final) | J014 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 34 | Claude (base final) | J015 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 35 | Claude (base final) | J015 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 36 | Claude (base final) | J016 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 37 | Claude (base final) | J016 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 38 | Claude (base final) | J018 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 39 | Claude (base final) | J018 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 40 | Claude (base final) | J019 | `fundamento_inviabilidade_extrauterina` | Não | Rejeita | RF |
| 41 | Claude (base final) | J019 | `fundamento_dignidade_autonomia` | Não | Rejeita | RF |
| 42 | Claude (base final) | J021 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 43 | Claude (base final) | J021 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 44 | Claude (base final) | J021 | `fundamento_dignidade_autonomia` | Sim | Rejeita | RF |
| 45 | Claude (base final) | J028 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 46 | Claude (base final) | J029 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 47 | Claude (base final) | J029 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 48 | Claude (base final) | J029 | `fundamento_dignidade_autonomia` | Sim | Rejeita | RF |
| 49 | Claude (base final) | J034 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 50 | Claude (base final) | J034 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 51 | Claude (base final) | J034 | `fundamento_dignidade_autonomia` | Não | Rejeita | RF |
| 52 | Claude (base final) | J035 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 53 | Claude (base final) | J035 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 54 | Claude (base final) | J035 | `fundamento_dignidade_autonomia` | Não | Rejeita | RF |
| 55 | Claude (base final) | J037 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 56 | Claude (base final) | J052 | `fundamento_risco_vida_gestante` | Não | Rejeita | RF |
| 57 | Claude (base final) | J056 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 58 | Claude (base final) | J056 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 59 | Claude (base final) | J056 | `fundamento_dignidade_autonomia` | Sim | Rejeita | RF |
| 60 | Claude (base final) | J058 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 61 | Claude (base final) | J058 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 62 | Claude (base final) | J058 | `fundamento_dignidade_autonomia` | Sim | Rejeita | RF |
| 63 | Claude (base final) | J060 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 64 | Claude (base final) | J060 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 65 | Claude (base final) | J065 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 66 | Claude (base final) | J065 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 67 | Claude (base final) | J069 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 68 | Claude (base final) | J069 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 69 | Claude (base final) | J071 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 70 | Claude (base final) | J090 | `fundamento_risco_vida_gestante` | Não | Rejeita | RF |
| 71 | Claude (base final) | J091 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 72 | Claude (base final) | J091 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 73 | Claude (base final) | J092 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 74 | Claude (base final) | J092 | `fundamento_dignidade_autonomia` | Não | Rejeita | RF |
| 75 | Claude (base final) | J095 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 76 | Claude (base final) | J097 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 77 | Claude (base final) | J097 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 78 | Claude (base final) | J097 | `comparacao_com_anencefalia` | Não faz | Distingue | CE |
| 79 | Claude (base final) | J100 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 80 | Claude (base final) | J101 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RP |
| 81 | Claude (base final) | J101 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 82 | Claude (base final) | J102 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RP |
| 83 | Claude (base final) | J102 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 84 | Claude (base final) | J103 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 85 | Claude (base final) | J103 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 86 | Claude (base final) | J104 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 87 | Claude (base final) | J104 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 88 | Claude (base final) | J105 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 89 | Claude (base final) | J107 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 90 | Claude (base final) | J109 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 91 | Claude (base final) | J109 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 92 | Claude (base final) | J111 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 93 | Claude (base final) | J111 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 94 | Claude (base final) | J124 | `comparacao_com_anencefalia` | Não faz | Equipara | CE |
| 95 | Claude (base final) | J126 | `comparacao_com_anencefalia` | Distingue | Equipara | CP |
| 96 | Claude (base final) | J128 | `fundamento_risco_vida_gestante` | Sim | Rejeita | RF |
| 97 | Claude (base final) | J128 | `fundamento_inviabilidade_extrauterina` | Sim | Rejeita | RF |
| 98 | Claude (base final) | (demais) | `fundamento_*` | Sim / Não | Acolhe / Não enfrenta | RA |
| 99 | Gemini (só na comparação) | J002 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 100 | Gemini (só na comparação) | J003 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 101 | Gemini (só na comparação) | J011 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 102 | Gemini (só na comparação) | J021 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 103 | Gemini (só na comparação) | J022 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 104 | Gemini (só na comparação) | J023 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 105 | Gemini (só na comparação) | J024 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 106 | Gemini (só na comparação) | J025 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 107 | Gemini (só na comparação) | J026 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 108 | Gemini (só na comparação) | J026 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 109 | Gemini (só na comparação) | J027 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 110 | Gemini (só na comparação) | J028 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 111 | Gemini (só na comparação) | J029 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 112 | Gemini (só na comparação) | J029 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 113 | Gemini (só na comparação) | J030 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 114 | Gemini (só na comparação) | J030 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 115 | Gemini (só na comparação) | J031 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 116 | Gemini (só na comparação) | J032 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 117 | Gemini (só na comparação) | J033 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 118 | Gemini (só na comparação) | J034 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 119 | Gemini (só na comparação) | J035 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 120 | Gemini (só na comparação) | J036 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 121 | Gemini (só na comparação) | J037 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 122 | Gemini (só na comparação) | J037 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 123 | Gemini (só na comparação) | J040 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 124 | Gemini (só na comparação) | J040 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 125 | Gemini (só na comparação) | J041 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 126 | Gemini (só na comparação) | J042 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 127 | Gemini (só na comparação) | J043 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 128 | Gemini (só na comparação) | J044 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 129 | Gemini (só na comparação) | J045 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 130 | Gemini (só na comparação) | J046 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 131 | Gemini (só na comparação) | J047 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 132 | Gemini (só na comparação) | J048 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 133 | Gemini (só na comparação) | J049 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 134 | Gemini (só na comparação) | J050 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 135 | Gemini (só na comparação) | J051 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 136 | Gemini (só na comparação) | J051 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 137 | Gemini (só na comparação) | J052 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 138 | Gemini (só na comparação) | J053 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 139 | Gemini (só na comparação) | J054 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 140 | Gemini (só na comparação) | J055 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 141 | Gemini (só na comparação) | J056 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 142 | Gemini (só na comparação) | J057 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 143 | Gemini (só na comparação) | J057 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 144 | Gemini (só na comparação) | J058 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 145 | Gemini (só na comparação) | J059 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 146 | Gemini (só na comparação) | J060 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 147 | Gemini (só na comparação) | J061 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 148 | Gemini (só na comparação) | J062 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 149 | Gemini (só na comparação) | J062 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 150 | Gemini (só na comparação) | J064 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 151 | Gemini (só na comparação) | J065 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 152 | Gemini (só na comparação) | J066 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 153 | Gemini (só na comparação) | J067 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 154 | Gemini (só na comparação) | J068 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 155 | Gemini (só na comparação) | J069 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 156 | Gemini (só na comparação) | J070 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 157 | Gemini (só na comparação) | J074 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 158 | Gemini (só na comparação) | J075 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 159 | Gemini (só na comparação) | J076 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 160 | Gemini (só na comparação) | J077 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 161 | Gemini (só na comparação) | J078 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 162 | Gemini (só na comparação) | J079 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 163 | Gemini (só na comparação) | J080 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 164 | Gemini (só na comparação) | J081 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 165 | Gemini (só na comparação) | J084 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 166 | Gemini (só na comparação) | J088 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 167 | Gemini (só na comparação) | J090 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 168 | Gemini (só na comparação) | J099 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 169 | Gemini (só na comparação) | J105 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 170 | Gemini (só na comparação) | J107 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 171 | Gemini (só na comparação) | J112 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 172 | Gemini (só na comparação) | J112 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 173 | Gemini (só na comparação) | J113 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 174 | Gemini (só na comparação) | J114 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 175 | Gemini (só na comparação) | J115 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 176 | Gemini (só na comparação) | J115 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 177 | Gemini (só na comparação) | J116 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 178 | Gemini (só na comparação) | J117 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 179 | Gemini (só na comparação) | J118 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 180 | Gemini (só na comparação) | J119 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 181 | Gemini (só na comparação) | J120 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 182 | Gemini (só na comparação) | J121 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 183 | Gemini (só na comparação) | J122 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 184 | Gemini (só na comparação) | J123 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 185 | Gemini (só na comparação) | J125 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 186 | Gemini (só na comparação) | J126 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 187 | Gemini (só na comparação) | J128 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 188 | Gemini (só na comparação) | J129 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 189 | Gemini (só na comparação) | J129 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 190 | Gemini (só na comparação) | J130 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 191 | Gemini (só na comparação) | J130 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 192 | Gemini (só na comparação) | J137 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 193 | Gemini (só na comparação) | J140 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 194 | Manus (só na comparação) | J003 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 195 | Manus (só na comparação) | J004 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 196 | Manus (só na comparação) | J013 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 197 | Manus (só na comparação) | J018 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 198 | Manus (só na comparação) | J021 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 199 | Manus (só na comparação) | J024 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 200 | Manus (só na comparação) | J026 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 201 | Manus (só na comparação) | J029 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 202 | Manus (só na comparação) | J030 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 203 | Manus (só na comparação) | J033 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 204 | Manus (só na comparação) | J037 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 205 | Manus (só na comparação) | J039 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 206 | Manus (só na comparação) | J040 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 207 | Manus (só na comparação) | J041 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 208 | Manus (só na comparação) | J043 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 209 | Manus (só na comparação) | J044 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 210 | Manus (só na comparação) | J044 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 211 | Manus (só na comparação) | J045 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 212 | Manus (só na comparação) | J045 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 213 | Manus (só na comparação) | J046 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 214 | Manus (só na comparação) | J046 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 215 | Manus (só na comparação) | J047 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 216 | Manus (só na comparação) | J048 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 217 | Manus (só na comparação) | J051 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 218 | Manus (só na comparação) | J052 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 219 | Manus (só na comparação) | J055 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 220 | Manus (só na comparação) | J057 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 221 | Manus (só na comparação) | J062 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 222 | Manus (só na comparação) | J064 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 223 | Manus (só na comparação) | J066 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 224 | Manus (só na comparação) | J067 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 225 | Manus (só na comparação) | J068 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 226 | Manus (só na comparação) | J084 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 227 | Manus (só na comparação) | J088 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 228 | Manus (só na comparação) | J090 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 229 | Manus (só na comparação) | J099 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 230 | Manus (só na comparação) | J105 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 231 | Manus (só na comparação) | J107 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 232 | Manus (só na comparação) | J112 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 233 | Manus (só na comparação) | J115 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 234 | Manus (só na comparação) | J117 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 235 | Manus (só na comparação) | J118 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 236 | Manus (só na comparação) | J119 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 237 | Manus (só na comparação) | J120 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 238 | Manus (só na comparação) | J121 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 239 | Manus (só na comparação) | J122 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 240 | Manus (só na comparação) | J123 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 241 | Manus (só na comparação) | J125 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 242 | Manus (só na comparação) | J125 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 243 | Manus (só na comparação) | J126 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 244 | Manus (só na comparação) | J126 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 245 | Manus (só na comparação) | J128 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 246 | Manus (só na comparação) | J128 | `via_processual` | Autorização prévia contra Estado | Autorização prévia sem polo passivo | I2 |
| 247 | Manus (só na comparação) | J129 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 248 | Manus (só na comparação) | J130 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 249 | Manus (só na comparação) | J132 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 250 | Manus (só na comparação) | J133 | `via_processual` | Autorização prévia contra Estado | Autorização prévia sem polo passivo | I2 |
| 251 | Manus (só na comparação) | J134 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 252 | Manus (só na comparação) | J137 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
| 253 | Manus (só na comparação) | J137 | `via_processual` | Autorização prévia contra o Estado | Autorização prévia sem polo passivo | I2 |
| 254 | Manus (só na comparação) | J140 | `momento_idade_gestacional` | Não especificado | Não consta | I1 |
