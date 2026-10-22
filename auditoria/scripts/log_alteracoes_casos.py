# Gera as linhas de alteracoes_por_celula para a mudança de casos.csv (v1 -> v2), comparando célula a célula.
# Uso: python3 log_alteracoes_casos.py <casos_antes.csv> <casos_depois.csv> <saida.csv> <numero_inicial> <julgados.csv>
import csv, sys
old = {r["id_caso"]: r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8-sig"))}
new = list(csv.DictReader(open(sys.argv[2], encoding="utf-8-sig")))
inicio = int(sys.argv[4])
import re
JUL = {r["id_julgado"]: r for r in csv.DictReader(open(sys.argv[5], encoding="utf-8-sig"))}
def fonte_ig(r):
    return next((j for j in r["julgados"].split("; ") if re.fullmatch(r"\d+", JUL[j]["idade_gestacional_semanas"])), "Não aplicável")
COP = {"fonte_dos_fundamentos", "instancia", "orgao_julgador", "via_processual", "art128_I", "fundamento_risco_vida_gestante",
       "fundamento_inviabilidade_extrauterina", "fundamento_dignidade_autonomia", "comparacao_com_anencefalia",
       "cita_adpf54", "cita_hc_932495", "forma_do_texto", "perda_de_objeto"}
out, n = [], inicio
for r in new:
    o = old[r["id_caso"]]
    for k, v in r.items():
        antes = o.get(k, "(coluna nova)")
        if antes == v: continue
        if k in COP: crit, fonte = "CF", (r["julgado_decisivo"] if r["fonte_dos_fundamentos"] != "Não aplicável" else "Não aplicável")
        elif k in ("ig_semanas", "ig_momento"): crit, fonte = "IG", fonte_ig(r)
        elif k in ("data_ultima_decisao", "observacao"): crit, fonte = "DP", r["julgados"].split("; ")[-1]
        else: raise SystemExit(f"alteração sem critério: {r['id_caso']} {k}")
        out.append({"n": n, "base": "casos.csv", "registro": r["id_caso"], "campo": k, "antes": antes, "depois": v,
                    "criterio": crit, "julgado_fonte": fonte}); n += 1
with open(sys.argv[3], "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out), Counter(x["criterio"] for x in out), Counter(x["campo"] for x in out if x["criterio"] != "CF"))
