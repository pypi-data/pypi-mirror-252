import contextvars
import datetime
import functools
import inspect
import logging
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from ..utils.text import generate_uid, shorten_str
from .serialization import Data, serialize_with_type

TRACING_FORMAT_VERSION = "3.0"

_LOG = logging.getLogger(__name__)

_TRACING_STACK = contextvars.ContextVar("_TRACING_STACK", default=())


class TracingNodeState(Enum):
    """
    An enumeration representing the state of a tracing node.
    """

    NEW = "new"
    """The tracing node has been created but has not started yet."""
    OPEN = "open"
    """The tracing node is currently running."""
    FINISHED = "finished"
    """The tracing node has successfully finished execution."""
    ERROR = "error"
    """The tracing node finished with an exception."""


@dataclass
class Tag:
    """
    A simple class representing a tag that can be applied to a tracing node. Optionally with style information.
    """

    name: str
    """The name of the tag; any short string."""
    color: Optional[str] = None
    """HTML hex color code, e.g. `#ff0000`."""

    @staticmethod
    def into_tag(obj: Union[str, "Tag"]) -> "Tag":
        if isinstance(obj, Tag):
            return obj
        if isinstance(obj, str):
            return Tag(obj)
        raise Exception(f"Object {obj!r} cannot be converted into Tag")


