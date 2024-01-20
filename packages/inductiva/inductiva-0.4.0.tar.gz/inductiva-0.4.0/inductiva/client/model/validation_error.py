# coding: utf-8
"""
    InductivaWebAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from inductiva.client import schemas  # noqa: F401


class ValidationError(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        required = {
            "msg",
            "loc",
            "type",
        }

        class properties:

            class loc(schemas.ListSchema):

                class MetaOapg:

                    class items(
                            schemas.ComposedSchema,):

                        class MetaOapg:
                            any_of_0 = schemas.StrSchema
                            any_of_1 = schemas.IntSchema

                            @classmethod
                            @functools.lru_cache()
                            def any_of(cls):
                                # we need this here to make our import statements work
                                # we must store _composed_schemas in here so the code is only run
                                # when we invoke this method. If we kept this at the class
                                # level we would get an error because the class level
                                # code would be run when this module is imported, and these composed
                                # classes don't exist yet because their module has not finished
                                # loading
                                return [
                                    cls.any_of_0,
                                    cls.any_of_1,
                                ]

                        def __new__(
                            cls,
                            *_args: typing.Union[
                                dict,
                                frozendict.frozendict,
                                str,
                                date,
                                datetime,
                                uuid.UUID,
                                int,
                                float,
                                decimal.Decimal,
                                bool,
                                None,
                                list,
                                tuple,
                                bytes,
                                io.FileIO,
                                io.BufferedReader,
                            ],
                            _configuration: typing.Optional[
                                schemas.Configuration] = None,
                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict,
                                                   frozendict.frozendict, str,
                                                   date, datetime, uuid.UUID,
                                                   int, float, decimal.Decimal,
                                                   None, list, tuple, bytes],
                        ) -> 'items':
                            return super().__new__(
                                cls,
                                *_args,
                                _configuration=_configuration,
                                **kwargs,
                            )

                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[
                        MetaOapg.items,
                        dict,
                        frozendict.frozendict,
                        str,
                        date,
                        datetime,
                        uuid.UUID,
                        int,
                        float,
                        decimal.Decimal,
                        bool,
                        None,
                        list,
                        tuple,
                        bytes,
                        io.FileIO,
                        io.BufferedReader,
                    ]], typing.List[typing.Union[
                        MetaOapg.items,
                        dict,
                        frozendict.frozendict,
                        str,
                        date,
                        datetime,
                        uuid.UUID,
                        int,
                        float,
                        decimal.Decimal,
                        bool,
                        None,
                        list,
                        tuple,
                        bytes,
                        io.FileIO,
                        io.BufferedReader,
                    ]]],
                    _configuration: typing.Optional[
                        schemas.Configuration] = None,
                ) -> 'loc':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )

                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)

            msg = schemas.StrSchema
            type = schemas.StrSchema
            __annotations__ = {
                "loc": loc,
                "msg": msg,
                "type": type,
            }

    msg: MetaOapg.properties.msg
    loc: MetaOapg.properties.loc
    type: MetaOapg.properties.type

    @typing.overload
    def __getitem__(
            self,
            name: typing_extensions.Literal["loc"]) -> MetaOapg.properties.loc:
        ...

    @typing.overload
    def __getitem__(
            self,
            name: typing_extensions.Literal["msg"]) -> MetaOapg.properties.msg:
        ...

    @typing.overload
    def __getitem__(
            self, name: typing_extensions.Literal["type"]
    ) -> MetaOapg.properties.type:
        ...

    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema:
        ...

    def __getitem__(self, name: typing.Union[typing_extensions.Literal[
        "loc",
        "msg",
        "type",
    ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)

    @typing.overload
    def get_item_oapg(
            self,
            name: typing_extensions.Literal["loc"]) -> MetaOapg.properties.loc:
        ...

    @typing.overload
    def get_item_oapg(
            self,
            name: typing_extensions.Literal["msg"]) -> MetaOapg.properties.msg:
        ...

    @typing.overload
    def get_item_oapg(
            self, name: typing_extensions.Literal["type"]
    ) -> MetaOapg.properties.type:
        ...

    @typing.overload
    def get_item_oapg(
            self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]:
        ...

    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal[
        "loc",
        "msg",
        "type",
    ], str]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
        ],
        msg: typing.Union[
            MetaOapg.properties.msg,
            str,
        ],
        loc: typing.Union[
            MetaOapg.properties.loc,
            list,
            tuple,
        ],
        type: typing.Union[
            MetaOapg.properties.type,
            str,
        ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict,
                               frozendict.frozendict, str, date, datetime,
                               uuid.UUID, int, float, decimal.Decimal, None,
                               list, tuple, bytes],
    ) -> 'ValidationError':
        return super().__new__(
            cls,
            *_args,
            msg=msg,
            loc=loc,
            type=type,
            _configuration=_configuration,
            **kwargs,
        )
