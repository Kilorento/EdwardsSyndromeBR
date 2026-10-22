# Metodologia

## 1. Busca nos tribunais

- **Responsável:** Pedro Farnese Dias de Assis Lima.
- **Período:** 17/09/2026 a 11/10/2026. A data da última consulta de cada tribunal está no espelho.
- **Registro completo:** `pesquisa/espelho_das_pesquisas.md`. Para cada tribunal, o espelho traz o link do sistema de jurisprudência, o alcance (1º grau, 2º grau, colégios recursais), a captura de tela dos critérios e a lista de resultados de cada chave.

**Chaves finais:**

- `"Síndrome de Edwards" E Aborto`
- `"Síndrome de Edwards" E "Interrupção da gravidez"`

A coluna `chave_busca` de `dados/julgados.csv` indica por qual chave cada julgado retornou.

**Abrangência:** os 27 tribunais de justiça, o STJ e o STF.

| Resultado | Tribunais |
|---|---|
| Sem resultado | TJAC, TJAM, TJAP, TJPA, TJRR, TJRO, TJAL, TJBA, TJPI, TJSE, TJMA, TJPE, TJPB, TJES, TJGO, TJMT, TJMS e STF |
| Com resultado | TJCE, TJDFT, TJMG, TJPR, TJRJ, TJRN, TJRS, TJSC, TJSP, TJTO e STJ |

O 1º grau foi pesquisado onde o tribunal o disponibiliza.

**Histórico do escopo:** a pesquisa começou mais ampla, com crimes contra a vida de pessoas com síndrome de Edwards e chaves que incluíam homicídio e infanticídio. Em outubro de 2026, o objeto foi reduzido ao aborto, e a busca foi refeita com as chaves acima.

## 2. Corpus

O corpus tem **141 arquivos .md**, um por documento obtido, em `julgados/<tribunal>/`, já anonimizados (ver `julgados/NOTA_ANONIMIZACAO.md`). Cada julgado recebeu um código `J001`–`J140`. A coluna `arquivos_fonte` de `dados/julgados.csv` indica o arquivo de cada julgado.

| Forma do texto | n |
|---|---|
| PDF de inteiro teor | 106 |
| Inteiro teor colado no espelho do tribunal | 21 |
| Apenas ementa | 10 |
| Apenas referência | 2 |

**Casos especiais:**

- **J009:** o arquivo `TJTO/0000866-26.2025…` contém, por engano, o acórdão de outro processo, o RSE 0010922-92.2021, que não retornou na busca. Por decisão do pesquisador, esse conteúdo não é usado. O J009 fica como `Apenas referência`, e o RSE foi registrado como `R001`.
- **J012:** é um despacho do STJ sem conteúdo decisório. Foi retirado da base de julgados e está em `dados/documentos_de_contexto.csv`, ligado ao J013.
- **J002 e J003:** acórdãos idênticos de um mesmo julgamento conjunto, publicados com dois números no TJDFT.
- **Processos referenciados:** são processos sobre T18 que um julgado cita com número, mas que não retornaram na busca. Ficam em `dados/processos_referenciados.csv` como metadado, não como julgado. Eles mostram que a busca não alcança tudo; ver as limitações.

## 3. Desenho da extração

A extração foi feita em blocos, porque campos fechados e textos livres pedem controles diferentes.

| Bloco | Campos | Quem faz | Controle |
|---|---|---|---|
| **A** | Valores fechados e literais: números, datas, órgão, relator, provimento, fundamentos, comparações etc. | Três extratores independentes e cegos: Claude, Gemini e Manus | Concordância entre os três. A divergência vai para arbitragem humana |
| **B1** | Texto livre: `tipo_acao` e `resumo_do_julgado` | Claude | — |
| **B2** | Verificação do B1 | Gemini | Para cada afirmação do resumo: `Sustentada`, `Não sustentada` ou `Contrariada` |

Três resumos de um mesmo acórdão nunca coincidem palavra por palavra. Por isso, nos textos livres não se mede concordância. O que se procura é afirmação sem respaldo no documento, ou seja, alucinação.

**Regras invioláveis do Bloco A** (texto completo em `auditoria/prompts/prompt_blocoA.md`):

- decidir só pelo documento;
- nunca inventar;
- não usar busca por palavra-chave;
- ler o documento inteiro;
- justificar cada campo não trivial com trecho literal;
- não alterar o vocabulário fechado (o que não couber vira `REPORTAR`);
- não copiar dados pessoais.

**Três códigos de ausência:** `vazio` nunca é resposta.

