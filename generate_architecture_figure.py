from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

output = Path("results/big_data_architecture.png")
output.parent.mkdir(exist_ok=True)
figure, axis = plt.subplots(figsize=(14, 5.2))
axis.set_xlim(0, 14)
axis.set_ylim(0, 5.2)
axis.axis("off")

steps = [
    ("Job sources", "JSON demo\nfuture APIs"),
    ("Ingestion", "load + validate\ndata quality"),
    ("Knowledge base", "resume + GitHub\npreferences chunks"),
    ("Hybrid RAG", "BM25 + dense\nevidence retrieval"),
    ("Matching", "hard gates +\n7-factor score"),
    ("Recommendation", "rank + evidence\nagent actions"),
    ("Interface", "Streamlit\ncharts + feedback"),
]
colors = ["#d9edf2", "#d7eadf", "#f6e3c4", "#eadcf2", "#f5d4cc", "#d8e3f4", "#e3e8d4"]
width = 1.65
for index, ((title, detail), color) in enumerate(zip(steps, colors)):
    x = 0.25 + index * 1.95
    box = FancyBboxPatch((x, 1.75), width, 1.55, boxstyle="round,pad=0.04,rounding_size=0.06", linewidth=1.2, edgecolor="#29434e", facecolor=color)
    axis.add_patch(box)
    axis.text(x + width / 2, 2.75, title, ha="center", va="center", fontsize=10, fontweight="bold")
    axis.text(x + width / 2, 2.18, detail, ha="center", va="center", fontsize=8)
    if index < len(steps) - 1:
        axis.annotate("", xy=(x + 1.91, 2.52), xytext=(x + width + 0.05, 2.52), arrowprops={"arrowstyle": "->", "lw": 1.4, "color": "#29434e"})
axis.text(7, 4.35, "Final Big Data Job Search Architecture", ha="center", fontsize=16, fontweight="bold", color="#183642")
axis.text(7, 0.75, "Current MVP: local JSON and in-memory processing | Future scale: APIs, Spark, streaming, embeddings, vector database", ha="center", fontsize=9, color="#4d626b")
figure.savefig(output, dpi=180, bbox_inches="tight")
plt.close(figure)
print(output)
