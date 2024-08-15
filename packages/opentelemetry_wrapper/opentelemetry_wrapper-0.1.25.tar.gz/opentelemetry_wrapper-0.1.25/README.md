# opentelemetry_wrapper

a wrapper around `opentelemetry` and `opentelemetry-instrumentation-*` to make life a bit easier

## design principles

### safe

* **never crash the application**
    * fallback to non-`opentelemetry` if necessary
    * ignore input over raising an exception
    * possible exception: it may be better to fail at startup than to run with known bad config
        * https://opentelemetry.io/docs/specs/otel/error-handling/#basic-error-handling-principles
    * make dangerous things impossible (by design) > difficult (guardrails) > unusual (defaults) > understood (docs)
        * there should be a "best practice" somewhere in that statement
* **hard to get wrong**
    * idempotent, even when you instrument the same thing in different ways from different places
    * "be conservative in what you send, be liberal in what you accept"
    * note: easy and simple mean different things

### unsurprising

* **simple, idiomatic, succinct, and pretty**
    * decorators over wrappers
    * wrappers over context managers
    * context mangers over ~~manually managing spans~~ anything else *(note: this is still a todo)*
* **reasonable documented defaults**
    * magic may be hard to understand, but it's better than being irritating
* **emits zero logs/spans (of its own) at runtime**
    * fail silently over flailing noisily
    * drowning out real logs can be worse than being useless (e.g., you could crash `fluentd` - ask me how I know)

### helpful

* **machine-readable first, human-readable a close second**
    * no newlines in logs or spans
    * no whitespace-delimited ambiguity
    * json all the things (within reason)
* **provide all available application context**
    * we want to know all we can about what's going on and where
    * code introspection and runtime analysis if we can make it fast enough

## usage

> **TL;DR:** <br>
> 1. call `instrument_all()` to instrument `logging` and `requests`
> 2. instrument your FastAPI app using `instrument_fastapi_app(FastAPI(...))`
> 3. use `@instrument_decorate` on any function or class you want to monitor
> 4. set `OTEL_WRAPPER_DISABLED=true` in your CICD tests, especially if you're using `pytest`

### env vars

| Variable Name                         | Description                                                                                                                                                                             | Default (if not set)                                                                                    |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT`         | Looks like `http://tempo.localhost:4317`.                                                                                                                                               | *NA* (traces are not exported to any OTLP endpoint)                                                     |
| `OTEL_EXPORTER_OTLP_HEADER`           | Looks like `Header-Name=header value`, where values can contain space ('\x20'). To insert multiple headers, delimit by any other whitespace char.                                       | *NA* (no header sent to OTLP endpoint)                                                                  |
| `OTEL_EXPORTER_OTLP_HEADER_SEPARATOR` | E.g. use `;` and then set `OTEL_EXPORTER_OTLP_HEADER=a=1;b=2` to send headers `a=1` and `b=2`                                                                                           | `\t` (HORIZONTAL TAB)                                                                                   |
| `OTEL_EXPORTER_OTLP_INSECURE`         | Set to `true` to disable SSL for OTLP trace exports, or `false` to always verify.                                                                                                       | *NA* (follows OpenTelemetry default, which is secure for https and insecure for http)                   |
| `OTEL_EXPORTER_PROMETHEUS_PORT`       | The port on which to expose metrics for Prometheus, running in parallel as a WSGI app. (E.g. `9464` to expose `http://localhost:9464/*`) WARNING: do not use the same port as your app. | *NA* (no Prometheus server)                                                                             |
| `OTEL_EXPORTER_PROMETHEUS_ENDPOINT`   | An endpoint on which to expose metrics for Prometheus via FastAPI. (E.g. `/metrics`) WARNING: this can clash with your fastapi routes.                                                  | `/metrics` (set to a space ` ` to avoid creating a Prometheus endpoint)                                 |
| `OTEL_HEADER_ATTRIBUTES`              | List of HTTP headers to extract from incoming requests as span attributes, split by comma.                                                                                              | `x-userinfo`                                                                                            |
| `OTEL_LOG_LEVEL`                      | Log level used by the logging instrumentor (case-insensitive).                                                                                                                          | `info`                                                                                                  |
| `OTEL_SERVICE_NAME`                   | Sets the value of the `service.name` resource attribute.                                                                                                                                | f'{k8s namespace}/{k8s deployment}/{k8s pod}' or f'{username}@{hostname}.{domain}:<{filename of main}>' |
| `OTEL_SERVICE_NAMESPACE`              | Sets the value of the `service.namespace` resource attribute.                                                                                                                           | f'{k8s namespace}' or None                                                                              |
| `OTEL_WRAPPER_DISABLED`               | Set to `true` to disable tracing globally (e.g. when running pytest).                                                                                                                   | `false` (tracing is enabled)                                                                            |

