# Monta casos.csv (uma linha por gestação/litígio) e acrescenta id_caso a julgados.csv.
# Fonte: julgados.csv definitivo do pesquisador (14/10/2026). Ligações e exceções manuais documentadas abaixo.
# Uso: python3 build_casos.py <julgados.csv> <pasta de saída com processos_referenciados.csv>
# Exemplo, a partir da raiz do repositório:
#   mkdir saida && cp dados/processos_referenciados.csv saida/
#   python3 auditoria/scripts/build_casos.py dados/julgados.csv saida/
import csv, re, sys, os, datetime

SRC, OUT = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
J = {r["id_julgado"]: r for r in rows}
refs = list(csv.DictReader(open(os.path.join(OUT, "processos_referenciados.csv"), encoding="utf-8-sig")))
AUS = {"Não consta", "Não acessível", "Não aplicável", "—", ""}

# --- Casos com mais de um julgado (ordem = cronologia da trajetória) ---
GRUPOS = [
    ["J002", "J003"], ["J005", "J006", "J007", "J008"], ["J046", "J013"], ["J069", "J014", "J015"],
    ["J016", "J017"], ["J019", "J020"], ["J054", "J053"], ["J066", "J067"], ["J100", "J120"],
    ["J102", "J121"], ["J122", "J112"], ["J114", "J113"], ["J130", "J129"],
]
RELACIONADOS = {"J022": ("J023", "mesma gestante, gestação anterior (2023), também com T18"),
                "J023": ("J022", "mesma gestante, gestação seguinte (2024), também com T18")}

# --- Desfecho tirado de decisão relatada no julgado (quando nenhum julgado do caso tem efeito prático) ---
DESFECHO_RELATADO = {
    "J031": ("Autorizado", "Decisão relatada no julgado (tutela antecipada recursal deferida no próprio agravo)"),
    "J102": ("Autorizado", "Decisão relatada no julgado (liminar concedida no mandado de segurança, relatada no J121)"),
    "J130": ("Autorizado", "Decisão relatada no julgado (sentença do DIPO que autorizou, fora do corpus)"),
}
DECISIVO_RELATADO = {"J031": "J031", "J102": "J121", "J130": "J130"}

INTERRUPCAO_ANTES = {"J005", "J013", "J043", "J048", "J055", "J125", "J129"}  # interrupção feita antes da decisão final do caso
IMPUGNACAO = {"J013": "Terceiros (HC em favor do nascituro, no STJ)", "J041": "Ministério Público",
              "J053": "Ministério Público (mandado de segurança)", "J129": "Ministério Público (apelação e mandado de segurança)"}

