python_logging
==============

Use logging decorators to minimize your project code.

---

# Configurations
You can pass your own logger by using python logging module.

It's mandatory to invoke the `logger.with_logger()` method.
Enabling your own logger is possible by invoking this method with your logger object at the beginning of the .py file, e.g. `logger.with_logger(my_logger)`.

Unless you pass your own log, the default python logger is set with it's default formatting.

---

# Possible Log Levels

Supports the same default log levels as the standard python logging library:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

## Before decorator

`@logger.before(level, Arguments)`

Logs information upon invocation of the method.
Log selected or all input information.

**Arguments**:

* `{0}`: print(s the method's *first parameter*, usually *self*.
* `{1}`: print(s the method's *second parameter*.
* `{2}`: print(s the method's *third parameter*, and so on...
* `{*args}`: print(s the **args* of the method.
* `{**kwargs}`: print(s the ***kwargs* of the method.

## After decorator

`@logger.after(level, Arguments>)`

Logs information upon invocation of the method.
Log selected arguments when the method ends.

**Arguments**:

* `{t}`: print(s the method's *run time* in seconds.
* `{rv}`: print(s the method's *return* value.
* `{exc}`: print(s *uncaught exceptions* with log level error.

---

### Usage Examples:
BEFORE:
```
@logger.before(logging.debug, "name: (param_1)%d, id: (param_2)%d"):
def somefunc(param_1, param_2):
    pass
```

When invoking the `.somefunc()` method, the following line will be written to the log **before** the function's code is executed.

=> print(s your logging formatting options and then:
`- {name: John, id: 123456789}`

---

AFTER:
```
@logger.after(logging.info, { t, rv }):
def somefunc(param1, param2):
    return result
```

When invoking the `.somefunc()` method, the following line will be written to the log **after** the function's code is executed.

=> print(s your logging formatting options and then:
`- {elasped: 2.7 , return: value}`

---
