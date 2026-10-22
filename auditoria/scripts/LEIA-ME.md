# Scripts

Os dois scripts usam só Python 3 (versão 3.8 ou superior) e nenhuma biblioteca externa.

## `build_casos.py`

Gera `casos.csv` a partir de `julgados.csv` e grava `julgados.csv` com a coluna `id_caso` na segunda posição. As ligações manuais entre julgados e as exceções estão escritas no próprio script e explicadas em `dados/metodo_planilha_de_casos.md`.

Para reproduzir a partir da raiz do repositório:

```bash
mkdir saida
cp dados/processos_referenciados.csv saida/
python3 auditoria/scripts/build_casos.py dados/julgados.csv saida/
```

Os arquivos gerados em `saida/` são idênticos, byte a byte, a `dados/casos.csv` e `dados/julgados.csv` (conferido em 22/10/2026).

## `log_alteracoes_casos.py`

Gerou `auditoria/alteracoes_por_celula_casos.csv`, comparando célula a célula a primeira versão de `casos.csv` com a versão final. A primeira versão não é publicada, porque foi substituída. O script fica como registro de como o log foi produzido.