Q = {  # questionamentos sobre a busca e o acesso (por julgado; agregados no caso)
    "J002": "O portal do TJDFT mostra dois acórdãos formais (nº 1248053 e 1248070), com o mesmo voto e a mesma data, para um único julgamento conjunto de dois processos conexos. Por quê?",
    "J007": "O espelho lista este acórdão sob '1º grau'. Segundo o pesquisador, o TJRN só disponibiliza a ementa, por limitação do próprio sistema somada a segredo de justiça.",
    "J008": "Na chave 'Interrupção', o 2º grau devolveu um item rotulado 'acórdão – repetido', que pode ser este documento ou o J007; não dá para saber qual.",
    "J009": "O arquivo deste resultado traz o inteiro teor de outro processo (R001, TJTO 0010922-92.2021); o conteúdo próprio não está acessível.",
    "J016": "O processo de origem no TJES (R002) não aparece na busca: o TJES retornou zero resultados.",
    "J017": "Listado só na chave 'Interrupção'.",
    "J018": "Os processos de origem no TJSC (R003, R004) não retornaram na busca.",
    "J029": "O texto só traz '0003966-'; o número completo veio do índice do espelho.",
    "J031": "Listado só na chave 'Interrupção'.",
    "J043": "O processo de origem (R005) não retornou na busca.",
    "J049": "O processo de origem (R006) não retornou na busca.",
    "J053": "O processo de origem em Carazinho (R008) não retornou na busca.",
    "J055": "O processo de origem em São Borja (R007) não retornou na busca.",
    "J057": "Retornou só na chave 'Interrupção da gravidez', não na chave 'Aborto'.",
    "J059": "Retornou só na chave 'Interrupção da gravidez', não na chave 'Aborto'.",
    "J066": "As ementas de J066 e J067 são idênticas e só o número muda; nenhuma menciona T18, aborto ou gestação. O termo que casou com a chave deve estar no inteiro teor sigiloso.",
    "J069": "Sob a chave 'Interrupção da gravidez', o espelho mostra 'Sem resultado' e, logo abaixo, a lista com este processo.",
    "J070": "O espelho registra 'Somente ementa', mas o arquivo traz só a referência. Retornou só na chave 'Interrupção da gravidez'.",
    "J071": "O processo conexo de autorização (R009) não retornou na busca.",
    "J073": "A autorização criminal de 2016 é citada sem número; não foi possível localizá-la.",
    "J081": "Cita o HC 2136944-77.2020.8.26.0000 (R014), acórdão de T18 do próprio TJSP que não aparece na busca de 2º grau.",
    "J092": "Retornou só na chave 'Interrupção da gravidez', não na chave 'Aborto'.",
    "J111": "A data do documento (15/08/2012) é incompatível com o número do processo (2013) e com a liberação nos autos (07/03/2013); conferir no sistema.",
    "J115": "O processo de origem (R013) não retornou na busca.",
    "J116": "Cita o HC 2136944-77.2020.8.26.0000 (R014), acórdão de T18 do próprio TJSP que não aparece na busca de 2º grau.",
    "J117": "O processo de origem (R012) não retornou na busca. Cita o HC 2136944-77.2020.8.26.0000 (R014), acórdão de T18 do próprio TJSP que também não aparece na busca de 2º grau.",
    "J126": "O processo de origem (R011) não retornou na busca.",
    "J139": "O processo de origem (R010) não retornou na busca. Retornou só na chave 'Interrupção da gravidez'.",
    "J140": "Retornou só na chave 'Interrupção da gravidez', não na chave 'Aborto'.",
}
SO_EMENTA = ["J040", "J041", "J042", "J051", "J062", "J065", "J066", "J067", "J069"]
for j in SO_EMENTA:
    Q[j] = ("Só a ementa está disponível; o espelho registra 'Processo em sigilo'. " + Q.get(j, "")).strip()

OBS = {  # observação de trajetória para casos com mais de um julgado e para desfechos relatados
    "J002": "Julgamento conjunto de duas apelações conexas (ação da operadora para rescindir o contrato e ação da beneficiária e dos genitores). Criança já nascida; não há pedido de interrupção.",
    "J005": "Liminar em plantão, em processo contra o Estado (0801596-93), autorizou a interrupção, feita em 15/04/2022 (J005). Em processo separado contra a operadora (0801632-38): sentença procedente (J006), apelações desprovidas (J007) e recurso especial inadmitido (J008). A ligação vem do J006, que registra a autorização por liminar no processo contra o Estado.",
    "J046": "HC da Defensoria no TJRJ: liminar satisfativa e ordem concedida (J046). Terceiros impetraram HC no STJ em favor do nascituro contra a liminar; julgado prejudicado porque a interrupção já fora feita (J013). O despacho J012, do mesmo HC, está em documentos_de_contexto.csv.",
    "J069": "O TJSC manteve a sentença que negou o alvará (J069). No STJ, a liminar do HC foi indeferida (J014) e o HC, julgado prejudicado na 43ª semana de contagem gestacional (J015).",
    "J016": "O TJES negou o alvará (R002, fora da busca). No STJ, a liminar do HC foi indeferida (J016) e o HC, depois, julgado prejudicado (J017).",
    "J019": "A sentença indeferiu o alvará (J019). A apelação foi julgada em 2025 com perda superveniente do objeto (J020).",
    "J054": "MS do MP contra liminar da 1ª Vara Criminal de Carazinho que autorizou a interrupção pelo SUS. A 2ª Câmara Cível declinou da competência (J054); a 3ª Câmara Criminal denegou a segurança e manteve a autorização (J053).",
    "J066": "Apelações em ação cautelar e ação principal de família (mesmo relator, mesma data, ementas idênticas). Falso positivo.",
    "J100": "A sentença negou por taxatividade (J100). O MS da Defensoria foi concedido no 2º grau, com convalidação da liminar (J120).",
    "J102": "A sentença negou (J102). No MS do casal, a liminar foi concedida; depois a Câmara julgou o pedido prejudicado, porque a autorização já fora dada (J121). Desfecho tirado da liminar relatada no J121.",
    "J122": "Dois HCs do mesmo advogado, para a mesma paciente, impetrados direto no tribunal: não conhecidos por falta de pedido em 1º grau e de documentos (J122) e por reiteração (J112). Não houve decisão sobre o mérito em nenhuma instância.",
    "J114": "Ação indenizatória por laqueadura sem exame de gravidez: apelações (J114) e embargos de declaração (J113). A criança, com T18, nasceu e morreu; não há pedido de interrupção.",
    "J130": "Sentença do DIPO de 17/09/1997 autorizou a interrupção por analogia (fora do corpus). O MP impetrou MS para dar efeito suspensivo à apelação, julgado prejudicado porque a cirurgia já fora feita (J130), e a apelação do MP também foi julgada prejudicada (J129). Desfecho tirado da sentença relatada.",
    "J031": "A tutela antecipada recursal foi deferida no agravo; depois o relator negou seguimento por prejudicialidade, a pedido dos próprios agravantes. Desfecho tirado da tutela relatada.",
}

