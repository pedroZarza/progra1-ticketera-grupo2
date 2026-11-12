import os
from datetime import datetime

from utils.layout_helpers import build_event_sales_summary

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

def save_sales_report(event):
    """Arma el resumen de ventas y lo agrega al archivo de reportes.

    Parámetros:
        event (dict): evento a consultar.

    Retorna:
        str: ruta del archivo generado.
    """
    summary = build_event_sales_summary(event)
    header = " | ".join([
        str(event["name"]),
        summary["datetime"].strftime("%d/%m/%Y %H:%M"),
        str(event["venue"]),
        str(summary["status"]),
        str(summary["total_sold"]),
        str(summary["total_capacity"]),
        str(f"${summary['revenue']:.2f}"),
    ])
    generated_at = f"\nReport timestamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}"
    lines = [generated_at, header]
    for sector in summary["sectors"]:
        lines.append(" | ".join([
            str(sector["name"]),
            str(sector["sold"]),
            str(sector["available"]),
            str(f"${sector['revenue']:.2f}"),
        ]))

    filename = "events-sales-report.txt"
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.normpath(os.path.join(REPORTS_DIR, filename))
    with open(path, "a", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return path
