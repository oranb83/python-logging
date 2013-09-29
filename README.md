python_logging
==============

Use logging decorators to minimize your project code.

---

# Configurations
You can pass your own logger by using python logging module.

It's mandatory to invoke the `@logger.with_logger()` method.  
Enabling your own logger is possible by invoking this method with your logger object at the beginning of the .py file, e.g. `@logger.with_logger( my_logger )`.

Unless you pass your own log, the default python logger is set with it's default formatting.

---

# Possible Log Levels

Supports the same default log levels as the standard python logging library:  

* DEBUG  
* INFO  
* WARNING  
* ERROR  
* CRITICAL

---

## @logger.before(<<l>level>, <<l>Arguments>)

Logs information upon invokation of the method.  
Log selected or all input information.

**Arguments**:  

* `{0}`: prints the method's *first parameter*, usually *self*.  
* `{1}`: prints the method's *second parameter*.  
* `{2}`: prints the method's *third parameter*, and so on...
* `{*args}`: prints the **args* of the method.  
* `{**kwargs}`: prints the ***kwargs* of the method.

---

## @logger.after(<<l>level>, <<l>Arguments>)

Logs information upon invokation of the method.
Log selected arguments when the method ends.

**Arguments**:  

* `{t}`: prints the method's *run time* in seconds.
* `{rv}`: prints the method's *return* value.
* `{exc}`: prints *uncaught exceptions* with log level error.

---

### Usage Examples:
BEFORE:  
```
@logger.before( debug, { 0, 1 } ):  
def somefunc( param1 = value1, param2 = value2 ):  
    pass
```

=> prints your formatting options and then:  
`- {param1: value1, param2: value2}`

---

AFTER:  
```
@logger.after( info, { t, rv } ):  
def somefunc( param1, param2 ):  
    return result
```

=> prints your formatting options and then:  
`- {elasped: 2.7 , return: value}`

---