> **Note:**
>
> The `service.name` and `service.namespace` can also be set via `OTEL_RESOURCE_ATTRIBUTES`, but any settings there
> will be overwritten by `OTEL_SERVICE_NAME` and `OTEL_SERVICE_NAMESPACE`. For more details, read the
> original [OpenTelemetry docs](https://opentelemetry.io/docs)
>
> If you don't have a `serviceAccount` mounted in your pod (i.e. `automountServiceAccountToken: false`),
> then you should manually set `OTEL_SERVICE_NAMESPACE` using the following yaml:
> ```yaml
>  env:
>    - name: OTEL_SERVICE_NAMESPACE
>      valueFrom:
>        fieldRef:
>          fieldPath: metadata.namespace
> ```
> [K8s docs](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/)

### `@instrument_decorate` decorator for functions and classes

* decorating a function creates a span whenever the function is called
    * the span name is set to the function or class name, and attributes are added for the filename, line number, etc
* also works for async functions
* also works for classes and dataclasses
    * creates a span for every method call, including __init__ (or __post_init__), __new__, and __call__
    * creates a span for every property get, set, or delete
    * if this is too verbose, feel free to decorate specific methods in the class instead
* it is not recommended to use this on functions that are called thousands of times or classes you create thousands of
  instances for (e.g. pydantic classes, usually), since it can be excessively noisy

```python
from opentelemetry_wrapper import instrument_decorate


@instrument_decorate
def square(x):
    return x * x


@instrument_decorate
async def cube(x):
    return x * x * x


@instrument_decorate
class Thing:
    def __init__(self):
        self.x = 1
```

### instrumenting the builtin `logging` module

* sets a root logger handler (or more than one) that can output logs to the console or to a file path
* logs are output as json by default to make them easier to work with downstream, set `print_json=False` to disable
    * the `verbose` parameter has no effect on json output, which is maximally verbose
    * otherwise, it defaults to `True` - set to `False` to print less text to the console
* the log level can be specified via the `level` arg, but defaults to whatever was set via
  the `OTEL_LOG_LEVEL` [env var](#env-vars)

```python
import logging
from opentelemetry_wrapper import instrument_logging

instrument_logging()

logging.warning('...')
```

### instrumenting fastapi

* Warning: using `opentelemetry.instrumentation.fastapi.FastAPIInstrumentor` does not work as intended
* use `instrument_fastapi_app`, for example:

```python
from fastapi import FastAPI
from opentelemetry_wrapper import instrument_fastapi_app

app = instrument_fastapi_app(FastAPI(...))
```

Capturing headers:

* to avoid capturing any headers as spans, set a blank header, like `OTEL_HEADER_ATTRIBUTES=,`
* `OTEL_HEADER_ATTRIBUTES` will attempt to parse base64 and json, and will flatten the data structure
* `OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST` behaves similarly, but does not flatten the structure

### prometheus

[//]: # (TODO: rewrite these docs)

* set (for example) `OTEL_EXPORTER_PROMETHEUS_ENDPOINT=/metrics`
* remember to whitelist `/metrics` in OPA
* repeated and trailing slashes are normalized (e.g. `///metrics/` -> `/metrics`)
* if you set `OTEL_EXPORTER_PROMETHEUS_ENDPOINT=/metrics/`, a redirect will be set up from `/metrics` to `/metrics/`
* if you set the port instead, the created wsgi app accepts any endpoint
* if you set up both, the endpoint will be created in fastapi and a separate wsgi app will also be created
* the `/graph` endpoint is not available, you'll need to actually run prometheus to get that

## features

* Make instrumentation (more) idempotent:
    * you can call the instrument functions unlimited times from multiple places in your codebase, and it'll work the
      same
    * e.g., a class definition, a defined method of the class, a class instance, and a method from the instance
* Make re-instrumentation of `logging` actually work when passing in a new format string
* Make `logging` print as a one-line JSON dict by default, with a lot of magic to convert stuff to valid json
* logs and spans contain info about which thread / process and which file / function / line of code it came from
    * and the k8s namespace and pod, if applicable, otherwise the local pc name
* Provide support for decorating functions and classes
* Provide support for instrumentation of dataclasses
    * NOTE: Global instrumentation needs to be run *before* any dataclasses are initialized
    * Otherwise, use the decorator on each class as usual (since it is idempotent anyway)
* Add global instrumentation of FastAPI
    * sometimes works even after apps are created for some reason, likely due to how Uvicorn runs in a new process
    * but somehow sometimes doesn't work in prod, for equally unknown reasons
    * probably best to instrument each app instance
* Logs OIDC http headers as span attributes for FastAPI
* Creates OTLP exporters if specific env vars (below) are set
    * Pushes logs, metrics, and traces to the OTEL endpoint, if configured
    * Note: only logs and traces are printed to console, metrics are too noisy