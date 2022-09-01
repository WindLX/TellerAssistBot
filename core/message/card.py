import datetime
import pandas as pd
from core.assist.read_data import load_help, load_information, load_tarrow, load_str2emoji
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

def create_hrace_card(hd: pd.DataFrame):
    title = Module.Header("Horse Race")
    at = "Choose one horse below and it will fight for you then."
    bt = [
            str(load_str2emoji(0, str(i))) + " **"
             + str(hd.iloc[i, 0]) + "**     " 
             + str(hd.iloc[i, 1])
             for i in range(4)
        ]
    bm = [Module.Section(Element.Text(content=bt[i], type=Types.Text.KMD), Element.Button("+ 1", value=str(i))) for i in range(4)]

    card = Card(title)
    card.append(Module.Divider())
    card.append(Module.Section(Element.Text(content=at, type=Types.Text.KMD)))
    for i in range(4):
        card.append(bm[i])
    card.append(Module.Countdown(mode=Types.CountdownMode.SECOND, start=datetime.datetime.now(), end=datetime.datetime.now()+datetime.timedelta(seconds=30)))
    card.append(Module.Divider())
    last_line = ":horse: Rush! Rush! Rush!"
    card.append(Module.Context(last_line))
    return CardMessage(card)
