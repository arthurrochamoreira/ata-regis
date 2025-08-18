from components.dashboard import DonutStatus


def make_donut_panel(*, data):
    donut = DonutStatus(data)
    donut.col = {"xs": 12, "md": 6}
    return donut
