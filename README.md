# EdwardsSyndromeBR

**Português** · [English](#english)

Base de jurisprudência brasileira sobre pedidos judiciais de interrupção da gestação de fetos com **Síndrome de Edwards** (trissomia do cromossomo 18, T18).

A base reúne 139 decisões de 10 Tribunais de Justiça e do Superior Tribunal de Justiça, proferidas entre 1998 e 2026. Ela foi construída para a pesquisa *O ABORTO DE NASCITUROS COM SÍNDROME DE EDWARDS: ENTRE A LITERATURA MÉDICA E O STATUS JURÍDICO BRASILEIRO*, de Pedro Farnese Dias de Assis Lima.

## Conteúdo

| | Quantidade |
|---|---|
| Julgados (decisões) | 139 |
| Casos (gestações) | 123 |
| Casos no escopo (T18 em gestação, sem falso positivo) | 78 |
| Casos no escopo com decisão sobre o pedido | 72 (52 autorizados, 20 negados) |
| Tribunais com resultado | STJ, TJCE, TJDFT, TJMG, TJPR, TJRJ, TJRN, TJRS, TJSC, TJSP, TJTO |

O TJSP concentra metade dos julgados (70 de 139).

## Estrutura do repositório

```
EdwardsSyndromeBR/
├── README.md
├── LICENSE
├── METODOLOGIA.md            busca, extração, comparação, arbitragem e limitações
├── dados/                    o que a maioria dos usuários vai usar
│   ├── julgados.csv                  uma linha por decisão
│   ├── casos.csv                     uma linha por gestação
│   ├── processos_referenciados.csv   processos citados que não retornaram na busca
│   ├── documentos_de_contexto.csv    documento retirado da base, mantido como contexto
│   ├── dicionario_julgados.md        variáveis e valores de julgados.csv
│   ├── dicionario_casos.md           variáveis e valores de casos.csv
│   └── metodo_planilha_de_casos.md   como os julgados foram agrupados em casos
├── julgados/                 inteiro teor anonimizado, uma pasta por tribunal
│   └── NOTA_ANONIMIZACAO.md
├── pesquisa/
│   ├── espelho_das_pesquisas.md      chaves, filtros e telas de cada busca nos tribunais
│   ├── imagens/
│   └── triagem_literatura_pubmed.xlsx   triagem da revisão da literatura médica
└── auditoria/                para conferir ou reproduzir a codificação
    ├── ALTERACOES.md                 critérios de cada alteração feita depois da extração
    ├── alteracoes_por_celula.csv     toda célula alterada em julgados.csv
    ├── alteracoes_por_celula_casos.csv   toda célula gerada ou alterada em casos.csv
    ├── prompts/                      instruções enviadas às IAs
    ├── extracoes/                    extração independente de cada IA (Claude, Gemini, Manus)
    ├── comparacao/                   concordância e divergências entre as IAs
    └── scripts/                      programa que gera casos.csv a partir de julgados.csv
```

## Como usar

1. **Abra as planilhas.** Os arquivos `.csv` abrem no Excel, no LibreOffice, no Google Sheets, no R ou no Python (UTF-8, separador vírgula).
2. **Escolha a unidade de análise.**
   - `casos.csv` responde perguntas sobre gestações: quantas foram autorizadas, quanto tempo levou, se houve reforma.
   - `julgados.csv` responde perguntas sobre decisões: tribunal, relator, fundamentos, precedentes citados.
3. **Ligue as duas tabelas** pela coluna `id_caso`, presente nas duas.
4. **Leia o texto da decisão.** A coluna `arquivos_fonte` de `julgados.csv` indica o arquivo correspondente na pasta `julgados/`.
5. **Filtros recomendados.**
   - Para analisar o fenômeno, use `no_escopo = Sim` em `casos.csv`. Os demais casos são falsos positivos da busca (outra síndrome, ação de outra natureza).
   - Para cruzar desfecho com fundamento, use `fonte_dos_fundamentos = Julgado decisivo` (ver `dicionario_casos.md`).
6. **Códigos de ausência.** `Não consta`: a decisão foi lida por inteiro e não traz a informação. `Não aplicável`: a pergunta não cabe naquele caso. `Não acessível`: o texto integral não estava disponível.

## Como a base foi feita

O passo a passo completo está em [`METODOLOGIA.md`](METODOLOGIA.md). Em resumo:

- **Busca.** Portais públicos de jurisprudência dos 27 Tribunais de Justiça, do STJ e do STF, de 17/09 a 11/10/2026, com as chaves `"Síndrome de Edwards" E Aborto` e `"Síndrome de Edwards" E "Interrupção da gravidez"`. O registro de cada busca está em `pesquisa/espelho_das_pesquisas.md`.
- **Universo.** Levantamento censitário dos julgados acessíveis pelas chaves de busca; não há amostragem.
- **Extração.** Cada julgado foi codificado de forma independente por três modelos de linguagem (Claude, Gemini e Manus). A base final parte da extração do Claude, e as divergências e lacunas foram decididas pelo pesquisador. Toda célula alterada está em `auditoria/`, com o valor anterior, o novo e o critério.
- **Casos.** Julgados que tratam da mesma gestação formam um caso, mesmo em processos ou tribunais diferentes. A `casos.csv` é gerada por um script (`auditoria/scripts/build_casos.py`) que a reproduz de forma idêntica.

## Anonimização

Os textos das decisões foram anonimizados antes da publicação. Foram mantidos os nomes de quem atuou no processo (magistrados, membros do Ministério Público, advogados, defensores e peritos oficiais), dos autores citados e das pessoas jurídicas. Foram substituídos por rótulos como `[PACIENTE]` ou `[MÉDICO]` os nomes das partes, familiares, testemunhas e médicos assistentes, com seus documentos, endereços e telefones. Os critérios estão em `julgados/NOTA_ANONIMIZACAO.md`.

A anotação "Anonimização: …" na coluna `observacao` de `julgados.csv` descreve como o **tribunal** publicou a decisão (por exemplo, se o nome da gestante aparecia em claro). Ela não se refere aos textos deste repositório, que estão anonimizados.

## Limitações

- Os números descrevem o corpus encontrado, não o Judiciário brasileiro. Decisões em segredo de justiça ou fora dos portais não aparecem.
- 15 processos citados nas decisões não retornaram na busca (`processos_referenciados.csv`).
- 2 casos não tinham conteúdo acessível e 2 casos no escopo só tinham a ementa.
- A distribuição entre tribunais reflete o que cada portal disponibiliza, não a frequência real de pedidos.
- A codificação foi feita com apoio de modelos de linguagem, que erram e podem compartilhar vieses. Ver a seção de limitações de `METODOLOGIA.md`.

## Como citar

> LIMA, Pedro Farnese Dias de Assis. *EdwardsSyndromeBR: base de jurisprudência brasileira sobre Síndrome de Edwards (trissomia 18)*. 2026. Disponível em: https://github.com/Kilorento/EdwardsSyndromeBR.

## Licença

[CC BY-NC 4.0](LICENSE): uso livre para fins não comerciais, com citação da fonte.

## Autoria

- **Pesquisa e organização da base:** Pedro Farnese Dias de Assis Lima
- **Revisão da organização do repositório:** Lucas Vilas Boas Iwano

Encontrou um erro? Abra uma *issue* neste repositório.

---

<a id="english"></a>

# EdwardsSyndromeBR (English)

[Português](#edwardssyndromebr) · **English**

A dataset of Brazilian court decisions on requests to terminate pregnancies of fetuses with **Edwards syndrome** (trisomy 18, T18).

The dataset covers 139 decisions from 10 Brazilian Courts of Justice (state-level courts and their first-instance judges) and the Superior Court of Justice (STJ), issued between 1998 and 2026. It was built for the research project *O ABORTO DE NASCITUROS COM SÍNDROME DE EDWARDS: ENTRE A LITERATURA MÉDICA E O STATUS JURÍDICO BRASILEIRO* ("THE ABORTION OF UNBORN CHILDREN WITH EDWARDS SYNDROME: BETWEEN MEDICAL LITERATURE AND THE BRAZILIAN LEGAL STATUS"), by Pedro Farnese Dias de Assis Lima.

All data, variable names, values and supporting documents are in Portuguese.

## Contents

| | Count |
|---|---|
| Decisions (`julgados`) | 139 |
| Cases (pregnancies, `casos`) | 123 |
| In-scope cases (T18 pregnancy, not a false positive) | 78 |
| In-scope cases with a ruling on the request | 72 (52 granted, 20 denied) |
| Courts with results | STJ, TJCE, TJDFT, TJMG, TJPR, TJRJ, TJRN, TJRS, TJSC, TJSP, TJTO |

The São Paulo court (TJSP) accounts for half of the decisions (70 of 139).

## Repository structure

```
EdwardsSyndromeBR/
├── README.md
├── LICENSE
├── METODOLOGIA.md            methodology: search, extraction, comparison, arbitration, limitations
├── dados/                    data: what most users need
│   ├── julgados.csv                  one row per decision
│   ├── casos.csv                     one row per pregnancy
│   ├── processos_referenciados.csv   cited proceedings not retrieved by the search
│   ├── documentos_de_contexto.csv    document removed from the dataset, kept as context
│   ├── dicionario_julgados.md        codebook for julgados.csv
│   ├── dicionario_casos.md           codebook for casos.csv
│   └── metodo_planilha_de_casos.md   how decisions were grouped into cases
├── julgados/                 anonymized full texts, one folder per court
│   └── NOTA_ANONIMIZACAO.md
├── pesquisa/                 search records
│   ├── espelho_das_pesquisas.md      search strings, filters and screenshots for each court
│   ├── imagens/
│   └── triagem_literatura_pubmed.xlsx   screening sheet of the medical literature review
└── auditoria/                audit trail: to check or reproduce the coding
    ├── ALTERACOES.md                 criteria for every change made after extraction
    ├── alteracoes_por_celula.csv     every changed cell in julgados.csv
    ├── alteracoes_por_celula_casos.csv   every generated or changed cell in casos.csv
    ├── prompts/                      instructions sent to the AI models
    ├── extracoes/                    independent extraction by each model (Claude, Gemini, Manus)
    ├── comparacao/                   agreement and disagreements between models
    └── scripts/                      program that builds casos.csv from julgados.csv
```

## How to use

1. **Open the spreadsheets.** The `.csv` files open in Excel, LibreOffice, Google Sheets, R or Python (UTF-8, comma separator).
2. **Choose the unit of analysis.**
   - `casos.csv` answers questions about pregnancies: how many were granted, how long it took, whether a decision was reversed.
   - `julgados.csv` answers questions about decisions: court, reporting judge, legal grounds, precedents cited.
3. **Link the two tables** through the `id_caso` column, present in both.
4. **Read the decision.** The `arquivos_fonte` column in `julgados.csv` points to the matching file in `julgados/`.
5. **Recommended filters.**
   - To study the phenomenon, use `no_escopo = Sim` in `casos.csv`. The other cases are search false positives (another syndrome, a different kind of lawsuit).
   - To cross outcome with legal grounds, use `fonte_dos_fundamentos = Julgado decisivo` (see `dicionario_casos.md`).
6. **Missing-value codes.** `Não consta`: the decision was read in full and does not provide the information. `Não aplicável`: the question does not apply. `Não acessível`: the full text was not available.

## How the dataset was built

The full procedure is in [`METODOLOGIA.md`](METODOLOGIA.md). In short:

- **Search.** Public case-law portals of all 27 Courts of Justice, the STJ and the Supreme Court (STF), from 17 September to 11 October 2026, with the search strings `"Síndrome de Edwards" E Aborto` and `"Síndrome de Edwards" E "Interrupção da gravidez"` ("abortion" and "termination of pregnancy"). Each search is documented in `pesquisa/espelho_das_pesquisas.md`.
- **Universe.** A census of the decisions retrievable with these search strings; no sampling.
- **Extraction.** Each decision was coded independently by three large language models (Claude, Gemini and Manus). The final dataset starts from Claude's extraction; disagreements and gaps were decided by the researcher. Every changed cell is logged in `auditoria/`, with the previous value, the new value and the criterion.
- **Cases.** Decisions concerning the same pregnancy form one case, even across different proceedings or courts. `casos.csv` is generated by a script (`auditoria/scripts/build_casos.py`) that reproduces it exactly.

## Anonymization

The decision texts were anonymized before publication. Names of those who acted in the proceedings (judges, prosecutors, lawyers, public defenders and official experts), of cited authors and of legal entities were kept. Names of parties, relatives, witnesses and attending physicians, with their ID numbers, addresses and phone numbers, were replaced by labels such as `[PACIENTE]` (patient) or `[MÉDICO]` (physician). The criteria are in `julgados/NOTA_ANONIMIZACAO.md`.

The note "Anonimização: …" in the `observacao` column of `julgados.csv` describes how the **court** published the decision (for instance, whether the pregnant woman's name appeared in full). It does not refer to the texts in this repository, which are anonymized.

## Limitations

- The figures describe the corpus found, not the Brazilian judiciary. Sealed decisions and decisions not available on the portals are missing.
- 15 proceedings cited in the decisions were not retrieved by the search (`processos_referenciados.csv`).
- 2 cases had no accessible content and 2 in-scope cases only had the headnote.
- The distribution across courts reflects what each portal makes available, not the actual frequency of requests.
- Coding was done with the support of language models, which make mistakes and may share biases. See the limitations section of `METODOLOGIA.md`.

## How to cite

> LIMA, Pedro Farnese Dias de Assis. *EdwardsSyndromeBR: Brazilian case-law dataset on Edwards syndrome (trisomy 18)*. 2026. Available at: https://github.com/Kilorento/EdwardsSyndromeBR.

## License

[CC BY-NC 4.0](LICENSE): free non-commercial use, with attribution.

## Authors

- **Research and dataset organization:** Pedro Farnese Dias de Assis Lima
- **Repository organization review:** Lucas Vilas Boas Iwano

Found an error? Open an *issue* in this repository.