class TracingNode:
    """
    A tracing object that represents a single request or (sub)task in a nested hierarchy.

    The class has several attributes that are intended as read-only; use setters to modify them.

    The `TracingNode` can be used as context manager, e.g.:

    ```python
    with TracingNode("my node", inputs={"z": 42}) as c:
        c.add_input("x", 1)
        y = do_some_computation(x=1)
        # The tracing node would also note any exceptions raised here
        # (letting it propagate upwards), but a result needs to be set manually:
        c.set_result(y)
    # <- Here the tracing node is already closed.
    ```
    """

    def __init__(
        self,
        name: str,
        kind: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Data]] = None,
        tags: Optional[Sequence[str | Tag]] = None,
        storage: Optional["StorageBase"] = None,
        directory=False,
        result=None,
    ):
        """
        - `name` - A description or name for the tracing node.
        - `kind` - Indicates category of the tracing node, may e.g. influence display of the tracing node.
        - `inputs` - A dictionary of inputs for the tracing node.
        - `meta` - A dictionary of any metadata for the tracing node, e.g. UI style data.
        - `tags` - A list of tags for the tracing node
        - `storage` - A storage object for the tracing node. Set on the root tracing node to log all nodes below it.
        - `directory` - Whether to create a sub-directory for the tracing node while storing.
          This allows you to split the stored data across multiple files.
        - `result` - The result value of the tracing node, if it has already been computed.
        """

        if storage is None and current_tracing_node(False) is None:
            storage = current_storage()

        if inputs:
            assert isinstance(inputs, dict)
            assert all(isinstance(key, str) for key in inputs)
            inputs = serialize_with_type(inputs)

        if meta:
            meta = serialize_with_type(meta)

        if result:
            result = serialize_with_type(result)

        if tags is not None:
            tags = [Tag.into_tag(tag) for tag in tags]

        self.name = name
        self.kind = kind
        self.inputs = inputs
        self.result = result
        self.error = None
        self.state: TracingNodeState = (
            TracingNodeState.NEW if result is None else TracingNodeState.FINISHED
        )
        self.uid = generate_uid(name)
        self.children: List[TracingNode] = []
        self.tags: List[Tag] = tags
        self.start_time = None
        self.end_time = None if result is None else datetime.datetime.now()
        self.meta = meta
        self.storage = storage
        self.directory = directory
        self._token = None
        self._depth = 0
        self._lock = Lock()

        if storage:
            storage.register_node(self)

    @classmethod
    def deserialize(cls, data: Data, depth=0):
        """
        Deserialize a `TracingNode` object from given JSON data.

        - `data` - A dictionary containing the serialized tracing data.
        """
        assert isinstance(data, dict)

        # For backward compatibility we also "Context"
        assert data["_type"] == "TracingNode" or data["_type"] == "Context"
        self = cls.__new__(cls)
        self.uid = data["uid"]
        self.name = data["name"]

        state = data.get("state")
        if state:
            state = TracingNodeState(state)
        else:
            state = TracingNodeState.FINISHED
        self.state = state
        for name in ["kind", "inputs", "result", "error", "tags", "meta"]:
            setattr(self, name, data.get(name))
        self.kind = data.get("kind")
        self.inputs = data.get("inputs")
        self.tags = data.get("tags")

        start_time = data.get("start_time")
        if start_time is None:
            self.start_time = None
        else:
            self.start_time = datetime.datetime.fromisoformat(start_time)

        end_time = data.get("end_time")
        if end_time is None:
            self.end_time = None
        else:
            self.end_time = datetime.datetime.fromisoformat(end_time)

        children = data.get("children")
        if children is None:
            self.children = None
        else:
            new_depth = depth + 1
            self.children = [
                TracingNode.deserialize(child, depth=new_depth) for child in children
            ]

        self._token = None
        self._depth = depth
        self._lock = Lock()
        return self

    def to_dict(self, with_children=True, root=True):
        """
        Serialize `TracingNode` object into JSON structure.

        - `with_children` - If True then children are recursively serialized.
                            If False then serialization of children is skipped and only
                            children UIDs are put into key `children_uids`
        """
        with self._lock:
            result = {"_type": "TracingNode", "name": self.name, "uid": self.uid}
            if root:
                result["version"] = TRACING_FORMAT_VERSION
            if self.state != TracingNodeState.FINISHED:
                result["state"] = self.state.value
            for name in ["kind", "result", "error", "tags"]:
                value = getattr(self, name)
                if value is not None:
                    result[name] = value
            if self.inputs:
                result["inputs"] = self.inputs
            if with_children and self.children:
                result["children"] = [c.to_dict(root=False) for c in self.children]
            if not with_children and self.children:
                result["children_uids"] = [c.uid for c in self.children]
            if self.start_time:
                result["start_time"] = self.start_time.isoformat()
            if self.end_time:
                result["end_time"] = self.end_time.isoformat()
            if self.meta:
                result["meta"] = self.meta
            if self.tags:
                result["tags"] = serialize_with_type(self.tags)
            return result

    @property
    def _pad(self):
        return " " * self._depth

    def __enter__(self):
        def _helper(depth):
            with self._lock:
                assert not self._token
                assert self.state == TracingNodeState.NEW
                self.start_time = datetime.datetime.now()
                self._depth = depth
                self._token = _TRACING_STACK.set(parents + (self,))
                self.state = TracingNodeState.OPEN
                _LOG.debug(
                    f"{self._pad}TracingNode {self.kind} inputs={shorten_str(self.inputs, 50)}"
                )

        # First we need to get Lock from parent to not get in collision
        # with to_dict() that goes down the tree
        parents = _TRACING_STACK.get()
        if parents:
            parent = parents[-1]
            with parent._lock:  # noqa
                _helper(len(parents))
                parent.children.append(self)
        else:
            _helper(0)
        return self

    def __exit__(self, _exc_type, exc_val, _exc_tb):
        with self._lock:
            assert self._token
            assert self.state == TracingNodeState.OPEN
            if exc_val:
                # Do not call set_error here as it takes a lock
                self.state = TracingNodeState.ERROR
                self.error = serialize_with_type(exc_val)
                _LOG.debug(
                    f"{self._pad}-> ERR  {self.kind} error={shorten_str(exc_val, 50)}"
                )
            else:
                self.state = TracingNodeState.FINISHED
                _LOG.debug(
                    f"{self._pad}-> OK   {self.kind} result={shorten_str(repr(self.result), 50)}"
                )
            self.end_time = datetime.datetime.now()
            _TRACING_STACK.reset(self._token)
            self._token = None
        if self.storage:
            self.storage.write_node(self)
        return False  # Propagate any exception

    def add_tag(self, tag: str | Tag):
        """
        Add a tag to the tracing node.
        """
        with self._lock:
            if self.tags is None:
                self.tags = [Tag.into_tag(tag)]
            else:
                self.tags.append(Tag.into_tag(tag))

    def add_event(
        self,
        name: str,
        kind: Optional[str] = None,
        data: Optional[Any] = None,
        meta: Optional[Dict[str, Data]] = None,
        tags: Optional[List[str | Tag]] = None,
    ) -> "TracingNode":
        event = TracingNode(name=name, kind=kind, result=data, meta=meta, tags=tags)
        with self._lock:
            self.children.append(event)
        return event

    def add_input(self, name: str, value: object):
        """
        Add a named input value to the tracing node.

        If an input of the same name already exists, an exception is raised.
        """
        with self._lock:
            if self.inputs is None:
                self.inputs = {}
            if name in self.inputs:
                raise Exception(f"Input {name} already exists")
            self.inputs[name] = serialize_with_type(value)

    def add_inputs(self, inputs: dict[str, object]):
        """
        Add a new input values to the tracing node.

        If an input of the same name already exists, an exception is raised.
        """
        with self._lock:
            if self.inputs is None:
                self.inputs = {}
            for name in inputs:
                if name in self.inputs:
                    raise Exception(f"Input {name} already exists")
            for name, value in inputs.items():
                self.inputs[name] = serialize_with_type(value)

    def set_result(self, value: Any):
        """
        Set the result value of the tracing node.
        """
        with self._lock:
            self.result = serialize_with_type(value)

    def set_error(self, exc: Any):
        """
        Set the error value of the tracing node (usually an `Exception` instance).
        """
        with self._lock:
            self.state = TracingNodeState.ERROR
            self.error = serialize_with_type(exc)

    def has_tag_name(self, tag_name: str):
        """
        Returns `True` if the tracing node has a tag with the given name.
        """
        if not self.tags:
            return False
        for tag in self.tags:
            if tag == tag_name or (isinstance(tag, Tag) and tag.name == tag_name):
                return True
        return False

    def find_nodes(self, predicate: Callable) -> List["TracingNode"]:
        """
        Find all nodes matching the given callable `predicate`.

        The predicate is called with a single argument, the `TracingNode` to check, and should return `bool`.
        """

        def _helper(node: TracingNode):
            with node._lock:
                if predicate(node):
                    result.append(node)
                if node.children:
                    for child in node.children:
                        _helper(child)

        result = []
        _helper(self)
        return result

    def write_html(self, filename: str):
        from ..ui.staticview import create_node_static_page

        html = create_node_static_page(self)
        with open(filename, "w") as f:
            f.write(html)

    def display(self):
        """Show tracing in Jupyter notebook"""
        from IPython.core.display import HTML
        from IPython.display import display

        from ..ui.staticview import create_node_static_html

        html = create_node_static_html(self)
        display(HTML(html))


