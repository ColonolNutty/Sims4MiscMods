import inspect
from functools import wraps


def inject_flexmethod(target_object, target_function_name):
    def _wrap_original_function(original_function, new_function):
        if hasattr(original_function, 'func'):
            @wraps(original_function)
            def _wrapped_function(*args, **kwargs):
                new_keywords = original_function.keywords.copy()
                new_keywords.update(kwargs)
                cls = original_function.args[0]
                inst = original_function.args[1]
                if len(args) > 0:
                    inst = args[0]
                return new_function(original_function.func, cls, inst, **new_keywords)
            return _wrapped_function
        else:
            @wraps(original_function)
            def _wrapped_function(*args, **kwargs):
                return new_function(original_function, *args, **kwargs)
            if not inspect.ismethod(original_function):
                return _wrapped_function
            return classmethod(_wrapped_function)

    def _injected(wrap_function):
        original_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, _wrap_original_function(original_function, wrap_function))
        return wrap_function
    return _injected
