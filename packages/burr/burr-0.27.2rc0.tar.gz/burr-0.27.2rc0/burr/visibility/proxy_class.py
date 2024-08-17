class ProxyClass:
    def __init__(self, wrapped_object, tracer, name=""):
        self._wrapped_object = wrapped_object
        self._tracer: TracerFactory = tracer
        self._active_spans = {}
        self._name = name

    def __getattr__(self, name):
        if name == "_wrapped_object":
            return self._wrapped_object
        elif name == "_tracer":
            return self._tracer
        elif name == "_active_spans":
            return self._active_spans
        elif name == "_name":
            return self._name
        attr = getattr(self._wrapped_object, name)

        if callable(attr):

            def hooked(*args, **kwargs):
                print(f"Calling method: {name}")
                print(f"Arguments: {args}")
                print(f"Keyword Arguments: {kwargs}")
                context_manager: ActionSpanTracer = self._tracer(f"{self._name}.{name}")
                context_manager.__enter__()
                self._active_spans[name] = context_manager
                result = attr(*args, **kwargs)
                context_manager = self._active_spans.pop(name)
                context_manager.__exit__(None, None, None)
                print(f"Result: {result}")
                return result

            return hooked
        elif isinstance(attr, object):
            return ProxyClass(attr, self._tracer, name=f"{self._name}.{name}")
        else:
            return attr
