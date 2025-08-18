from components.dashboard import MonthlyBarChart


def make_monthly_bar_panel(*, data):
    bars = MonthlyBarChart(data)
    bars.col = {"xs": 12, "md": 6}
    return bars
