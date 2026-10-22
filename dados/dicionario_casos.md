# casos.csv: dicionário e regras (15/10/2026, versão 2)

**Unidade.** Um caso é uma gestação. Os julgados que tratam da mesma gestação formam um único caso, mesmo quando estão em processos, classes ou tribunais diferentes. Duas gestações da mesma mulher são dois casos, ligados entre si por `caso_relacionado`.

**Ligação.** Cada julgado pertence a um só caso. A ligação está na coluna `id_caso`, a segunda de `julgados.csv`; as demais colunas dessa planilha não foram alteradas. Citação de um caso por outro não é ligação: é rede de precedentes e fica fora desta tabela.

**Totais.**
- 123 casos para 139 julgados.
- 13 casos têm mais de um julgado, somando 29 julgados.
- 78 casos estão no escopo: T18 em gestação e não falso positivo.

**Fonte.** O arquivo é gerado por `auditoria/scripts/build_casos.py` a partir da `julgados.csv` definitiva. As ligações e as exceções manuais estão escritas no próprio script.

**Limite.** A planilha de casos não cria variável nova. Tudo nela vem de `julgados.csv`, por cópia ou por agregação dos julgados do caso. A discussão médica fica fora desta base.

## Colunas

| Coluna | Conteúdo | Valores e regra |
|---|---|---|
| `id_caso` | Identificador | C001–C123, na ordem do primeiro julgado |
| `julgados` | Julgados do caso | Em ordem cronológica da trajetória |
| `n_julgados` | Quantidade de julgados | |
| `no_escopo` | O caso está no escopo? | `Sim` se algum julgado do caso tem `falso_positivo = Não`. `Não` se todos são falsos positivos. `Não acessível` nos casos J009 e J070 |
| `falso_positivo`, `motivo_falso_positivo` | Classificação de falso positivo e o motivo | Copiados dos julgados do caso; valores distintos separados por "; ". Nenhum caso é misto |
| `tribunais`, `uf` | Tribunais e UFs | Na ordem da trajetória |
| `comarca_origem` | Comarca | A primeira informada no caso |
| `processos` | Números dos processos | Todos os números dos julgados. Origem ou processo conexo fora da busca aparece com o código de `processos_referenciados.csv`, como "(R008)" |
| `condicao_fetal`, `forma_citogenetica` | Diagnóstico | O valor mais informativo entre os julgados do caso |
| `ig_semanas` | Idade gestacional, em semanas | Só o número: a primeira idade gestacional numérica da trajetória. `Não consta` quando nenhum julgado informa |
| `ig_momento` | Momento da medida de `ig_semanas` | `Pedido`, `Diagnóstico`, `Julgamento`, `Não especificado` ou `Não consta`. Copiado de `momento_idade_gestacional` do mesmo julgado que deu a `ig_semanas` |
| `instancias_percorridas` | Instâncias | Por exemplo, "1º grau → 2º grau → STJ" |
| `data_pedido` | Data do pedido | A mais antiga `data_inicial` do caso |
| `data_primeira_decisao`, `data_ultima_decisao` | Datas de julgamento | Data do primeiro e do último julgado da trajetória. `Não consta` quando o próprio julgado não traz a data. Se o último julgado não traz a data de julgamento, `data_ultima_decisao` recebe a sua `data_publicacao`, e isso fica anotado em `observacao` (C052, C055, C056, C058). Quando não há nenhuma das duas datas, a célula fica `Não consta`, também com anotação (C005, C012, C016, C040) |
| `dias_ate_decisao_util` | Dias até a decisão útil | Da `data_pedido` até o julgamento do `julgado_decisivo`. Calculado só quando o desfecho vem do próprio julgado e as duas datas existem. São 9 valores numéricos, conferidos em 15/10/2026. Quando houve liminar antes do acórdão, o prazo real até a autorização foi menor |
| `desfecho_final` | Resultado do caso | `Autorizado`, `Negado`, `Sem decisão útil`, `Não decide a autorização` ou `Não acessível` (regra abaixo) |
| `julgado_decisivo` | Julgado de onde vem o desfecho | |
| `fonte_do_desfecho` | Onde está a decisão que prevaleceu | `Próprio julgado`, `Decisão relatada no julgado` (liminar ou tutela) ou `Decisão de origem relatada no julgado (fora do corpus)` |
| `fonte_dos_fundamentos` | De onde vêm as colunas copiadas abaixo | `Julgado decisivo`, quando `fonte_do_desfecho = Próprio julgado`. `Julgado que relata a decisão`, quando o desfecho vem de liminar, tutela ou decisão de origem relatada. `Não aplicável`, quando o desfecho é `Não decide a autorização`, `Sem decisão útil` ou `Não acessível` |
| `instancia`, `orgao_julgador`, `via_processual`, `art128_I`, `fundamento_risco_vida_gestante`, `fundamento_inviabilidade_extrauterina`, `fundamento_dignidade_autonomia`, `comparacao_com_anencefalia`, `cita_adpf54`, `cita_hc_932495`, `forma_do_texto`, `perda_de_objeto` | Colunas copiadas do `julgado_decisivo` | Cópia exata das colunas de mesmo nome em `julgados.csv`, com o mesmo vocabulário, feita pelo script. São `Não aplicável` quando o desfecho é `Não decide a autorização` ou `Sem decisão útil`, e `Não acessível` quando o desfecho é `Não acessível` |
| `houve_reforma` | A decisão final mudou o resultado inicial? | `Sim (negado → autorizado)`, `Sim (extinto → autorizado)`, `Sim (autorizado → negado)`, `Não`, `Não consta` (a origem não é informada) ou `Não aplicável` (caso com uma única decisão de 1º grau, ou sem desfecho) |
| `gestacao_encerrada_antes_da_decisao_final` | A gestação terminou antes da última decisão? | `Sim — interrupção`, `Sim — parto ou óbito fetal`, `Não consta` ou `Não aplicável` |
| `impugnado_por` | Quem impugnou a autorização | Ministério Público ou terceiros; `Nenhuma no corpus` quando não há impugnação |
| `caso_relacionado` | Caso ligado | Recorrência da mesma gestante |
| `questionamentos` | Anomalias de busca ou de acesso | Com o julgado de origem entre colchetes. Exemplos: só ementa, chave que não casou, origem fora da busca, dois acórdãos para um julgamento |
| `observacao` | Trajetória do caso | Em casos com mais de um julgado e em desfechos tirados de decisão relatada |

