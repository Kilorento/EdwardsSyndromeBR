# PROMPT — EXTRAÇÃO DE JULGADOS, BLOCO A (valores fechados e literais) · Lote {LOTE}

Você é um dos três extratores independentes de uma pesquisa acadêmica sobre como os tribunais brasileiros decidem pedidos de interrupção da gestação de feto com trissomia do cromossomo 18 (síndrome de Edwards, T18). Abaixo deste prompt há **{N} documentos**, separados por linhas `===== DOCUMENTO N (ref. Jxxx) — arquivo =====`. Cada documento corresponde a um julgado (às vezes com um anexo, como voto vencido, no mesmo bloco).

## Regras invioláveis

1. **Decida apenas pelo documento fornecido.** Não use conhecimento externo sobre o caso, o tribunal ou os envolvidos.
2. **Nunca invente.** Se a informação não está no texto, use o código de ausência correto (abaixo).
3. **Não use código, script nem busca por palavra-chave.** Leia e entenda o documento.
4. **Leia cada documento inteiro**, sem truncar.
5. **Justifique cada campo não trivial com trecho literal entre aspas.** Sem trecho, o campo é ausente.
6. **Processe todos os documentos.** Termine com a linha `Lote {LOTE}: X documentos lidos`.
7. **Não altere o vocabulário fechado.** Se o valor não couber, escreva `REPORTAR` no campo e explique na justificativa.
8. As primeiras linhas de alguns documentos (tabela Campo/Valor, Classe, Data de liberação) são metadados do sistema do tribunal. Use-os como contexto. Quando o corpo do documento contradisser os metadados, prevalece o corpo; registre a divergência em `observacao`.
9. Se o número do processo no nome do arquivo não coincidir com o do texto, registre o número **do texto** e aponte a divergência em `observacao`. Se o arquivo contiver o texto de **outro processo**, não extraia esse outro processo: marque `forma_do_texto = Apenas referência`, preencha os campos de conteúdo com `Não acessível` e explique em `observacao`.
10. Se um bloco contiver mais de um julgado (ex.: acórdão e embargos), extraia o julgado principal e registre o outro em `observacao`.
11. **Não copie dados pessoais** (nome de parte, RG, CPF, endereço, data de nascimento) para nenhum campo. Escreva "a gestante", "o casal" etc. Nomes de magistrados podem ser copiados.

## Códigos de ausência — `vazio` nunca é resposta

| Código | Uso |
|---|---|
| `Não aplicável` | O campo não existe nesse tipo de processo (ex.: `unanimidade` em sentença; `idade_gestacional_semanas` quando não há pedido de interrupção) |
| `Não consta` | O documento foi lido por inteiro e não traz a informação |
| `Não acessível` | Só cabe quando `forma_do_texto` for `Apenas ementa` ou `Apenas referência` (o texto integral não está disponível) |

## Variáveis (preencha todas, na ordem)

