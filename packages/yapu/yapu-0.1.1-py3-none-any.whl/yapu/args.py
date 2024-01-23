from argparse import ArgumentParser, BooleanOptionalAction
import typing
from typing import Self, Any, Union, Iterable, Literal
import inspect
import dataclasses
from dataclasses import is_dataclass

class Args:
    @classmethod
    def from_parser(cls, parser: ArgumentParser) -> Self:
        assert is_dataclass(cls), f"Expected dataclass, got {cls}."
        def obj_to_dict(obj: object) -> dict[str, Any]:
            return {
                name: v
                for name in dir(obj)
                if not name.startswith("_")
                if not inspect.isclass(v:=getattr(obj, name))
                if not inspect.isfunction(v)
                if not inspect.ismethod(v)
                if not inspect.ismodule(v)
            }
        args = parser.parse_args()
        args = cls(**obj_to_dict(args))
        return args

    @classmethod
    def parse_args(cls) -> Self:
        assert is_dataclass(cls), f"Expected dataclass, got {cls}."
        parser = cls.get_parser()
        return cls.from_parser(parser)

    @classmethod
    def get_parser(cls) -> ArgumentParser:
        assert is_dataclass(cls), f"Expected dataclass, got {cls}."
        def is_optional_type(t):
            return typing.get_origin(t) is Union and type(None) in typing.get_args(t)
        parser = ArgumentParser()
        for f in dataclasses.fields(cls):
            name = "--"+f.name
            if f.type is bool:
                parser.add_argument(name, action=BooleanOptionalAction)
                continue

            kwargs = {}
            
            if is_optional_type(f.type):
                t = typing.get_args(f.type)[0]
                kwargs["required"] = False
            else:
                t = f.type
                kwargs["required"] = True

            if inspect.isclass(typing.get_origin(t)) and issubclass(typing.get_origin(t), Iterable):
                targs = typing.get_args(t)
                tori = typing.get_origin(t)
                assert all(a is targs[0] for a in targs), f"Expected homogenous type, got {t}"
                t = targs[0]
                if tori is list:
                    kwargs["nargs"] = "+"
                elif tori is tuple:
                    kwargs["nargs"] = len(targs)
                else:
                    raise NotImplementedError

            if typing.get_origin(t) is Literal:
                kwargs["choices"] = typing.get_args(t)
            
            if f.default != dataclasses.MISSING:
                kwargs["required"] = False
                kwargs["default"] = f.default
            
            parser.add_argument(name, **kwargs)
        return parser