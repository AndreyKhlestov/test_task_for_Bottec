from aiogram.dispatcher.filters.state import State, StatesGroup


class StateUser(StatesGroup):
    category_menu: State = State()
    subcategory_menu: State = State()
    choice_product: State = State()

    view_shopping_cart: State = State()
    delete_products: State = State()
    enter_address: State = State()
    confirmation_address: State = State()

    # enter_quantity_product: State = State()
    # main_menu: State = State()