- **`Não aplicável`:** o campo não existe naquele tipo de processo.
- **`Não consta`:** o documento foi lido por inteiro e não traz a informação. Isso é um achado sobre o tribunal.
- **`Não acessível`:** o texto integral não estava disponível. É um limite da pesquisa.

### 3.1 Calibração e mudanças de protocolo (12/10/2026)

Antes de enviar os lotes às IAs, o Claude extraiu um lote de calibração de 11 documentos (TJDFT, TJRN e TJTO). Em seguida extraiu os 140. As lacunas do dicionário encontradas nessa etapa entraram no prompt final:

- valor `Apenas referência`;
- tabela de processos referenciados;
- `fundamento_risco_vida_gestante` vinculado ao exame do art. 128, I;
- ADPF 54 citada sem número;
- tratamento de magistrado não flexionado → `Não consta`;
- data de liberação nos autos não é data de publicação;
- definição de falso positivo;
- proibição de copiar dados pessoais.

### 3.2 Execução

| Extrator | Como foi rodado | Datas |
|---|---|---|
| **Claude** (Anthropic) | Leitura integral dos 140 documentos, com conferência automática de datas e números contra o texto | 12/10/2026 |
| **Gemini** (Google) | Uma remessa por vez (`loteNN_blocoA…`), coladas uma a uma em conversas separadas. O J020 foi omitido pelo Gemini no lote 01 e extraído depois, em pedido avulso | 13–14/10/2026 |
| **Manus AI** | Recebeu a pasta inteira de remessas de uma vez e trabalhou de forma autônoma. A execução foi pausada quando os créditos acabavam e retomada com o pedido de continuar | 13–14/10/2026 |
| **Gemini (B2)** | Remessas `loteNN_blocoB2_verificador.md`, em conversa separada da do Bloco A | 13–14/10/2026 |

**Versão dos modelos:** o prompt pedia que cada IA registrasse nome e versão. O Manus declarou não ver a versão. O Gemini se declarou "1.5 Pro / Experimental", o que não é plausível em outubro de 2026. A versão exata dos modelos fica, portanto, **não registrada**.

**Tentativa com o ChatGPT:** considerou-se fazer a terceira extração com o ChatGPT. Pela demora e pela necessidade constante de reenviar os prompts (o modelo lia os documentos, mas muitas vezes não extraía os dados), buscou-se outra IA, e o Manus AI cumpriu bem o trabalho. Nenhuma saída do ChatGPT foi usada.

## 4. Comparação entre extratores

Os arquivos estão em `auditoria/comparacao/`. Foram comparados 24 campos fechados e 5 semiestruturados: número do processo, três datas e idade gestacional. Os textos livres ficaram de fora.

1. **Normalização só de grafia** nas saídas do Gemini, por exemplo "2.º grau" → "2º grau". As trocas estão em `auditoria/extracoes/gemini/normalizacoes_de_grafia.csv`. A abreviação "Des." sem flexão **não** foi normalizada, porque pela regra ela vale `Não consta`.
2. **Intervenções do pesquisador nas extrações das IAs**, aplicadas só na comparação. Cada célula está em `auditoria/comparacao/log_intervencoes.csv`.
   - **I1:** `momento_idade_gestacional = Não especificado` sem idade gestacional informada → `Não consta`. Sem idade gestacional, não existe momento.
   - **I2:** "Autorização prévia contra o Estado" em alvará, HC ou MS contra ato judicial → "sem polo passivo". O Estado não é réu nesses casos. **Atenção:** a I2 alinha os valores das IAs ao do Claude. Antes dela, a concordância Claude × Gemini em `via_processual` era de 43%.
   - **I3:** `forma_do_texto` ficou fora da comparação, porque as IAs não viram o arquivo original.
3. **Fundamentos** (`fundamento_*`). O protocolo pedia `Sim` = "enfrentado como razão de decidir, em qualquer sentido". Na prática:
   - o **Manus** seguiu essa regra: nas 60 células em que o julgador rejeita o fundamento, marcou `Sim` em 53;
   - o **Gemini** leu `Sim` como "acolhe": nessas 60 células, marcou `Sim` em 15.

   A codificação do Claude foi refeita em três valores (`Acolhe · Rejeita · Não enfrenta`), relendo o corpus, e passou a ser comparada com cada IA no nível que ela usou:
   - Claude × Gemini: acolhe × não acolhe;
   - Claude × Manus: enfrenta × não enfrenta.

   Gemini × Manus não é comparável nesses campos.
4. **Unidade de comparação:** valores independentes de cada extrator. A comparação mede a concordância de leitura, não a qualidade da base final. As decisões de arbitragem (seção 5) não entram no cálculo.

