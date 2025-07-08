import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metric_graphs(csv_path: str, saida: str = "metricas_graficos"):
    """
    Gera e salva gráficos de métricas do YOLO com linha fina.
    
    Parâmetros:
    - csv_path (str): Caminho para o arquivo results.csv
    - saida (str): Pasta onde os gráficos serão salvos como PNG
    """
    df = pd.read_csv(csv_path)

    os.makedirs(saida, exist_ok=True)

    metric_info = {
        "train/box_loss": "Train Box Loss",
        "train/cls_loss": "Train Class Loss",
        "train/dfl_loss": "Train DFL Loss",
        "val/box_loss": "Val Box Loss",
        "val/cls_loss": "Val Class Loss",
        "val/dfl_loss": "Val DFL Loss",
        "metrics/precision(B)": "Precisão",
        "metrics/recall(B)": "Revocação",
        "metrics/mAP50(B)": "mAP@50",
        "metrics/mAP50-95(B)": "mAP@50-95",
    }

    for key, label in metric_info.items():
        if key in df.columns:
            plt.figure(figsize=(7, 4))
            plt.plot(df["epoch"], df[key], label=label, linewidth=1.2, color="blue")
            plt.title(f"{label} por Época")
            plt.xlabel("Época")
            plt.ylabel(label)
            plt.xlim(0, 100)
            plt.grid(True, linestyle='--', linewidth=0.5)
            plt.tight_layout()
            nome_arquivo = os.path.join(saida, f"{label.replace('/', '_').replace(' ', '_')}.png")
            plt.savefig(nome_arquivo)
            plt.close()


plot_metric_graphs("runs/detect/train5/results.csv")
