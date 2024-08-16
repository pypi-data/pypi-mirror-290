# Radiant SDK

Radiant SDK is a Python package that simplifies the process of adding OpenTelemetry instrumentation to your applications, with a focus on integrating with Radiant's observability platform.

## Features

- Easy setup of OpenTelemetry tracing with Radiant
- Automatic instrumentation of OpenAI API calls
- Simple decorator for annotating functions with tracing

## Installation

The Radiant SDK uses Poetry for dependency management and packaging. To install the SDK and its dependencies:

```python
pip install radiant-sdk
```

## Usage

### Basic Setup

```python
from radiant import Instrumentor

# Initialize the instrumentor with your Radiant endpoint
Instrumentor.start("https://your-radiant-endpoint.com/api/v0/ingest/submit/otel/{project_name}",", api_key="")
```

### Error Handling

The SDK will raise a `RadiantConfigurationError` if the Radiant endpoint is not provided:

```python
from radiant import Instrumentor
try:
    Instrumentor.start("https://your-radiant-endpoint.com/api/v0/ingest/submit/otel/{YOUR_APP_NAME}", "<YOUR_API_KEY>")
except RadiantConfigurationError as e:
    print(f"Failed to initialize Radiant: {e}")
```

If you already have a `TracerProvider` (`opentelemetry.sdk.trace.TracerProvider()), you can just pass that into the configuration as well.

```python
tracer_provider = opentelemetry.sdk.trace.TracerProvider()
try:
    Instrumentor.start("http://your-radiant-endpoint.com/api/v0/ingest/submit/otel/{YOUR_APP_NAME}", "<YOUR_API_KEY>" tracer_provider)
except RadiantConfigurationError as e:
    print(f"Failed to initialize Radiant: {e}")
```

## Contributing

Reach out to support@radiantai.com if you want to provide feedback or suggest changes.

## License

This project is licensed under the MIT License.