def dt(s):
    try: return datetime.datetime.strptime(s, "%d/%m/%Y").date()
    except ValueError: return None

def origem(r):  # resultado da decisão de origem relatado no resumo de um julgado de 2º grau ou STJ
    if r["instancia"] == "1º grau": return None
    m = re.search(r"contra (a |o )?(decisão|sentença|acórdão|liminar|tutela)([^.;]{0,220})", r["resumo_do_julgado"])
    if not m: return None
    t = m.group(3)
    k = re.search(r"\b(negou|indeferiu|julgou improcedente|manteve o indeferimento|autorizou|autorizara|extinguiu)\b", t)
    if not k: return None
    v = k.group(1)
    if v in ("autorizou", "autorizara"): return "Autorizado"
    if v == "extinguiu": return "Extinto sem mérito"
    return "Negado"

COPIA = ["instancia", "orgao_julgador", "via_processual", "art128_I", "fundamento_risco_vida_gestante",
         "fundamento_inviabilidade_extrauterina", "fundamento_dignidade_autonomia", "comparacao_com_anencefalia",
         "cita_adpf54", "cita_hc_932495", "forma_do_texto", "perda_de_objeto"]
EF = {"Autoriza": "Autorizado", "Nega": "Negado"}
in_g = {j for g in GRUPOS for j in g}
casos_j = []
for r in rows:
    j = r["id_julgado"]
    if j in in_g:
        g = next(g for g in GRUPOS if j in g)
        if g not in casos_j: casos_j.append(g)
    else:
        casos_j.append([j])

def prio(vals, ordem):
    for o in ordem:
        if o in vals: return o
    return vals[0]

