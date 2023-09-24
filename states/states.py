from aiogram.dispatcher.filters.state import StatesGroup, State


class EditChat(StatesGroup):
    EC1 = State()


class MultiEdit(StatesGroup):
    EC1 = State()


class AddAccount(StatesGroup):
    A1 = State()
    A2 = State()
    A3 = State()
    A4 = State()
    A5 = State()
    A6 = State()



class AddChat(StatesGroup):
    A1 = State()
    A2 = State()


class SendMessageState(StatesGroup):
    A1 = State()
    A2 = State()


class GiveTime(StatesGroup):
    GT1 = State()
    GT2 = State()


class TakeTime(StatesGroup):
    T1 = State()
    T2 = State()


class BroadcastState(StatesGroup):
    BS1 = State()
    BS2 = State()
    BS3 = State()
    BS4 = State()
