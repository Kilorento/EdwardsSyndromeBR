# Dicionário de variáveis — `dados/julgados.csv`

Uma linha por julgado (decisão). Os campos fechados só admitem os valores listados. `vazio` nunca é resposta.

## Códigos de ausência

| Código | Significado |
|---|---|
| `Não aplicável` | O campo não existe nesse tipo de processo. Ex.: `unanimidade` em sentença; `idade_gestacional_semanas` quando não há pedido de interrupção |
| `Não consta` | O documento foi lido por inteiro e não traz a informação. Isso é um achado sobre o registro do tribunal |
| `Não acessível` | Só existe ementa ou referência; o texto integral não estava disponível. É um limite da pesquisa |

## Identificação e busca

| Variável | Valores / regra |
|---|---|
| `id_julgado` | `J001`–`J140`. O J012 não está aqui: foi movido para `documentos_de_contexto.csv` |
| `id_caso` | Caso (gestação) a que o julgado pertence: `C001`–`C123`. Ver `dicionario_casos.md` |
| `regiao` | `N` · `NE` · `CO` · `SE` · `S` · `—` (tribunais superiores) |
| `uf` | Sigla do estado; `—` para o STJ |
| `tribunal` | `TJSP`, `TJRS`, `STJ`… |
| `comarca` | Onde o processo correu. Em acórdão, é a comarca de origem |
| `n_processo` | Número conforme o texto do documento |
| `padrao_numeracao` | `CNJ` · `Interna` · `Ambas` |
| `n_processo_alternativo` | A outra numeração quando `Ambas`; senão `Não aplicável` |
| `n_processo_origem` | Processo de origem, quando o documento indica o número |
| `chave_busca` | Chave(s) da pesquisa pela(s) qual(is) o julgado retornou |
| `forma_do_texto` | `PDF de inteiro teor` · `Inteiro teor colado no espelho` · `Apenas ementa` · `Apenas referência` |
| `arquivos_fonte` | Arquivo(s) do corpus |
| `link_acesso` | Página de consulta de jurisprudência do tribunal |
| `data_busca` | Data da consulta (DD/MM/AAAA) |

## Órgão e julgamento

| Variável | Valores / regra |
|---|---|
| `instancia` | `1º grau` · `2º grau` · `Tribunal Superior` |
| `tipo_pronunciamento` | `Sentença` · `Acórdão` · `Decisão monocrática` · `Decisão interlocutória` |
| `orgao_julgador` | Vara ou câmara, por extenso, com o tribunal |
| `relator` | Nome do magistrado (no 1º grau, o juiz que decide) |
| `tratamento_relator` | `Desembargador` · `Desembargadora` · `Juiz` · `Juíza` · `Ministro` · `Ministra` · `Não consta`. Copiado do documento. Formas não flexionadas ("Juiz(a) de Direito", "Relator" sem "Des.") ficam `Não consta` |
| `genero_relator_declarado` | `Masculino` · `Feminino` · `Não consta`. Deriva **só** da flexão do tratamento, nunca do nome |
| `redator_designado`, `tratamento_redator` | Quando o relator fica vencido; senão `Não aplicável` |
| `unanimidade` | `Unânime` · `Por maioria` · `Monocrática` · `Não consta` (`Não aplicável` em sentença) |
| `votos_separados` | `Nenhum` · `Voto vencido` · `Voto-vista` · `Declaração de voto` · `Voto divergente`. Os valores podem ser combinados com `;` |
| `tipo_acao` | Texto livre (Bloco B1): classe processual e natureza do pedido |
| `data_inicial`, `data_julgamento`, `data_publicacao` | `DD/MM/AAAA`. A "data de liberação nos autos" e a data de assinatura **não** são publicação; a data do D.E./DJe é |

## Resultado

| Variável | Valores / regra |
|---|---|
| `provimento` | Rótulo processual do dispositivo. **1º grau:** `Procedente` · `Parcialmente procedente` · `Improcedente` · `Extinto sem resolução de mérito` · `Homologado` · `Liminar deferida` · `Liminar indeferida`. **Recursal:** `Provido` · `Parcialmente provido` · `Desprovido` · `Não conhecido` · `Prejudicado`. **HC e MS:** `Ordem concedida` · `Ordem denegada`. Convenções da arbitragem: resultado duplo → `Parcialmente provido`; inadmissão de REsp e competência declinada → `Não conhecido`; acórdão que concede liminar ou a ordem liminarmente → `Liminar deferida`; indeferimento por decisão quando o pedido liminar é o próprio objeto → `Liminar indeferida` |
| `efeito_pratico` | **Efeito da decisão sobre a interrupção**, independentemente do rótulo: `Autoriza` · `Nega` · `Sem efeito` (prejudicado, não conhecido, homologado, extinto sem alvará) · `Não aplicável` (a decisão não trata de autorizar a interrupção: plano de saúde, indenização, menção incidental). Na `Impugnação da autorização`, o sentido se inverte: ordem denegada ou pedido improcedente **mantém** a autorização (`Autoriza`). A sentença extinta sem mérito que vale como alvará (J103, J104, J109, J111) é `Autoriza`, e a liminar deferida também. **Use esta coluna para medir taxas de autorização** |
| `perda_de_objeto` | `Sim` · `Não` |
| `houve_parto_antes_do_fim` | `Sim` · `Não` · `Não consta` |
| `situacao_vital_na_decisao` | `Gestação em curso` · `Nascida viva` · `Óbito fetal` (inclui interrupção já realizada) · `Óbito após nascimento` · `Não consta` |

## Objeto e caso

