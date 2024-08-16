from dataclasses import dataclass, field
import math
import types
from typing import Optional


class Piper:
    """A class that allows using the pipe operator to chain operations."""

    def on_pipe(self, val):
        """Handle the piping of a value."""
        raise NotImplementedError("Subclasses should implement this method.")

    def __or__(self, val):
        return self.on_pipe(val)

    def __ror__(self, val):
        return self.on_pipe(val)


@dataclass
class ProgressState:
    value: int = 0
    step_titles: list[str] = field(default_factory=list)
    max: Optional[int] = None
    per: int = 1

    def append_step(self, title: str):
        self.step_titles.append(title)

    def increment(self):
        self.value += 1

    @property
    def is_complete(self):
        return self.value >= self.max

    @property
    def all_steps(self):
        pmax = math.floor(self.max / self.per)
        current_step_idx = math.floor(self.value / self.per)

        for idx in range(0, max(pmax, len(self.step_titles))):
            is_defined = idx < len(self.step_titles)

            if idx < current_step_idx:
                completion_state = "complete"
            elif idx == current_step_idx:
                completion_state = "working"
            elif idx > current_step_idx:
                completion_state = "waiting"

            yield {
                "title": self.step_titles[idx] if is_defined else None,
                "state": completion_state,
                "step_number": idx + 1,
                "is_defined": is_defined,
                f"is_{completion_state}": True,
            }

    @property
    def steps(self):
        return [step for step in self.all_steps if step["is_defined"]]

    @property
    def undefined_steps(self):
        return [step for step in self.all_steps if not step["is_defined"]]

    def as_json(self):
        return self.__dict__ | {
            "steps": self.steps,
            "undefined_steps": self.undefined_steps,
            "is_complete": self.is_complete,
            "all_steps": list(self.all_steps),
        }


class ProgressIncrementer(Piper):
    def __init__(self):
        self.progress_state = ProgressState()

    def on_update(self, progress_state: ProgressState):
        pass

    def increment(self):
        self.progress_state.increment()
        self.on_update(self.progress_state)

    def reset(self, max: int, steps=None, per=1):
        old_progress_state = self.progress_state
        self.progress_state = ProgressState(max=max, step_titles=steps or [], per=per)

        if self.progress_state != old_progress_state:
            self.on_update(self.progress_state)

    def on_pipe(self, val):
        if isinstance(val, types.GeneratorType):
            return [x | self for x in val]

        self.increment()
        return val

    def upto(self, max: int, steps=None, per=1):
        self.reset(max, steps, per)
        return NoOp()

    @property
    def each(self):
        return Each(self)

    def step(self, step_title: str):
        self.progress_state.append_step(step_title)
        self.on_update(self.progress_state)

    def as_json(self):
        return self.progress_state.as_json()


class NoOp(Piper):
    def on_pipe(self, val):
        return val


def key_to_callable(key):
    if callable(key):
        return key

    if key is None:
        return lambda item: item

    if isinstance(key, str):
        return lambda item: getattr(item, key)


class Each(Piper):
    def __init__(self, incrementer: ProgressIncrementer):
        self.incrementer = incrementer
        self.per = 1
        self.key = None

    def on_pipe(self, items):
        key = key_to_callable(self.key)

        self.incrementer.upto(
            max=len(items) * self.per,
            steps=[key(item) for item in items],
            per=self.per,
        )
        return items

    def __call__(self, *args, per=1, key=None):
        self.per = per
        self.key = key

        match args:
            case tuple():  # e.g. items | inc.each(per=3)
                return self
            case tuple(items):  # e.g. inc.each(docs, per=3)
                return self | items  # returns items
