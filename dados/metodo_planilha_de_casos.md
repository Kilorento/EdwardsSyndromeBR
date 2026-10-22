# Planilha de casos (`casos.csv`): método de construção

Este documento descreve como foi construída a planilha `casos.csv` e o que mudou em `julgados.csv`. Cobre as decisões tomadas, as regras aplicadas a cada coluna, as intervenções manuais e as limitações. O objetivo é que qualquer pessoa consiga reproduzir o resultado e auditar cada valor.

- **Data de construção:** 15/10/2026
- **Entrada:** `julgados.csv`, versão definitiva fixada pelo pesquisador em 14/10/2026 (139 julgados, J001–J140; o J012 foi retirado e está em `documentos_de_contexto.csv`), e `processos_referenciados.csv` (R001–R015)
- **Saídas:**
  - `casos.csv`
  - `julgados.csv`, acrescida da coluna `id_caso`
  - `dicionario_casos.md`
- **Script:** `auditoria/scripts/build_casos.py`

---

## 1. Por que uma planilha de casos

A unidade de `julgados.csv` é o **pronunciamento judicial**. Muitas perguntas da pesquisa, porém, são sobre a **pessoa e a gestação**:

- a gestante obteve a autorização?
- quanto tempo levou?
- a primeira decisão foi revertida?
- a gestação terminou antes de o Judiciário decidir?

Uma mesma gestação pode gerar vários julgados: liminar, sentença, apelação, habeas corpus no STJ, ação contra o plano de saúde. Contar julgados como se fossem casos superestima o número de pedidos e distorce taxas de autorização. A planilha de casos corrige isso.

## 2. Decisões de desenho

O pesquisador aprovou as três decisões abaixo antes da construção, em 15/10/2026.

| Decisão | Escolha | Alternativa descartada | Razão |
|---|---|---|---|
| Unidade do caso | **Gestação** | Processo | É a gestação que responde se a gestante conseguiu. Uma mesma gestação pode tramitar em mais de um processo (por exemplo, um pedido contra o Estado e uma ação contra o plano de saúde). |
| Falsos positivos | **Entram**, marcados `no_escopo = Não` | Só os casos no escopo | Assim todo julgado tem caso e a análise só precisa filtrar. Nada some da base. |
| Ligação entre as tabelas | **Coluna `id_caso` em `julgados.csv`** | Só a lista `julgados` dentro de `casos.csv` | Torna o cruzamento direto (relação 1:N). É a única alteração em `julgados.csv`. |

**Regras complementares:**

- **Uma gestação, um caso.** Duas gestações da mesma mulher são dois casos, ligados pela coluna `caso_relacionado`.
- **Cada julgado pertence a exatamente um caso.**
- **Citação não é ligação.** Quando um julgado cita outro, isso é rede de precedentes e não entra em `casos.csv`. Exemplo: o J090 (TJSP) cita o J001 (TJDFT), e os dois continuam em casos separados.

## 3. Etapas

### 3.1. Identificação dos casos com mais de um julgado

As ligações foram identificadas durante a **leitura integral dos documentos** na extração. Cada uma foi anotada na coluna `observacao` do julgado com as marcas "MESMO CASO", "MESMO PROCESSO", "ORIGEM" ou "ligar na planilha de casos". Depois foram conferidas contra:

1. a coincidência de número de processo;
2. o `n_processo_origem` de um julgado coincidindo com o `n_processo` de outro;
3. a identificação, no próprio texto, da decisão atacada, da mesma paciente ou do mesmo casal.

Nenhuma ligação foi feita só por semelhança de texto. Modelos de sentença repetidos (por exemplo, a 1ª Vara do Júri da Capital paulista) **não** são ligações: são casos distintos que usam o mesmo texto-base.

Resultado: **13 casos com mais de um julgado, que somam 29 julgados.**

