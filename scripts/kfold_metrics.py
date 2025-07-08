import pandas as pd
import os

# Caminho base dos folds
base_dir = "kfold_runs"
folds = ["fold1", "fold2", "fold3"]

# Lista para armazenar os dados de cada fold
resultados = []

for fold in folds:
    path_csv = os.path.join(base_dir, fold, "results/results.csv")
    
    if os.path.exists(path_csv):
        df = pd.read_csv(path_csv)
        ultima_linha = df.iloc[-1]

        resultados.append({
            "fold": fold,
            "precision": ultima_linha["metrics/precision(B)"],
            "recall": ultima_linha["metrics/recall(B)"],
            "mAP50": ultima_linha["metrics/mAP50(B)"],
            "mAP50-95": ultima_linha["metrics/mAP50-95(B)"]
        })
    else:
        print(f"⚠️ CSV não encontrado em {fold}")

# Criar DataFrame
df_resultados = pd.DataFrame(resultados)

# Calcular média e desvio padrão
df_resultados.loc["Média"] = df_resultados.mean(numeric_only=True)
df_resultados.loc["Desvio Padrão"] = df_resultados.std(numeric_only=True)

# Exibir no terminal
print("\n📊 Resumo K-Fold YOLO:\n")
print(df_resultados)

# Salvar em arquivo CSV
df_resultados.to_csv("resumo_kfold_yolo.csv", index=False)
print("\n✅ Resultados salvos em 'resumo_kfold_yolo.csv'")

### Elencar as métricas em gráficos sobrepostos

import os
import pandas as pd
import matplotlib.pyplot as plt

def coletar_metricas_kfold(pastas_kfold, metricas=None):
    """
    Lê os arquivos de resultados (results.csv) de múltiplos folds e retorna
    um DataFrame com as métricas desejadas e uma linha extra com a média.

    Parâmetros:
    -----------
    pastas_kfold : list[str]
        Lista com os nomes das pastas dos folds (ex: ['fold1', 'fold2']).

    metricas : list[str] or None
        Lista de colunas a extrair dos resultados. Se None, detecta automaticamente.

    Retorno:
    --------
    df : pandas.DataFrame
        DataFrame contendo as métricas por fold e a linha da média.
    metricas_utilizadas : list[str]
        Lista de métricas que foram efetivamente usadas.
    """
    resultados = []

    for fold in pastas_kfold:
        csv_path = os.path.join("kfold_runs", fold, "results", "results.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            final = df.iloc[-1].copy()
            final["fold"] = fold
            resultados.append(final)
        else:
            print(f"⚠️ Não encontrado: {csv_path}")

    if not resultados:
        print("❌ Nenhum resultado válido encontrado.")
        return None, None

    df = pd.DataFrame(resultados)

    colunas_excluidas = {"epoch", "time", "fold"}
    if metricas is None:
        metricas = [col for col in df.columns if col not in colunas_excluidas and pd.api.types.is_numeric_dtype(df[col])]
    else:
        metricas = [col for col in metricas if col in df.columns]

    if not metricas:
        print("❌ Nenhuma métrica válida encontrada.")
        return None, None

    # Adiciona linha de média
    medias = df[metricas].mean()
    linha_media = {col: medias[col] for col in metricas}
    linha_media["fold"] = "kfold-média"
    df = pd.concat([df, pd.DataFrame([linha_media])], ignore_index=True)

    return df, metricas


def plotar_metricas_barras(df, metricas, saida="metricas_graficos"):
    """
    Gera gráfico de barras agrupadas com as métricas fornecidas por fold + média.

    Parâmetros:
    -----------
    df : pandas.DataFrame
        DataFrame com os folds + kfold-média e as métricas numéricas.

    metricas : list[str]
        Lista de colunas numéricas que representam as métricas a serem plotadas.

    saida : str
        Pasta onde o gráfico será salvo.
    """
    os.makedirs(saida, exist_ok=True)

    x = range(len(df["fold"]))
    bar_width = 0.8 / len(metricas)

    plt.figure(figsize=(12, 6))

    for i, metric in enumerate(metricas):
        x_pos = [p + i * bar_width for p in x]
        valores = df[metric]
        bars = plt.bar(x_pos, valores, width=bar_width, label=metric)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.01,
                f"{height:.4f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

    plt.xticks([p + (bar_width * len(metricas)) / 2 for p in x], df["fold"])
    plt.ylabel("Valor")
    plt.title("Comparação de Métricas por Fold + Média")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    nome_arquivo = "Comparacao_KFold_com_Media.png"
    plt.savefig(os.path.join(saida, nome_arquivo), dpi=300)
    plt.close()
    print(f"✅ Gráfico salvo em '{os.path.join(saida, nome_arquivo)}'")

pastas = ["fold1", "fold2", "fold3"]

metricas_escolhidas = [
    "metrics/precision(B)",
    "metrics/recall(B)",
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)"
]

df_resultado, metricas_usadas = coletar_metricas_kfold(pastas, metricas_escolhidas)

if df_resultado is not None:
    plotar_metricas_barras(df_resultado, metricas_usadas)
    