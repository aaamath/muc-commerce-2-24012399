from pathlib import Path

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{metric_map['流失率']:.1%}", "note": ""},
        {"label": "平均订单数", "value": f"{metric_map['平均订单数']:.2f}", "note": "单/人"},
    ]

    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()
    if selected_category != "全部":
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]
    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    max_loss_row = segment_df.loc[segment_df["流失率"].idxmax()]
    stage_name = max_loss_row["TenureGroup"]
    loss_rate = max_loss_row["流失率"]
    user_count = max_loss_row["用户数"]
    insight = f"风险最高生命周期阶段：{stage_name}，阶段流失率{loss_rate:.1%}，该阶段用户规模为{user_count}人。"

    seg_table = segment_df.rename(
        columns={
            "TenureGroup": "生命周期阶段",
            "用户数": "用户数",
            "流失人数": "流失人数",
            "流失率": "流失率"
        }
    )[["生命周期阶段", "用户数", "流失人数", "流失率"]]
    seg_table["流失率"] = seg_table["流失率"].map(lambda v: f"{v:.2%}")

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
        "segment_rows": seg_table.to_dict("records")
    }

__all__ = ["load_dashboard_data"]