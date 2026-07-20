from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"

    if any(word in normalized for word in ["流失率", "流失多少人", "流失用户"]):
        churn_rate = float(metrics["流失率"])
        churn_user = int(metrics["流失人数"])
        return f"系统总流失人数为{churn_user:,}人，总体流失率为{churn_rate:.1%}。"

    if any(word in normalized for word in ["哪个品类用户最多", "偏好品类", "品类用户"]):
        max_cat_row = category_df.loc[category_df["用户数"].idxmax()]
        cat_name = max_cat_row["PreferedOrderCat"]
        cat_user = int(max_cat_row["用户数"])
        return f"用户规模最大的偏好品类是{cat_name}，该品类共有{cat_user:,}名用户。"

    if any(word in normalized for word in ["哪个阶段风险最高", "生命周期", "流失最高阶段"]):
        max_loss_row = segment_df.loc[segment_df["流失率"].idxmax()]
        stage_name = max_loss_row["TenureGroup"]
        loss_rate = float(max_loss_row["流失率"])
        return f"流失风险最高的用户生命周期阶段为{stage_name}，阶段流失率达到{loss_rate:.1%}。"

    if any(word in normalized for word in ["平均订单数", "订单均值", "订单中位数"]):
        order_mean = float(metrics["平均订单数"])
        order_median = segment_df["平均订单数"].median()
        return f"用户平均订单数均值为{order_mean:.2f}单，全生命周期用户订单中位数为{order_median:.2f}单。"

    return (
        "基础问答尚未完成。目前只能回答总用户数；"
        "请换一种更具体的问法。"
    )
