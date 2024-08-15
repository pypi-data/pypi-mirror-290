from ddtrace import patch_all, tracer

patch_all()

from azure.functions import AppExtensionBase, Context
import typing
from logging import Logger

class TracerExtension(AppExtensionBase):
    """A Python worker extension to start Datadog tracer and insturment Azure Functions"""

    @classmethod
    def init(cls):
        print("==== version 16 ====")
        pass

    @classmethod
    def pre_invocation_app_level(cls, _logger: Logger, context: Context, _func_args: typing.Dict[str, object] = {}, *args, **kwargs) -> None:
        route_function_name = context.function_name
        print("==== adding tag to span ====")
        t = tracer.trace("azure.function")
        span = tracer.current_span()
        span.set_tag('route_function_name', route_function_name)
        span.set_tag('resource_name', route_function_name)
        cls.t = t

    @classmethod
    def post_invocation_app_level(cls, _logger: Logger, _context: Context, _func_args: typing.Dict[str, object] = {}, _func_ret: typing.Optional[object] = None, *args, **kwargs) -> None:
        print(" === ending span ===")
        cls.t.finish()
