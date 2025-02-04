from aiogram.filters.state import StatesGroup, State


# Create class heritable from StateGroup for states our FSM
class FSMAdmin(StatesGroup):
    """Create instances of the State class, sequentially
    listing the possible states it will be in
    bot at different moments of interaction with the admin"""

    default_state = State()
    add_driver = State()
    delete_driver = State()
    add_admin = State()
    delete_admin = State()
    view_stats = State()

    attach_name_to_id = State()


