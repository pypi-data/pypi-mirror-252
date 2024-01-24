# ruff: noqa: A003, D100, D101, D102, D103, D104, D105, D107
from __future__ import annotations

from typing import Any, Callable, Generic, Protocol, Sequence, TypeAlias, TypeGuard

from immutable import Immutable
from typing_extensions import TypeVar


class BaseAction(Immutable):
    ...


class BaseEvent(Immutable):
    ...


class EventSubscriptionOptions(Immutable):
    run_async: bool = True


# Type variables
State = TypeVar('State', bound=Immutable, infer_variance=True)
Action = TypeVar('Action', bound=BaseAction, infer_variance=True)
Event = TypeVar('Event', bound=BaseEvent, infer_variance=True)
Event2 = TypeVar('Event2', bound=BaseEvent, infer_variance=True)
SelectorOutput = TypeVar('SelectorOutput', infer_variance=True)
ComparatorOutput = TypeVar('ComparatorOutput', infer_variance=True)
Comparator = Callable[[State], ComparatorOutput]
EventHandler = Callable[[Event], Any] | Callable[[], Any]


class CompleteReducerResult(Immutable, Generic[State, Action, Event]):
    state: State
    actions: Sequence[Action] | None = None
    events: Sequence[Event] | None = None


ReducerResult = CompleteReducerResult[State, Action, Event] | State
ReducerType = Callable[[State | None, Action], ReducerResult[State, Action, Event]]

AutorunOriginalReturnType = TypeVar('AutorunOriginalReturnType', infer_variance=True)


class InitializationActionError(Exception):
    def __init__(self: InitializationActionError, action: BaseAction) -> None:
        super().__init__(
            f"""The only accepted action type when state is None is "InitAction", \
action "{action}" is not allowed.""",
        )


class InitAction(BaseAction):
    ...


class FinishAction(BaseAction):
    ...


class FinishEvent(BaseEvent):
    ...


def is_reducer_result(
    result: ReducerResult[State, Action, Event],
) -> TypeGuard[CompleteReducerResult[State, Action, Event]]:
    return isinstance(result, CompleteReducerResult)


def is_state(result: ReducerResult[State, Action, Event]) -> TypeGuard[State]:
    return not isinstance(result, CompleteReducerResult)


class Scheduler(Protocol):
    def __call__(self: Scheduler, callback: Callable, *, interval: bool) -> None:
        ...


class CreateStoreOptions(Immutable):
    auto_init: bool = False
    threads: int = 5
    autorun_initial_run: bool = True
    scheduler: Scheduler | None = None
    action_middleware: Callable[[BaseAction], Any] | None = None
    event_middleware: Callable[[BaseEvent], Any] | None = None


class AutorunType(Protocol, Generic[State]):
    def __call__(
        self: AutorunType,
        selector: Callable[[State], SelectorOutput],
        comparator: Callable[[State], Any] | None = None,
        *,
        default_value: AutorunOriginalReturnType | None = None,
        initial_run: bool = True,
    ) -> AutorunDecorator[State, SelectorOutput, AutorunOriginalReturnType]:
        ...


class AutorunDecorator(
    Protocol,
    Generic[State, SelectorOutput, AutorunOriginalReturnType],
):
    def __call__(
        self: AutorunDecorator,
        func: Callable[[SelectorOutput], AutorunOriginalReturnType]
        | Callable[[SelectorOutput, SelectorOutput], AutorunOriginalReturnType],
    ) -> AutorunReturnType[AutorunOriginalReturnType]:
        ...


class AutorunReturnType(Protocol, Generic[AutorunOriginalReturnType]):
    def __call__(self: AutorunReturnType) -> AutorunOriginalReturnType:
        ...

    @property
    def value(self: AutorunReturnType) -> AutorunOriginalReturnType:
        ...

    def subscribe(
        self: AutorunReturnType,
        callback: Callable[[AutorunOriginalReturnType], Any],
        *,
        immediate: bool = False,
    ) -> Callable[[], None]:
        ...


class EventSubscriber(Protocol):
    def __call__(
        self: EventSubscriber,
        event_type: type[Event],
        handler: EventHandler[Event],
        options: EventSubscriptionOptions | None = None,
    ) -> Callable[[], None]:
        ...


DispatchParameters: TypeAlias = Action | Event | list[Action | Event]


class Dispatch(Protocol, Generic[State, Action, Event]):
    def __call__(
        self: Dispatch,
        *items: Action | Event | list[Action | Event],
        with_state: Callable[[State | None], Action | Event | list[Action | Event]]
        | None = None,
    ) -> None:
        ...


class InitializeStateReturnValue(Immutable, Generic[State, Action, Event]):
    dispatch: Dispatch[State, Action, Event]
    subscribe: Callable[[Callable[[State], Any]], Callable[[], None]]
    subscribe_event: EventSubscriber
    autorun: AutorunType[State]