| Caso | Julgados, na ordem da trajetória | Base da ligação |
|---|---|---|
| C002 | J002, J003 | Julgamento conjunto de duas apelações conexas. O portal mostra dois acórdãos com o mesmo voto e a mesma data. |
| C004 | J005, J006, J007, J008 | O J005 é a liminar, em processo contra o Estado. O J006 (ação contra a operadora) registra essa autorização por liminar. O J007 e o J008 são do mesmo processo do J006. |
| C008 | J046, J013 | A mesma paciente, a mesma vara e o mesmo parecer institucional. O HC no STJ (J013) ataca a liminar do TJRJ (J046). |
| C009 | J069, J014, J015 | O HC no STJ ataca o acórdão do TJSC. O número de origem no STJ é o número do J069. |
| C010 | J016, J017 | Mesmo HC no STJ. A origem, no TJES, está fora da busca (R002). |
| C012 | J019, J020 | Mesmo número de processo (sentença e apelação). |
| C044 | J054, J053 | Mesmo número de processo (declínio de competência e mérito). |
| C056 | J066, J067 | Ementas idênticas, mesmo relator, mesma data e mesmo código de comarca. Provavelmente ação cautelar e ação principal. São falsos positivos. |
| C088 | J100, J120 | O acórdão identifica a sentença atacada e a mesma gestante. |
| C090 | J102, J121 | O acórdão identifica a sentença atacada e a mesma gestante. |
| C100 | J122, J112 | O J112 não conhece o HC por ser reiteração do HC 2078297-02.2014, que é o J122. |
| C101 | J114, J113 | Mesmo processo (apelação e embargos de declaração). São falsos positivos. |
| C113 | J130, J129 | Mesmo casal e mesma sentença de origem (MS e apelação do MP). |

**Recorrência:** os casos C014 (J022) e C015 (J023) são a mesma gestante, em gestações de 2023 e de 2024, ambas com T18. O J022 registra a autorização anterior à mesma requerente. São casos distintos, ligados por `caso_relacionado`.

Os 110 julgados restantes formam, cada um, um caso de um único julgado.

### 3.2. Ordenação dentro do caso

Os julgados de cada caso seguem a **ordem da trajetória processual**. Quando há datas, ela coincide com a cronologia. Quando a data não consta (J020, J046), a posição foi fixada pela lógica processual: a liminar antes do HC que a ataca, a sentença antes do recurso. A ordem está na constante `GRUPOS` do script.

### 3.3. Numeração

Os casos foram numerados de C001 a C123, na ordem em que o primeiro julgado de cada caso aparece em `julgados.csv`.

### 3.4. Cálculo das colunas

Cada coluna é derivada **dos campos já extraídos** em `julgados.csv`. Não houve nova extração dos documentos. As exceções manuais estão listadas na seção 4.