| Variável | Valores / regra |
|---|---|
| `doc` | número do DOCUMENTO no lote |
| `ref` | o código `Jxxx` que aparece no cabeçalho do documento |
| `uf` | sigla de 2 letras (`—` para STJ/STF) |
| `tribunal` | `TJSP`, `TJRS`, `STJ`… |
| `comarca` | onde o processo correu; em acórdão, a comarca **de origem**; `Não consta` se o documento não disser |
| `n_processo` | número CNJ ou interno, conforme o texto |
| `padrao_numeracao` | `CNJ` · `Interna` · `Ambas` |
| `n_processo_alternativo` | a outra numeração quando `Ambas` (inclui número antigo do tribunal ou "Controle nº"); senão `Não aplicável` |
| `n_processo_origem` | processo de origem, quando o documento indicar o número |
| `forma_do_texto` | `Inteiro teor colado no espelho` · `PDF de inteiro teor` · `Apenas ementa` · `Apenas referência` |
| `instancia` | `1º grau` · `2º grau` · `Tribunal Superior` — determinar pelo documento |
| `tipo_pronunciamento` | `Sentença` · `Acórdão` · `Decisão monocrática` · `Decisão interlocutória` |
| `orgao_julgador` | 1º grau: `2ª Vara Cível da Comarca de Jaru (TJRO)`. 2º grau: `1ª Câmara Cível do Tribunal de Justiça do Estado de Alagoas (TJAL)` |
| `relator` | nome do magistrado (o juiz que decide, no 1º grau) |
| `tratamento_relator` | `Desembargador` · `Desembargadora` · `Juiz` · `Juíza` · `Ministro` · `Ministra` · `Não consta` — **copiar do documento**. Abreviações flexionadas valem (`Des.` → Desembargador; `Des.ª`/`Desa.` → Desembargadora). Formas não flexionadas (`Juiz(a) de Direito: Dr(a).`) ou só `Relator`/`Relatora` → `Não consta` |
| `genero_relator_declarado` | `Masculino` · `Feminino` · `Não consta` — derivado **só da flexão do tratamento**, nunca do nome |
| `redator_designado` | nome, quando o relator fica vencido; senão `Não aplicável` |
| `tratamento_redator` | como `tratamento_relator` |
| `unanimidade` | `Unânime` · `Por maioria` · `Monocrática` · `Não consta` (`Não aplicável` em sentença) |
| `votos_separados` | `Nenhum` · `Voto vencido` · `Voto-vista` · `Declaração de voto` · `Voto divergente` (combináveis com `;`). Declaração anunciada no dispositivo conta, mesmo se o texto não vier |
| `data_inicial` | `DD/MM/AAAA` da petição inicial ou do recurso, ou `Não consta` |
| `data_julgamento` | `DD/MM/AAAA` ou `Não consta` |
| `data_publicacao` | `DD/MM/AAAA` ou `Não consta`. "Data de liberação nos autos" e data de assinatura **não** são publicação; data do D.E./DJe é |
| `provimento` | 1º grau: `Procedente` · `Parcialmente procedente` · `Improcedente` · `Extinto sem resolução de mérito` · `Homologado` · `Liminar deferida` · `Liminar indeferida`. Recursal: `Provido` · `Parcialmente provido` · `Desprovido` · `Não conhecido` · `Prejudicado`. HC e MS: `Ordem concedida` · `Ordem denegada`. Resultado duplo ou fora da lista → `REPORTAR` |
| `enfrenta_tipificacao` | `Sim` · `Não` — `Sim` quando a decisão raciocina sobre tipicidade, atipicidade, ADPF 54 por analogia, arts. 124/126/128 do CP, excludentes de ilicitude ou de culpabilidade ou inviabilidade de vida extrauterina **como razão de decidir** |
| `via_processual` | `Autorização prévia contra o Estado` · `Autorização prévia contra operadora de plano` · `Autorização prévia sem polo passivo` · `Ação penal` · `Demanda indenizatória conexa` · `Menção incidental` |
| `condicao_fetal` | `T18` · `T13 (Patau)` · `Anencefalia` · `Outra` · `Múltipla` · `Não consta` |
| `forma_citogenetica` | `Trissomia completa` (inclui "trissomia livre", 47,XX,+18 ou 47,XY,+18) · `Mosaico` · `Parcial` · `Não consta`; `Não aplicável` se a condição não for trissomia |
| `falso_positivo` | `Sim` · `Não` — `Sim` quando o documento **não** trata de gestação com T18 em discussão de interrupção (T18 só citada, outra condição, ou T18 presente mas objeto alheio à interrupção, como indenização por erro de diagnóstico ou licença-maternidade). Cobertura ou indenização ligadas à própria interrupção de gestação com T18 → `Não` |
| `motivo_falso_positivo` | texto curto (`Síndrome de Patau; T18 apenas citada (precedente)`, `Anencefalia`…); `Não aplicável` se não houver |
| `segredo_de_justica` | `Sim` · `Não` · `Não consta` — só `Sim` quando o **documento** declarar ou decretar sigilo |
| `idade_gestacional_semanas` | número inteiro (meses não se convertem: use `Não consta` e explique) |
| `momento_idade_gestacional` | `Diagnóstico` · `Pedido` · `Julgamento` · `Não especificado` |
| `faixa_etaria_gestante` | `≤19` · `20-29` · `30-34` · `35-39` · `≥40` · `Não consta` |
| `houve_parto_antes_do_fim` | `Sim` · `Não` · `Não consta` |
| `perda_de_objeto` | `Sim` · `Não` |
| `situacao_vital_na_decisao` | `Gestação em curso` · `Nascida viva` · `Óbito fetal` (inclui interrupção já realizada) · `Óbito após nascimento` · `Não consta` |
| `fundamento_risco_vida_gestante` | `Sim` · `Não` — `Sim` quando o julgador **examina o art. 128, I, do CP** como razão de decidir, para acolher ou para rejeitar; risco mencionado sem o artigo → `Não` (registre em `observacao`) |
| `fundamento_inviabilidade_extrauterina` | `Sim` · `Não` — inviabilidade de vida fora do útero enfrentada como razão de decidir, para acolher ou para rejeitar |
| `fundamento_dignidade_autonomia` | `Sim` · `Não` — dignidade, autonomia ou saúde da gestante enfrentada como razão de decidir, para acolher ou para rejeitar |
| `comparacao_com_anencefalia` | `Não faz` · `Equipara` · `Distingue` |
| `cita_adpf54` | `Sim` · `Não` — `Sim` se o texto do julgador (ou parecer que ele adota) menciona a ADPF 54 ou a decisão do STF sobre anencefalia, mesmo sem número; não basta a ADPF aparecer só dentro de ementa de precedente transcrita |
| `cita_hc_932495` | `Sim` · `Não` |
| `precedentes_citados` | julgados citados pelo julgador ou em trecho que ele adota como razão de decidir, separados por `;` (ex.: `TJSP HC 0045924-20.2012.8.26.0000; ADPF 54`). Ignore precedentes citados só nas alegações das partes |
| `observacao` | divergências, ambiguidades, o que faltou; **o sentido** (acolhe/rejeita) de cada `fundamento_*` marcado `Sim`; menção a outro processo do mesmo caso |

Nos campos `fundamento_*`, marque `Sim` só quando o fundamento for **razão de decidir do julgador**, e não mera alegação de parte ou transcrição de precedente. O trecho literal tem de demonstrar isso.

## Formato da resposta

**Parte 1:** um bloco de código CSV, delimitado por vírgula, com cabeçalho na ordem da tabela acima e uma linha por documento. Ponha entre aspas duplas todo campo que contenha vírgula.

**Parte 2:** para cada documento, uma lista `campo: "trecho literal"` com todos os campos não triviais.

**Parte 3 — processos sobre T18 citados:** uma tabela com os processos **sobre gestação com T18** que o documento cita **com número** (precedente, processo de origem, processo conexo), com as colunas `doc`, `n_processo_citado`, `tribunal`, `forma` (`Precedente citado` · `Processo de origem` · `Processo conexo`), `o_que_o_documento_informa` (trecho literal). Se não houver, escreva `Nenhum`.

**Parte 4:** a linha `Lote {LOTE}: X documentos lidos`.

Registre ao final o **nome e a versão completa do modelo**, como a interface os mostra, e a data de execução.

---
