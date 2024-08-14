""" Package containing classes for reading and writing configuration files. """

from .configurator import Configurator, DirNotFoundError
from .._types import AttrDict


def get_configurators(app_name: str) -> tuple[AttrDict, AttrDict]:
    """Get the application and environment configurators.

    Args:
        app_name (str): The name of the application.

    Returns:
        tuple[AttrDict, AttrDict]: The application and environment configurators.
    """
    configurator = Configurator()
    app_props = configurator.get(app_name)
    env_props = configurator.get_environment()

    return app_props, env_props


__all__ = ["Configurator", "DirNotFoundError", "get_configurators"]