saida, id_de = [], {}
for k, g in enumerate(casos_j, 1):
    cid = f"C{k:03d}"; rs = [J[j] for j in g]
    for j in g: id_de[j] = cid
    fps = {r["falso_positivo"] for r in rs}
    no_escopo = "Sim" if "Não" in fps else ("Não" if fps == {"Sim"} else "Não acessível")
    uniq = lambda xs: list(dict.fromkeys(x for x in xs if x not in AUS))
    procs = uniq(r["n_processo"] for r in rs)
    for rf in refs:
        if rf["forma_da_referencia"] in ("Processo de origem", "Processo conexo") and set(rf["citado_em"].split("; ")) & set(g):
            p = f"{rf['n_processo']} ({rf['id_referencia']})"
            if p not in procs: procs.append(p)
    cond = prio([r["condicao_fetal"] for r in rs], ["T18", "Múltipla", "T13 (Patau)", "Anencefalia", "Outra", "Não consta", "Não acessível", "Não aplicável"])
    forma = prio([r["forma_citogenetica"] for r in rs], ["Mosaico", "Trissomia completa", "Não consta", "Não acessível", "Não aplicável"])
    r_ig = next((r for r in rs if re.fullmatch(r"\d+", r["idade_gestacional_semanas"])), None)
    ig = r_ig["idade_gestacional_semanas"] if r_ig else "Não consta"
    ig_mom = r_ig["momento_idade_gestacional"] if r_ig else "Não consta"
    # data da última decisão: julgamento; se ausente, publicação do mesmo julgado (anotado)
    nota_data = ""
    if dt(rs[-1]["data_julgamento"]): d_ult = rs[-1]["data_julgamento"]
    elif dt(rs[-1]["data_publicacao"]):
        d_ult = rs[-1]["data_publicacao"]
        nota_data = f"data_ultima_decisao = data de publicação do {rs[-1]['id_julgado']}, que não traz a data de julgamento."
    else:
        d_ult = "Não consta"
        nota_data = f"data_ultima_decisao não recuperável: o {rs[-1]['id_julgado']} não traz data de julgamento nem de publicação."
    inst = " → ".join(dict.fromkeys(("STJ" if r["instancia"] == "Tribunal Superior" else r["instancia"]) for r in rs if r["instancia"] not in AUS)) or "Não acessível"
    dped = [dt(r["data_inicial"]) for r in rs if dt(r["data_inicial"])]
    djul = [dt(r["data_julgamento"]) for r in rs if dt(r["data_julgamento"])]
    # desfecho: última decisão com efeito prático; senão, decisão relatada
    com_efeito = [r for r in rs if r["efeito_pratico"] in EF]
    if g[0] in DESFECHO_RELATADO:
        desf, fonte = DESFECHO_RELATADO[g[0]]; dec = DECISIVO_RELATADO[g[0]]
    elif com_efeito:
        desf, fonte, dec = EF[com_efeito[-1]["efeito_pratico"]], "Próprio julgado", com_efeito[-1]["id_julgado"]
    elif all(r["efeito_pratico"] == "Não aplicável" for r in rs):
        desf = "Não acessível" if no_escopo == "Não acessível" else "Não decide a autorização"; fonte, dec = "Não aplicável", "Não aplicável"
    else:
        o = origem(rs[0])
        if o:
            desf = "Negado" if o == "Extinto sem mérito" else o
            fonte, dec = "Decisão de origem relatada no julgado (fora do corpus)", rs[0]["id_julgado"]
        else:
            desf, fonte, dec = "Sem decisão útil", "Não aplicável", "Não aplicável"
    # colunas copiadas do julgado decisivo (julgados.csv continua a única fonte)
    if desf in ("Não decide a autorização", "Sem decisão útil"):
        ffund, cop = "Não aplicável", {c: "Não aplicável" for c in COPIA}
    elif desf == "Não acessível":
        ffund, cop = "Não aplicável", {c: "Não acessível" for c in COPIA}
    else:
        ffund = "Julgado decisivo" if fonte == "Próprio julgado" else "Julgado que relata a decisão"
        cop = {c: J[dec][c] for c in COPIA}
    # reforma
    if rs[0]["instancia"] == "1º grau":
        ini = EF.get(rs[0]["efeito_pratico"])
        if len(rs) == 1: ini = "única"
    else:
        ini = origem(rs[0])
    if desf not in ("Autorizado", "Negado") or ini is None: reforma = "Não consta" if desf in ("Autorizado", "Negado") else "Não aplicável"
    elif ini == "única": reforma = "Não aplicável"
    elif ini in ("Negado", "Extinto sem mérito") and desf == "Autorizado": reforma = "Sim (" + ("extinto" if ini.startswith("Extinto") else "negado") + " → autorizado)"
    elif ini == "Autorizado" and desf == "Negado": reforma = "Sim (autorizado → negado)"
    elif ini == "Extinto sem mérito" and desf == "Negado": reforma = "Não"
    else: reforma = "Não" if ini == desf else "Não consta"
    if fonte.startswith("Decisão de origem"): reforma = "Não"  # o desfecho É a decisão de origem
    dias = "Não consta"
    if dped and dec in J and fonte == "Próprio julgado" and dt(J[dec]["data_julgamento"]): dias = str((dt(J[dec]["data_julgamento"]) - min(dped)).days)
    # gestação encerrada antes da decisão final
    if desf in ("Não decide a autorização", "Não acessível"): enc = "Não aplicável"
    elif set(g) & INTERRUPCAO_ANTES: enc = "Sim — interrupção"
    elif any(r["houve_parto_antes_do_fim"] == "Sim" or r["situacao_vital_na_decisao"] == "Óbito fetal" for r in rs): enc = "Sim — parto ou óbito fetal"
    else: enc = "Não consta"
    imp = next((IMPUGNACAO[j] for j in g if j in IMPUGNACAO), "Nenhuma no corpus")
    rel = "Não aplicável"
    if g[0] in RELACIONADOS: rel = f"{{{RELACIONADOS[g[0]][0]}}} — {RELACIONADOS[g[0]][1]}"
    quest = " ".join(f"[{j}] {Q[j]}" for j in g if j in Q) or "Não aplicável"
    saida.append({
        "id_caso": cid, "julgados": "; ".join(g), "n_julgados": str(len(g)), "no_escopo": no_escopo,
        "falso_positivo": "; ".join(dict.fromkeys(r["falso_positivo"] for r in rs)),
        "motivo_falso_positivo": "; ".join(dict.fromkeys(r["motivo_falso_positivo"] for r in rs)),
        "tribunais": "; ".join(dict.fromkeys(r["tribunal"] for r in rs)), "uf": "; ".join(uniq(r["uf"] for r in rs)) or "Não consta",
        "comarca_origem": next((r["comarca"] for r in rs if r["comarca"] not in AUS), "Não consta"),
        "processos": "; ".join(procs), "condicao_fetal": cond, "forma_citogenetica": forma, "ig_semanas": ig, "ig_momento": ig_mom,
        "instancias_percorridas": inst,
        "data_pedido": min(dped).strftime("%d/%m/%Y") if dped else "Não consta",
        "data_primeira_decisao": rs[0]["data_julgamento"] if dt(rs[0]["data_julgamento"]) else "Não consta",
        "data_ultima_decisao": d_ult,
        "dias_ate_decisao_util": dias, "desfecho_final": desf, "julgado_decisivo": dec, "fonte_do_desfecho": fonte,
        "fonte_dos_fundamentos": ffund, **cop,
        "houve_reforma": reforma, "gestacao_encerrada_antes_da_decisao_final": enc, "impugnado_por": imp,
        "caso_relacionado": rel, "questionamentos": quest, "observacao": " ".join(x for x in (OBS.get(g[0], ""), nota_data) if x),
    })

COMARCA = {"J005": "Mossoró (ação contra a operadora); a liminar contra o Estado saiu no plantão de Natal"}
for s_ in saida:
    if s_["julgados"].split("; ")[0] in COMARCA: s_["comarca_origem"] = COMARCA[s_["julgados"].split("; ")[0]]

# resolve caso_relacionado para id_caso
for s in saida:
    s["caso_relacionado"] = re.sub(r"\{(J\d{3})\}", lambda m: id_de[m.group(1)], s["caso_relacionado"])
    if not s["observacao"]: s["observacao"] = "Não aplicável"

cols = list(saida[0])
with open(os.path.join(OUT, "casos.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(saida)

jcols = [c for c in rows[0] if c != "id_caso"]; jcols.insert(1, "id_caso")  # aceita julgados.csv com ou sem id_caso
with open(os.path.join(OUT, "julgados.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, jcols); w.writeheader()
    for r in rows: w.writerow({**r, "id_caso": id_de[r["id_julgado"]]})

# validação
assert len(id_de) == len(rows) and sum(int(s["n_julgados"]) for s in saida) == len(rows)
print(len(saida), "casos;", sum(s["no_escopo"] == "Sim" for s in saida), "no escopo")
