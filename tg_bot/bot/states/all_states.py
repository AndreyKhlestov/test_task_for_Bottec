from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    test: State = State()
    main_menu: State = State()