## 5. Arbitragem e base final

A base final (`dados/julgados.csv`) parte da extração do Claude e recebe as decisões do pesquisador. **Toda célula alterada está em `auditoria/ALTERACOES.md`**, com o valor anterior, o valor novo, o critério e quem decidiu. As principais decisões foram estas.

**Lacunas de vocabulário (`REPORTAR`):**

- resultado duplo → `Parcialmente provido`;
- indeferimento do pedido por decisão → `Liminar indeferida`;
- inadmissão de recurso especial e competência declinada → `Não conhecido`;
- novo valor de via `Impugnação da autorização`, para quando o MP ou terceiros pedem que a interrupção seja impedida;
- novo valor de via `Autorização prévia contra hospital ou médico`;
- acórdão que concede a ordem liminarmente → `Liminar deferida`;
- regra para idade gestacional em intervalo: limite inferior.

**Recodificação dos fundamentos em três valores**, com estas regras:

- `Rejeita`: o julgador examinou o fundamento e o afastou.
- Risco à saúde citado sem o art. 128, I → `Não enfrenta`.
- Art. 128, I, invocado pelo julgador, direto ou por analogia, mesmo para risco à saúde → `Acolhe`.

**`comparacao_com_anencefalia`:**

- `Equipara` só quando o julgado aplica a ADPF 54 (ou sua razão de decidir) por **analogia direta**. Citar a anencefalia, ou agrupá-la com a T18, não basta.
- `Distingue` quando o julgado examina a analogia e a recusa. Esses julgados podem ser filtrados pelo valor `Distingue`.

**Novas colunas:**

- `efeito_pratico`: se a decisão autoriza ou nega a interrupção, independentemente do rótulo processual.
- `art128_I`: como o julgador tratou o art. 128, I, do CP. Distingue aplicação, afastamento, remessa ao médico e mera menção.

## 6. Limitações

1. **A busca mede jurisprudência publicada e acessível, não a incidência de casos.** Tribunais que não publicam o 1º grau, ou que mantêm os processos em segredo de justiça, aparecem com menos casos ou nenhum. Há prova disso na própria base:
   - o HC 732.868 do STJ veio do TJES, que não retornou nenhum resultado;
   - vários processos de T18 citados nos julgados não retornaram na busca (`processos_referenciados.csv`).
2. **A codificação foi feita por modelos de linguagem.** Eles erram e podem compartilhar vieses. A concordância entre três não substitui a decisão humana.
3. **Nem toda divergência foi arbitrada uma a uma.** A base final mantém o valor do Claude, salvo nas células listadas em `auditoria/ALTERACOES.md`. Em 146 células, Gemini e Manus concordam entre si contra o Claude:
   - 91 são de conteúdo;
   - 55 são só de código de ausência.

   Elas estão em `auditoria/comparacao/divergencias_campo_a_campo.csv` (coluna `maioria_2de3`). Essas células não foram revistas uma a uma. Há alguns prováveis acertos das IAs já identificados: perda de objeto em J006, J013 e J125; parto antes do fim em J055, J129 e J131; citação da ADPF em J050 e J119.
4. **A verificação B2 não encontrou nenhuma afirmação sem respaldo em 850.** Isso pode indicar resumos fiéis ou baixa capacidade de discriminação do verificador. Não houve teste com afirmações falsas plantadas.
5. **Versão dos modelos não registrada** (seção 3.2).
6. **Contar decisões não mede a força do argumento.** Várias sentenças do TJSP seguem modelos de texto repetidos pelo mesmo juízo, e isso infla a contagem de rotas jurídicas.
7. **Anonimização:** os textos foram anonimizados antes da publicação, com substituição por regras e revisão humana arquivo a arquivo, seguida de verificação automática de nomes. Nenhum processo elimina todo risco de reidentificação.

## 7. O que não foi publicado

Para proteger os dados pessoais das partes, três conjuntos de arquivos de trabalho ficaram fora do repositório:

- **Remessas enviadas às IAs** (`loteNN_blocoA…` e `loteNN_blocoB2…`): cada remessa é o prompt seguido da cópia integral, não anonimizada, dos julgados do lote. O prompt está em `auditoria/prompts/`, e os julgados, anonimizados, em `julgados/`.
- **Respostas brutas do Gemini e do Manus**, que trazem trechos literais com nomes das partes. As respostas estruturadas, em planilha, estão em `auditoria/extracoes/`.
- **Corpus original**, antes da anonimização.

Esses arquivos ficam com o pesquisador.