def with_trace(
    fn: Callable = None, *, name=None, kind=None, tags: Optional[List[str | Tag]] = None
):
    """
    A decorator wrapping every execution of the function in a new `TracingNode`.

    The `inputs`, `result`, and `error` (if any) are set automatically.
    Note that you can access the created tracing in your function using `current_tracing_node`.

    *Usage:*

    ```python
    @with_trace
    def func():
        pass

    @with_trace(name="custom_name", kind="custom_kind", tags=['tag1', 'tag2'])
    def func():
        pass
    ```
    """
    if isinstance(fn, str):
        raise TypeError("use `with_tracing()` with explicit `name=...` parameter")

    def helper(func):
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*a, **kw):
            binding = signature.bind(*a, **kw)
            with TracingNode(
                name=name or func.__name__,
                kind=kind or "call",
                inputs=binding.arguments,
                tags=tags,
            ) as node:
                result = func(*a, **kw)
                node.set_result(result)
                return result

        async def async_wrapper(*a, **kw):
            binding = signature.bind(*a, **kw)
            with TracingNode(
                name=name or func.__name__,
                kind=kind or "acall",
                inputs=binding.arguments,
            ) as node:
                result = await func(*a, **kw)
                node.set_result(result)
                return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    if fn is not None:
        assert callable(fn)
        return helper(fn)
    else:
        return helper


def current_tracing_node(check: bool = True) -> Optional[TracingNode]:
    """
    Returns the inner-most open tracing node, if any.

    Throws an error if `check` is `True` and there is no current tracing node. If `check` is `False` and there is
    no current tracing node, it returns `None`.
    """
    stack = _TRACING_STACK.get()
    if not stack:
        if check:
            raise Exception("No current tracing")
        return None
    return stack[-1]


# Solving circular dependencies
from .storage import StorageBase, current_storage  # noqa