| Variável | Valores / regra |
|---|---|
| `via_processual` | `Autorização prévia sem polo passivo` (alvará, jurisdição voluntária, HC ou MS contra ato judicial) · `Autorização prévia contra o Estado` · `Autorização prévia contra operadora de plano` · `Autorização prévia contra hospital ou médico` · `Impugnação da autorização` (quem aciona o tribunal busca **impedir** a interrupção: MP ou terceiros em favor do nascituro) · `Ação penal` · `Demanda indenizatória conexa` · `Menção incidental` |
| `enfrenta_tipificacao` | `Sim` quando a decisão raciocina sobre tipicidade, atipicidade, ADPF 54, arts. 124/126/128 do CP, excludentes ou inviabilidade **como razão de decidir** |
| `condicao_fetal` | `T18` · `T13 (Patau)` · `Anencefalia` · `Outra` · `Múltipla` · `Não consta` |
| `forma_citogenetica` | `Trissomia completa` (inclui "trissomia livre", 47,XX,+18) · `Mosaico` · `Parcial` · `Não consta`; `Não aplicável` se a condição não for trissomia |
| `falso_positivo` | `Sim` quando o documento **não** trata de gestação com T18 em discussão de interrupção: T18 só citada, outra condição, ou T18 presente com objeto alheio à interrupção. Cobertura ou indenização ligadas à própria interrupção são `Não` |
| `motivo_falso_positivo` | Texto curto; `Não aplicável` se não for falso positivo |
| `segredo_de_justica` | `Sim` só quando o documento declara sigilo; senão `Não consta` |
| `idade_gestacional_semanas` | Número inteiro. Intervalo ("23/24 semanas") → limite inferior. Meses não são convertidos (`Não consta`) |
| `momento_idade_gestacional` | `Diagnóstico` · `Pedido` · `Julgamento` · `Não especificado` (há IG, mas sem momento). Sem IG → `Não consta` |
| `faixa_etaria_gestante` | `≤19` · `20-29` · `30-34` · `35-39` · `≥40` · `Não consta` |

## Fundamentos

Marcados só quando são **razão de decidir do julgador** (ou de parecer que ele adota). Não contam alegação de parte nem precedente transcrito.

| Variável | Valores / regra |
|---|---|
| `fundamento_risco_vida_gestante` | `Acolhe` · `Rejeita` · `Não enfrenta`. **Acolhe:** o julgador fundamenta no risco à vida da gestante, ou invoca o art. 128, I (direto ou por analogia), ainda que para risco à saúde. **Rejeita:** examina e afasta. Quando o julgador remete o risco ao médico, o valor acompanha o resultado: nega por falta de interesse de agir (J101, J102) → `Rejeita`; a sentença vale como alvará (J103, J104, J109, J111) → `Acolhe`. Nos seis, `art128_I = Remetido ao médico`. Risco à saúde citado sem o artigo → `Não enfrenta` |
| `art128_I` | **Como o julgador tratou o art. 128, I, do CP:** `Aplicado` (fundamento da decisão, inclusive ampliado ou por analogia) · `Afastado` (examinado e declarado inaplicável) · `Remetido ao médico` (o julgador diz que o aborto necessário dispensa autorização judicial e deixa a avaliação do risco ao médico) · `Risco discutido sem o artigo` (o risco à gestante é razão de decidir, mas o artigo não é citado) · `Mencionado sem exame` (o artigo aparece só em exposição genérica, em alegação de parte ou em precedente transcrito) · `Não mencionado` · `Não acessível` |
| `fundamento_inviabilidade_extrauterina` | `Acolhe` · `Rejeita` · `Não enfrenta` |
| `fundamento_dignidade_autonomia` | `Acolhe` · `Rejeita` · `Não enfrenta`. Dignidade, autonomia ou saúde da gestante. `Rejeita` inclui ponderar o sofrimento da gestante e fazer prevalecer a vida do feto |
| `comparacao_com_anencefalia` | `Equipara`: o julgado aplica a ADPF 54 (ou sua razão de decidir) **por analogia direta**. `Distingue`: o julgado examina a analogia e a **recusa**. `Não faz`: não há analogia, e citar a anencefalia ou agrupá-la com a T18 não basta. Quando o próprio feto é anencéfalo, a ADPF se aplica diretamente → `Não faz` |
| `cita_adpf54` | `Sim` se o julgador menciona a ADPF 54 ou a decisão do STF sobre anencefalia, mesmo sem número. Não conta a ADPF que aparece só em ementa transcrita |
| `cita_hc_932495` | `Sim` · `Não` (STJ, HC 932.495/SC, 06/08/2024) |
| `precedentes_citados` | Julgados citados pelo julgador, separados por `;` |

## Texto livre

| Variável | Conteúdo |
|---|---|
| `resumo_do_julgado` | Resumo do caso e da decisão (Bloco B1, Claude; verificado no Bloco B2 pelo Gemini). Sem dados pessoais |
| `observacao` | Divergências, ambiguidades, o sentido dos fundamentos, ligações com outros julgados do mesmo processo e anotações da arbitragem |

---

## Outras tabelas

**`processos_referenciados.csv`**

| Coluna | Conteúdo |
|---|---|
| `id_referencia` | `R001`–`R015` |
| `tribunal`, `n_processo` | Identificação do processo |
| `citado_em` | Julgados que o citam |
| `forma_da_referencia` | `Precedente citado` · `Processo de origem` · `Processo conexo` |
| `o_que_o_julgado_citante_informa` | O que o julgado citante diz sobre o processo |
| `observacao` | Anotações |

**`documentos_de_contexto.csv`:** coluna `ligado_a` mais as mesmas colunas da extração original.

**`alteracoes_por_celula.csv`:** ver `auditoria/ALTERACOES.md`.