| Coluna | Regra |
|---|---|
| `id_caso`, `julgados`, `n_julgados` | Da etapa 3.1. |
| `no_escopo` | `Sim` se algum julgado do caso tem `falso_positivo = Não`. `Não` se todos têm `Sim`. `Não acessível` se todos têm `Não acessível` (J009, J070). |
| `falso_positivo`, `motivo_falso_positivo` | Copiados dos julgados do caso. Quando há mais de um valor distinto, aparecem separados por "; ". Nenhum caso mistura julgados que são falso positivo com julgados que não são, por isso `falso_positivo` é sempre o inverso de `no_escopo`. |
| `tribunais`, `uf` | Valores distintos, na ordem da trajetória. As UFs ausentes são ignoradas. |
| `comarca_origem` | A primeira comarca informada na trajetória. Há uma exceção manual (C004). |
| `processos` | Os números de processo distintos dos julgados, mais os processos de `processos_referenciados.csv` cuja `forma_da_referencia` é "Processo de origem" ou "Processo conexo" e que são citados por algum julgado do caso. Esses aparecem com o código da referência, por exemplo `(R008)`. Os precedentes apenas citados **não** entram. |
| `condicao_fetal` | O valor mais informativo entre os julgados, nesta prioridade: T18 > Múltipla > T13 (Patau) > Anencefalia > Outra > Não consta > Não acessível > Não aplicável. |
| `forma_citogenetica` | Mesma lógica, nesta prioridade: Mosaico > Trissomia completa > Não consta > Não acessível > Não aplicável. |
| `ig_semanas`, `ig_momento` | A primeira idade gestacional numérica da trajetória (só o número) e o `momento_idade_gestacional` do mesmo julgado, em coluna separada. Separados, permitem analisar só a IG do pedido, porque a IG do julgamento é maior nos processos demorados. Sem IG numérica, os dois ficam `Não consta`. |
| `instancias_percorridas` | As instâncias distintas na ordem da trajetória. "Tribunal Superior" aparece como "STJ". |
| `data_pedido` | A menor `data_inicial` válida do caso. |
| `data_primeira_decisao` / `data_ultima_decisao` | A `data_julgamento` do primeiro e do último julgado da trajetória; não se substitui pela data de outro julgado. Se o último julgado não traz a data de julgamento, `data_ultima_decisao` recebe a `data_publicacao` **do mesmo julgado**, com anotação em `observacao`. Se não há nenhuma das duas, fica `Não consta`, também anotado. |
| `dias_ate_decisao_util` | Dias entre `data_pedido` e a `data_julgamento` do `julgado_decisivo`. Só é calculado quando o desfecho vem do próprio julgado e as duas datas existem. |
| `desfecho_final`, `julgado_decisivo`, `fonte_do_desfecho` | Regra da seção 3.5. |
| `fonte_dos_fundamentos` | `Julgado decisivo` · `Julgado que relata a decisão` · `Não aplicável` (ver `dicionario_casos.md`). |
| `instancia`, `orgao_julgador`, `via_processual`, `art128_I`, `fundamento_risco_vida_gestante`, `fundamento_inviabilidade_extrauterina`, `fundamento_dignidade_autonomia`, `comparacao_com_anencefalia`, `cita_adpf54`, `cita_hc_932495`, `forma_do_texto`, `perda_de_objeto` | Cópia exata, pelo script, das colunas de mesmo nome do `julgado_decisivo` em `julgados.csv`. Valem `Não aplicável` quando o desfecho é `Não decide a autorização` ou `Sem decisão útil`, e `Não acessível` quando o desfecho é `Não acessível`. Quando o desfecho vem de decisão relatada, os fundamentos copiados são os do julgado que a relata, não os da decisão que prevaleceu. |
| `houve_reforma` | Regra da seção 3.6. |
| `gestacao_encerrada_antes_da_decisao_final` | `Sim — interrupção` para os casos listados na seção 4.3. `Sim — parto ou óbito fetal` se algum julgado tem `houve_parto_antes_do_fim = Sim` ou `situacao_vital_na_decisao = Óbito fetal`. `Não aplicável` quando o desfecho é `Não decide a autorização` ou `Não acessível`. Nos demais casos, `Não consta`. |
| `impugnado_por` | Quem impugnou a autorização judicial (seção 4.4). O padrão é `Nenhuma no corpus`. |
| `caso_relacionado` | Recorrência da mesma gestante (C014 ↔ C015). |
| `questionamentos` | Anomalias de busca e de acesso (seção 4.5). Cada uma vem precedida do julgado de origem entre colchetes. |
| `observacao` | Descrição da trajetória nos casos com mais de um julgado e nos desfechos tirados de decisão relatada. |

### 3.5. Regra do desfecho

O desfecho responde a uma pergunta: **o que valeu, ao fim, para a gestante?**

1. **Vale a última decisão do caso com efeito prático.** Se o `efeito_pratico` do julgado é `Autoriza`, o desfecho é `Autorizado`; se é `Nega`, é `Negado`. "Prejudicado", "não conhecido" e "homologada a desistência" não contam, porque não decidem nada para a gestante. O `julgado_decisivo` é esse julgado, e a `fonte_do_desfecho` é `Próprio julgado`.
2. **Quando nenhum julgado do caso tem efeito prático**, vale a decisão que o próprio julgado relata, e a `fonte_do_desfecho` registra isso.
   - **Liminar ou tutela concedida no próprio recurso:**
     - C023 (J031): tutela antecipada recursal deferida no agravo.
     - C090 (J121): liminar concedida no mandado de segurança.
   - **Decisão de origem que ficou fora do corpus:**
     - C113 (J130): sentença do DIPO que autorizou.
     - C040 (J049), C041 (J050), C047 (J057), C051 (J061), C106 (J119) e C114 (J131): decisões de origem que negaram.
   - **Extinção sem resolução do mérito na origem** conta como `Negado` (C040).
3. **`Não decide a autorização`** vale quando todos os julgados do caso têm `efeito_pratico = Não aplicável`. São as ações de cobertura de plano de saúde ou de indenização ligadas a uma interrupção já autorizada (C001, C059, C061, C072, C122) e os falsos positivos dessa natureza.
4. **`Sem decisão útil`** vale quando nenhuma instância decidiu o mérito e nenhum julgado relata decisão anterior. É só o C100, com dois HCs não conhecidos.

**Por que o passo 2 existe.** Na primeira versão da regra só contava o passo 1. Na conferência, ela produziu resultados errados. No C090, por exemplo, a sentença negou e o acórdão foi julgado prejudicado. A regra daria `Negado`, mas o próprio acórdão relata que a liminar concedida no MS já havia autorizado a interrupção. O passo 2 corrige isso, e a coluna `fonte_do_desfecho` permite separar esses 9 casos em qualquer análise.

