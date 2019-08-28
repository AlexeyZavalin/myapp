from functools import reduce
from settings import INSTALLED_MODULES


def get_server_actions():
    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_MODULES, []
    )
    submodules = reduce(
        lambda value, item: value + [getattr(item, 'actions', [])],
        modules, []
    )
    actionnames = reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        submodules, []
    )
    return {
        item.get('action'): item.get('controller') for item in actionnames
    }


def resolve(action_name, actions=None):
    actionnames = actions or get_server_actions()
    return actionnames.get(action_name)
