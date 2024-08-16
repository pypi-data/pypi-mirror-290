import json
import sys
from typing import IO, Optional

from geewiz.progress import ProgressIncrementer, ProgressState


class Client:
    last_card_attrs: Optional[dict] = None

    def __init__(self, input: IO[str] = sys.stdin, output: IO[str] = sys.stdout):
        self.input = input
        self.output = output
        self.variables = VarCache(self)
        self.var = VarCacheProxy(self.variables)
        self.progress = ProgressIncrementer()
        self.progress.on_update = lambda progress_state: self.update_progress(
            progress_state
        )

    def update_progress(self, progress_state: ProgressState):
        self.var.progress = progress_state
        self.resend_last_card()

    def set_input(self, input: IO[str]):
        self.input = input

    def set_output(self, output: IO[str]):
        self.output = output

    def set(self, title):
        self.command("set", title=title)

    def var_command(self, name, value):
        self.command("var", name=name, value=value)
        return value

    def card(self, id=None, var=None, steps: Optional[int] = None, **kwargs):
        id_kwargs = {"id": id} if id else {}

        if steps is not None:
            self.progress.reset(steps)

        var = var or {}
        for name, value in var.items():
            self.variables[name] = value

        attrs = dict(**kwargs, **id_kwargs)

        self.command("card", **attrs, responseFormat="json")

        self.last_card_attrs = attrs

        return self.read_response()

    def read_response(self):
        response = self.input.readline()
        return json.loads(response)

    def resend_last_card(self):
        if self.last_card_attrs is not None:
            return self.card(**self.last_card_attrs)

    def get_user_config(self, key):
        self.command("getUserConfig", key=key)
        return self.read_response()

    def command(self, command, **kwargs):
        self.output.write(f"@{GeewizJsonEncoder().encode([command, kwargs])}\n")
        self.output.flush()


class VarCache(dict):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client

    def __setitem__(self, key, value):
        self.client.var_command(key, value)
        super().__setitem__(key, value)

    # TODO: implement 'update' and other methods that modify items


class VarCacheProxy:
    def __init__(self, cache: VarCache):
        super().__setattr__("cache", cache)

    def __getattr__(self, name):
        return self.cache[name]

    def __setattr__(self, name, value):
        self.cache[name] = value

    def __getitem__(self, name):
        return self.cache[name]

    def __setitem__(self, name, value):
        self.cache[name] = value


class GeewizJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Geewiz objects."""

    def default(self, o):
        if hasattr(o, "as_json"):
            return o.as_json()

        if hasattr(o, "__dict__"):
            return o.__dict__

        return super().default(o)