## Regra do desfecho

1. **Vale a última decisão do caso com efeito prático.** `efeito_pratico` igual a `Autoriza` vira `Autorizado`; igual a `Nega` vira `Negado`. "Prejudicado" e "não conhecido" não contam.
2. **Quando nenhum julgado do caso tem efeito prático**, vale a decisão que o próprio julgado relata:
   - Liminar ou tutela concedida no recurso: J031 e J121.
   - Decisão de origem fora do corpus: J049, J050, J057, J061, J119 e J131, que negaram, e a sentença do DIPO em C113, que autorizou.
   - A extinção sem mérito na origem conta como `Negado` (J049).
3. **`Não decide a autorização`** marca os casos que discutem cobertura ou indenização e não o pedido de interrupção: J001, J071, J073, J084 e J139, além dos falsos positivos dessa natureza.
4. **`Sem decisão útil`** marca os casos em que nenhuma instância decidiu o mérito. Só o C100 está nessa situação: dois HCs não conhecidos.

## Ligações manuais

| Caso | Julgados | Base da ligação |
|---|---|---|
| C002 | J002, J003 | Julgamento conjunto de processos conexos |
| C004 | J005–J008 | O J006 registra a liminar no processo contra o Estado (J005) |
| C008 | J046, J013 | Mesma paciente, vara e parecer da FIOCRUZ. O J012, retirado da base, está em documentos_de_contexto.csv |
| C009 | J069, J014, J015 | O STJ ataca o acórdão do TJSC; o número de origem coincide |
| C010 | J016, J017 | Mesmo HC no STJ |
| C012 | J019, J020 | Mesmo número |
| C044 | J054, J053 | Mesmo número |
| C056 | J066, J067 | Ementas idênticas, mesmo relator e mesma data (cautelar e principal) |
| C088 | J100, J120 | O acórdão identifica a sentença e a gestante |
| C090 | J102, J121 | O acórdão identifica a sentença e a gestante |
| C100 | J122, J112 | O J112 não conhece o pedido por reiteração do HC 2078297-02.2014 |
| C101 | J114, J113 | Mesmo processo (apelação e embargos) |
| C113 | J130, J129 | Mesmo casal e mesma sentença do DIPO |
| C014 ↔ C015 | J022 e J023 | Recorrência: o J022 registra a autorização anterior à mesma requerente |

## Regra de `fonte_dos_fundamentos`

As colunas copiadas descrevem **o julgado de onde vem o desfecho**, não o caso inteiro. São três situações.

1. **`Julgado decisivo`:** o desfecho é a decisão do próprio julgado. As colunas mostram os fundamentos dessa decisão. São 63 casos no escopo.
2. **`Julgado que relata a decisão`:** o desfecho vem de liminar, tutela ou decisão de origem que o julgado só relata. Os fundamentos copiados são os do julgado que relata, quase sempre um "prejudicado" ou um "não conhecido". **Não são os fundamentos da decisão que prevaleceu.** São 9 casos: C023, C040, C041, C047, C051, C090, C106, C113 e C114. Nos 9, os três `fundamento_*` estão `Não enfrenta`.
3. **`Não aplicável`:** o caso não tem desfecho de autorização.

**Para cruzar desfecho com fundamento, filtre `fonte_dos_fundamentos = Julgado decisivo`.**