### 3.6. Regra da reforma

`houve_reforma` compara o **resultado inicial** do caso com o `desfecho_final`.

- **Resultado inicial:**
  - Se o primeiro julgado do caso é de 1º grau, o resultado inicial é o efeito prático desse julgado.
  - Se o primeiro julgado é de 2º grau ou do STJ, o resultado inicial é o da **decisão atacada, tal como descrita no resumo do julgado**. O script procura, no trecho que segue "contra a decisão/sentença/acórdão/liminar/tutela", os verbos "negou", "indeferiu", "julgou improcedente", "manteve o indeferimento", "autorizou", "autorizara" e "extinguiu". Todos os resultados dessa busca foram conferidos manualmente.
- **Valores:**
  - `Sim (negado → autorizado)`, `Sim (extinto → autorizado)` ou `Sim (autorizado → negado)`.
  - `Não`, quando o resultado se manteve.
  - `Não consta`, quando o resumo não descreve a decisão de origem. Isso ocorre no HC impetrado direto no tribunal e no C008.
  - `Não aplicável`, quando o caso tem uma única decisão de 1º grau ou não tem desfecho de autorização.
- Quando o desfecho vem da própria decisão de origem relatada (regra 3.5, passo 2), `houve_reforma` é `Não` por definição.

## 4. Intervenções manuais

Todas estão escritas como constantes no script, para que fiquem auditáveis.

### 4.1. Ligações (`GRUPOS`, `RELACIONADOS`)

São as listadas na seção 3.1.

### 4.2. Desfecho por decisão relatada (`DESFECHO_RELATADO`)

São três casos: C023, C090 e C113. Os demais desfechos por decisão de origem saem da regra automática da seção 3.6, que foi conferida caso a caso.

### 4.3. Interrupção antes da decisão final (`INTERRUPCAO_ANTES`)

Os casos são C004, C008, C035 (J043), C039 (J048), C045 (J055), C109 (J125) e C113.

Em todos eles, o próprio documento registra que a interrupção foi realizada antes do último julgado do caso. O vocabulário de `julgados.csv` não tem a categoria "interrupção realizada", por isso a informação foi tirada do texto e da `observacao`.

Outros três casos têm parto ou óbito fetal antes da decisão final e são detectados automaticamente: C041, C047 e C106.

### 4.4. Impugnação (`IMPUGNACAO`)

| Caso | Quem impugnou |
|---|---|
| C008 | Terceiros, em HC em favor do nascituro no STJ |
| C044 | Ministério Público, em mandado de segurança |
| C113 | Ministério Público, em apelação e mandado de segurança |
| J041 | Ministério Público (fora do escopo) |

### 4.5. Questionamentos (`Q`)

Por decisão do pesquisador, a planilha deve **registrar as anomalias da busca e do acesso, sem tentar explicá-las além do que se sabe**. Há questionamentos em 33 casos, de sete tipos:

- **Resultado apresentado de forma anômala no portal:**
  - dois acórdãos formais para um único julgamento (TJDFT, C002);
  - item rotulado "acórdão – repetido" que não se consegue atribuir a um documento (TJRN, C004);
  - "Sem resultado" seguido de lista com o processo (TJSC, C009).
- **Acesso limitado:**
  - só a ementa, com "Processo em sigilo" no espelho (TJPR e TJSC);
  - limitação do sistema do TJRN somada a segredo de justiça;
  - arquivo que traz o conteúdo de outro processo (J009);
  - arquivo só com a referência (J070).
- **Processo de origem ou conexo fora da busca:** R002 a R013, nos casos em que os julgados citam.
- **Precedente de T18 do próprio tribunal fora da busca:** HC 2136944-77.2020.8.26.0000 (R014), citado por J081, J116 e J117.
- **Resultado em uma só das chaves:** o julgado apareceu só com "Interrupção da gravidez" e não com "Aborto".
- **Dado a conferir no sistema:** data incompatível com o número do processo (J111).
- **Processo anterior citado sem número:** autorização de 2016 mencionada no J073.

### 4.6. Comarca (`COMARCA`)

No C004, o primeiro julgado (a liminar) saiu no plantão de Natal, mas a ação contra a operadora tramitou em Mossoró. A coluna registra as duas informações.

## 5. Validações

O script interrompe a execução se:

- algum julgado ficar sem caso ou em mais de um caso;
- a soma de `n_julgados` for diferente do número de linhas de `julgados.csv`.

