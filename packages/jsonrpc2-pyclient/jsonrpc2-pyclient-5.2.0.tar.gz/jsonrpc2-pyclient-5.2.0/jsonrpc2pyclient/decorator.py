"""BaseClient for quickly creating typed RPC clients."""
__all__ = ("Transportable", "rpc_client", "rpc_class_method", "rpc_method")

import abc
import functools
import inspect
import re
from typing import Any, Callable, ForwardRef, Optional, TypeVar, Union

from py_undefined import Undefined
from pydantic import BaseModel, create_model

# noinspection PyProtectedMember
from pydantic.v1.typing import evaluate_forwardref

from jsonrpc2pyclient.rpcclient import AsyncRPCClient, RPCClient

BaseClient = TypeVar("BaseClient")
FunctionType = TypeVar("FunctionType", bound=Callable)
ClientType = Union[AsyncRPCClient, RPCClient]


class Transportable(abc.ABC):
    """Abstract base for RPC client class."""

    def __init__(self, client: ClientType) -> None:
        self.transport = client


def rpc_client(
    transport: ClientType,
    method_prefix: Optional[str] = None,
    method_name_overrides: Optional[dict[str, str]] = None,
) -> Callable[[BaseClient], BaseClient]:
    """Add RPC implementations for the decorated classes methods.

    :param transport: RPC transport client.
    :param method_prefix: Prefix to add to each method name.
    :param method_name_overrides: Map of function name to method name to
        call instead of the `function.__name__`.
    :return: Class wrapper.
    """
    method_name_overrides = method_name_overrides or {}

    def _wrapper(cls: BaseClient) -> BaseClient:
        for attr in dir(cls):
            if not (callable(getattr(cls, attr)) and not attr.startswith("__")):
                continue
            source = inspect.getsource(getattr(cls, attr))
            if not re.match(r"^ *(async )?def.*?\.\.\.\n$", source, re.S):
                continue
            name = method_name_overrides.get(attr) or attr
            setattr(
                cls,
                attr,
                rpc_method(transport, f"{method_prefix}{name}")(getattr(cls, attr)),
            )
        return cls

    return _wrapper


def rpc_method(
    transport: ClientType, method_name: Optional[str] = None, *, by_name: bool = True
) -> Callable[[FunctionType], FunctionType]:
    """Use decorated method signature to call RPC method on call.

    :param transport: RPC transport client.
    :param method_name: Name of the method.
    :param by_name: Flag to indicate if params are passed by name.
    :return: An implemented version of the decorated method.
    """
    return _rpc_method(method_name, by_name=by_name, transport=transport)


def rpc_class_method(
    method_name: Optional[str] = None, *, by_name: bool = True
) -> Callable[[FunctionType], FunctionType]:
    """Decorate a `Transportable` class method.

    :param method_name: Name of the method.
    :param by_name: Flag to indicate if params are passed by name.
    :return: An implemented version of the decorated method.
    """
    return _rpc_method(method_name, by_name=by_name)


def _rpc_method(
    method_name: Optional[str] = None,
    *,
    by_name: bool = True,
    transport: Optional[ClientType] = None,
) -> Callable[[FunctionType], FunctionType]:
    """Use decorated method signature to call RPC method on call.

    :param method_name: Name of the method.
    :param by_name: Flag to indicate if params are passed by name.
    :return: An implemented version of the decorated method.
    """

    def _decorator(function: FunctionType) -> FunctionType:
        signature = inspect.signature(function)

        # Create model describing method parameters.
        param_model = create_model(  # type: ignore
            f"{function.__name__}Params",
            **{
                k: (
                    resolved_annotation(v.annotation, function),
                    v.default if v.default is not inspect.Signature.empty else ...,
                )
                for k, v in signature.parameters.items()
                if k != "self"
            },
        )

        # Create model describing method result.
        result_model = create_model(
            f"{function.__name__}Result",
            result=(resolved_annotation(signature.return_annotation, function), ...),
        )

        @functools.wraps(function)
        async def _wrapper(*args: Any, **kwargs: Any) -> Any:
            args = list(args)
            self = args.pop(0)
            params_dict, transport_kwargs = _parse_params(
                param_model, *args, by_name=by_name, **kwargs
            )
            params = params_dict if by_name else list(params_dict.values())
            name = method_name if method_name is not None else function.__name__
            transport_ = transport or self.transport
            # Type ignore because mypy is wrong.
            response = await transport_.call(
                name, params, **transport_kwargs  # type: ignore
            )
            # Cast to proper return type.
            # Type ignore because mypy can't understand `create_model`.
            return result_model(result=response).result  # type: ignore

        return _wrapper  # type: ignore

    return _decorator


def resolved_annotation(annotation: Any, function: Callable) -> Any:
    """Get annotation resolved."""
    if annotation == inspect.Signature.empty:
        return Any
    globalns = getattr(function, "__globals__", {})
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return type(None) if annotation is None else annotation


def _parse_params(
    params_model: BaseModel, *args: Any, by_name: bool, **kwargs: Any
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Get method params and transport kwargs.

    :param params_model: Model describing method parameters.
    :param by_name: Determines if params are passed by name.
    :param args: Args passed to method call.
    :param kwargs: Keyword args passed to method call.
    :return: A tuple of method params, transport kwargs.
    """
    params = {}
    transport_kwargs = {}
    param_names = list(params_model.model_fields.keys())

    # Get params passed by position.
    for i, arg in enumerate(args):
        params[param_names[i]] = arg

    # Get params passed by name.
    for name, arg in kwargs.items():
        if name in param_names:
            params[name] = arg
        else:
            # If not in param names must be transport arg.
            transport_kwargs[name] = arg
    if params:
        # Don't pass undefined params.
        if by_name:
            params = {k: v for k, v in params.items() if v is not Undefined}
        else:
            params = {k: None if v is Undefined else v for k, v in params.items()}
        params = params_model.model_validate(params).model_dump(exclude_unset=True)
    return params, transport_kwargs
