import datetime
from core.assist.read_data import load_help, load_information, load_tarrow
from khl.card import Card, Module, Element, CardMessage, Color, Types, Struct

def create_help_card():
    data = load_help()

    title = Module.Header("Help")
    content = [Module.Section(Element.Text(content=elt, type=Types.Text.KMD)) for elt in data]

    card = Card(title)
    card.append(Module.Divider())
    for element in content:
        card.append(element) 
    card.append(Module.Divider())
    last_line = "version " + load_information('version')
    card.append(Module.Context(last_line))
    return CardMessage(card)

def create_div_card(num: int, name: str):
    data = []
    if num >= 22:
        data.append(str(load_tarrow(0, num - 22)) + "?")
        data.append(":arrows_counterclockwise::" + str(load_tarrow(1, num - 22)) + ":")
    else:
        data.append(str(load_tarrow(0, num)))
        data.append(":" + str(load_tarrow(1, num)) + ":")
    data.append(str(load_tarrow(2, num)))
    dt = ":calendar: " + str(datetime.date.today())
    nt = ":raised_hands: @" + name
    rt = ":six_pointed_star: **" + data[0] + "**"
    it = ":scroll: " + data[2]

    title = Module.Header("Today's divination")

    card = Card(title)
    card.append(Module.Divider())
    card.append(Module.Section(Element.Text(content=dt, type=Types.Text.KMD)))
    card.append(Module.Section(Element.Text(content=nt, type=Types.Text.KMD)))
    card.append(Module.Section(Element.Text(content=rt, type=Types.Text.KMD)))
    card.append(Module.Section(Element.Text(content=it, type=Types.Text.KMD)))
    card.append(Module.Divider())
    last_line = data[1] + " Just for fun, don't be serious."
    card.append(Module.Context(last_line))

    return CardMessage(card)
