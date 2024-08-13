"""Base Configuration Functionality."""
from __future__ import annotations

import json
from abc import ABC
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import Field
from typing_extensions import dataclass_transform

from .auto import BaseAutoClass
from .generic import solve_typevar
from .registry import RegisterTypes, Registrable, register_meta_mixin


@dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class _register_model_meta(register_meta_mixin, ModelMetaclass):
    """metaclass for registrable pydantic model."""


class BaseConfig(Registrable, BaseModel, metaclass=_register_model_meta):
    """Base Configuration Pydantic Model."""

    # validate default argument
    model_config = ConfigDict(validate_default=True)

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration object to dictionary."""
        return self.model_dump() | {
            "type_id": type(self).type_id,
            "__type_hash__": type(self).type_hash,
        }

    def to_json(self, **kwargs) -> str:
        """Serialize config object into json format.

        Arguments:
            **kwargs: arguments forwarded to `json.dumps`

        Returns:
            serialized_config (str): the serialized configuration string
        """
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> BaseConfig:
        """Convert dict to configuration instance.

        Arguments:
            dct (dict[str, Any]): dictionary to be converted

        Returns:
            config (BaseConfig): the constructed configuration object
        """
        dct = dct.copy()
        # pop type hash and type identifier as they are meta
        # information and not actual fields needing to be set
        h = dct.pop("__type_hash__", None)
        t = dct.pop("type_id", None)

        # make sure hashes match up
        if (h is not None) and (h != cls.type_hash):
            raise ValueError(
                "Type hash in dict doesn't match type hash of config"
            )
        # make sure type identifiers match up
        if (t is not None) and (t != cls.type_id):
            raise ValueError(
                "Type identifier in dict doesn't match type identifier "
                "of config: %s != %s" % (t, cls.type_id)
            )
        # instantiate config
        return cls(**dct)

    @classmethod
    def from_json(cls, serialized: str) -> BaseConfig:
        """Deserialize a json string into a config.

        Arguments:
            serialized (str): the serialized string in json format

        Returns:
            config (BaseConfig): the constructed configuration object
        """
        return cls.from_dict(json.loads(serialized))


class AutoConfig(BaseAutoClass[BaseConfig]):
    """Auto Configuration."""

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> BaseConfig:
        """Convert dict to configuration object of appropriate type.

        The type is inferred by the following prioritization:

        1. based on the `__type_hash__` if present in the dictionary
        2. based on the type identifier `t` if present in the dictionary
        3. use the root class, i.e. the class on which the function is called

        Arguments:
            dct (dict[str, Any]): dictionary to be converted

        Returns:
            config (BaseConfig): the constructed configuration object
        """
        if "__type_hash__" in dct:
            # get type from registry
            h = dct.get("__type_hash__")
            T = cls.type_registry.get_type_by_hash(h)

        elif "type_id" in dct:
            # get type from type id
            t = dct.get("type_id")
            T = cls.type_registry.get_type_by_t(t)

        else:
            raise TypeError(
                "Unable to resolve type of config: `%s`" % str(dct)
            )

        # create instance
        return T.from_dict(dct)

    @classmethod
    def from_json(cls, serialized: str) -> BaseConfig:
        """Load configuration from json.

        Deserialize a json string into a configuration object of
        appropriate type.

        The type is inferred by the following prioritization:

        1. based on the `__type_hash__` if present in the json string
        2. based on the type identifier `t` if present in the json string
        3. use the root class, i.e. the class on which the function is called

        Arguments:
            serialized (str): the serialized string in json format

        Returns:
            config (BaseConfig): the constructed configuration object
        """
        return cls.from_dict(json.loads(serialized))


U = TypeVar("U", bound=BaseConfig)


class BaseConfigurable(Generic[U], RegisterTypes, ABC):
    """Base class for configurable types."""

    CONFIG_TYPE: None | type[U] = None

    def __init__(self, config: None | U = None, **kwargs) -> None:
        """Initialize the configurable.

        Args:
            config (C, optional): The configuration. If not provided, a configuration
                is created based on the given keyword arguments.
            **kwargs: Additional keyword arguments that update the provided configuration
                or create a new configuration if none is provided.
        """
        if config is None:
            config = self.config_type(**kwargs)
        elif len(kwargs) is not None:
            config = config.model_copy(update=kwargs)

        if not isinstance(config, self.config_type):
            raise TypeError()

        self._config = config

    @property
    def config(self) -> U:
        """Retrieves the configuration of the object.

        Returns:
            C: The configuration object.
        """
        return self._config

    @classmethod
    def from_config(cls, config: U) -> BaseConfigurable:
        """Abstract construction method, must be implemented by sub-types.

        Arguments:
            config (T): configuration to construct the instance from

        Returns:
            inst (Configurable): instance
        """
        return cls(config)

    @classmethod
    @property
    def generic_config_type(cls) -> type[U]:
        """Config Type specified by generic type var `U`.

        Get the generic configuration type of the configurable specified
        by the type variable `U`.
        """
        # get config class
        t = solve_typevar(cls, U)
        # check type
        if (t is not None) and not issubclass(t, BaseConfig):
            raise TypeError(
                "Configurable config type `%s` doesn't inherit from `%s`"
                % (str(t), str(BaseConfig))
            )
        return t or BaseConfig

    @classmethod
    @property
    def config_type(cls) -> type[U]:
        """Get the (final) configuration type of the configurable.

        The final configuration type is specified by the `CONFIG_TYPE`
        class attribute. Falls back to the generic config type if the
        class attribute is not specified. Also checks that the concrete
        configuration type is valid, i.e. inherits the generic configuration
        type.
        """
        generic_t = cls.generic_config_type
        # concrete config type must inherit generic config type
        if (cls.CONFIG_TYPE is not None) and not issubclass(
            cls.CONFIG_TYPE, generic_t
        ):
            raise TypeError(
                "Concrete config type `%s` specified by `CONFIG_TYPE` must "
                "inherit from generic config type `%s`"
                % (cls.CONFIG_TYPE, generic_t)
            )
        # return final config type and fallback to generic
        # type if not specified
        return cls.CONFIG_TYPE or generic_t

    @classmethod
    @property
    def type_id(cls) -> str:
        """Type Identifier.

        Type identifier used in type registry. Identifier is build
        from configuration type identifier by appending `.impl`.
        """
        # TODO: what should the relation between the type ids of a
        #       configurable and it's config be
        # specify registry type identifier based on config type identifier
        return "%s.impl" % cls.config_type.type_id


V = TypeVar("V", bound=BaseConfigurable)


class BaseAutoConfigurable(BaseAutoClass[V]):
    """Base Auto Class for configurable types."""

    @classmethod
    def from_config(cls, config: BaseConfig) -> V:
        """Create instance from given config.

        Arguments:
            config (BaseConfig): configuration

        Returns:
            inst (V): instance created from config
        """
        # build type identifier of configurable corresponding
        # to the config
        t = "%s.impl" % config.type_id
        T = cls.type_registry.get_type_by_t(t)
        # create instance
        return T.from_config(config)