Também foi verificado que, em `julgados.csv`, **todos os campos, menos o novo `id_caso`, são idênticos** aos da versão definitiva do pesquisador.

## 6. Resultado

| | n |
|---|---|
| Casos | 123 |
| No escopo (T18 em gestação, não falso positivo) | 78 |
| Fora do escopo (falsos positivos) | 43 |
| Não acessíveis (J009, J070) | 2 |
| Casos com mais de um julgado | 13 (29 julgados) |

**Nos 78 casos no escopo:**

| `desfecho_final` | n |
|---|---|
| Autorizado | 52 |
| Negado | 20 |
| Não decide a autorização | 5 |
| Sem decisão útil | 1 |

| `houve_reforma` | n |
|---|---|
| Sim (negado → autorizado) | 22 |
| Sim (extinto → autorizado) | 1 |
| Sim (autorizado → negado) | 0 |
| Não | 19 |
| Não consta | 4 |
| Não aplicável | 32 |

| `gestacao_encerrada_antes_da_decisao_final` | n |
|---|---|
| Sim — interrupção | 7 |
| Sim — parto ou óbito fetal | 3 |
| Não consta | 63 |
| Não aplicável | 5 |

## 7. Limitações

1. **`dias_ate_decisao_util` só pôde ser calculado em 9 casos**, porque `data_inicial` raramente consta nos documentos. Quando houve liminar antes do acórdão, o prazo calculado (até o acórdão) é **maior** que o prazo real até a autorização.
2. **A decisão de origem vem do resumo.** Em `houve_reforma` e nos desfechos por decisão relatada, a origem é a decisão descrita no resumo do julgado, que foi redigido a partir do documento e está sujeito à verificação do Bloco B2. Não é uma decisão lida diretamente, porque está fora do corpus.
3. **`gestacao_encerrada_antes_da_decisao_final = Não consta` não significa que a gestação continuava.** Significa que o documento não informa.
4. **As ligações dependem do que os documentos revelam.** Dois julgados da mesma gestação que não se referem um ao outro, nem pelo número nem pela identificação da parte, aparecem como casos separados. A busca não captou todos os processos (ver `processos_referenciados.csv`), então podem existir trajetórias incompletas.
5. **Uma ligação é inferência do texto, não identidade de número.** No C004, a sentença do J006 registra a autorização por liminar "em processo contra o Estado", e o J005 é essa liminar. Os números dos processos são diferentes.
6. **Não há dados pessoais.** A identificação da mesma gestante ou do mesmo casal foi feita na leitura, e nenhum nome ou dado pessoal foi copiado para as planilhas.

## 8. Como reproduzir

```bash
# Requer Python 3.8+ e nenhuma biblioteca externa. A partir da raiz do repositório:
mkdir saida
cp dados/processos_referenciados.csv saida/
python3 auditoria/scripts/build_casos.py dados/julgados.csv saida/
```

O script grava `casos.csv` e `julgados.csv` na pasta de saída, com a coluna `id_caso` na segunda posição, em UTF-8 com BOM, separados por vírgula. Os arquivos gerados são idênticos, byte a byte, aos publicados em `dados/` (conferido em 22/10/2026).

## 9. Registro de intervenções

| Data | Intervenção | Responsável |
|---|---|---|
| 12–14/10/2026 | Ligações anotadas em `observacao` durante a extração | Extração (IA), com revisão do pesquisador |
| 14/10/2026 | `julgados.csv` fixada como definitiva; J012 movido para `documentos_de_contexto.csv` | Pesquisador |
| 15/10/2026 | Aprovação do desenho: unidade gestação, falsos positivos incluídos, `id_caso` em `julgados.csv` | Pesquisador |
| 15/10/2026 | Construção de `casos.csv`. Inclusão do passo 2 na regra do desfecho, após a conferência mostrar que a regra original errava no C090 | Script e revisão manual |
| 15/10/2026 | Inclusão de `falso_positivo` e `motivo_falso_positivo` | Pedido do pesquisador |
| 15/10/2026 | Versão 2. Cópia de 12 colunas do julgado decisivo e de `fonte_dos_fundamentos` (critério CF). Separação de `ig_semanas` e `ig_momento` (IG). Data de publicação como substituta de `data_ultima_decisao` ausente, com anotação (DP). As 1.814 células alteradas estão em `auditoria/alteracoes_por_celula_casos.csv`. Nenhuma variável nova; `julgados.csv` intacta | Pedido do pesquisador; execução por script |
