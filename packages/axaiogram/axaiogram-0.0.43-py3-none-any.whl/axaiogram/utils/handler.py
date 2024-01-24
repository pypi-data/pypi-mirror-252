from functools import wraps
from typing import Any, Callable, TypeVar, Union, Protocol
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from axaiogram.utils.types import CallbackDataQuery, PaginatedMessage


class PaginatAbleHandler(Protocol):
    async def __call__(self, *args: Any, msg: types.Message, **kwds: Any) -> Any:
        raise NotImplementedError


def _extract_and_get_event_replaceable(
    args: list, 
    kwargs: dict
) -> Union[types.Message, CallbackDataQuery]:

    for i in range(len(args)):
        if isinstance(args[i], types.Message) or isinstance(args[i], types.CallbackQuery):
            return args.pop(i)
        
    for key, value in kwargs.items():
        if isinstance(value, types.Message) or isinstance(value, types.CallbackQuery):
            return kwargs.pop(key)

    raise NotImplementedError


TPaginatAbleHandler = TypeVar('TPaginatAbleHandler', bound=Callable)  #, bound=PaginatAbleHandler)


def extract_paginate_page(
    separator: str = "_page:", 
    loading_msg: str = '...', 
    only_start_loading: bool = True,
    default_page=1,
):
    def inner(f: TPaginatAbleHandler) -> TPaginatAbleHandler:
        @wraps(f)
        async def wrapper(*args_, **kwargs_):
            args = list(args_)
            kwargs = dict(kwargs_)
            event= _extract_and_get_event_replaceable(args, kwargs)
            
            if not isinstance(event, types.CallbackQuery):
                state: FSMContext = kwargs.pop('state', None)
                msg = (
                    await event.answer(loading_msg)
                    if not (
                        state
                        and event.from_user
                        and state.key.bot_id != event.from_user.id 
                    )
                    else event
                )
                event_message = PaginatedMessage(user_message=event, cq=None, page=default_page, loading=msg)  # type: ignore
            else:
                new_data, *page = event.data.split(separator)
                page = ''.join(page)
                page = int(page) if page.strip().isdigit() else default_page
                if not only_start_loading:
                    msg = await event.message.edit_text(loading_msg)
                else:
                    msg = event.message
                event = event.copy(update={'data': new_data})
                event_message = PaginatedMessage(user_message=None, cq=event, page=page, loading=msg)  # type: ignore

            return await f(*args, msg=event_message, **kwargs)

        return wrapper  # type: ignore
    return inner


def register_as_paginated_handler(
    router: Router,
    handler: Callable,
    command_filter: str,
    *filters,
) -> Router:

    router.callback_query(F.text.startswith(command_filter), *filters)(handler)
    router.message(F.text.startswith(command_filter), *filters)(handler)

    return router

