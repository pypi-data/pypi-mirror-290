# Radiant SDK

Radiant SDK is a Python package that simplifies the process of adding OpenTelemetry instrumentation to your applications, with a focus on integrating with Radiant's observability platform.

## Features

- Easy setup of OpenTelemetry tracing with Radiant
- Automatic instrumentation of OpenAI API calls
- Simple decorator for annotating functions with tracing

## Installation

The Radiant SDK uses Poetry for dependency management and packaging. To install the SDK and its dependencies:

1. Make sure you have Poetry installed. If not, install it by following the instructions at https://python-poetry.org/docs/#installation

2. Clone the repository:
   ```
   git clone https://github.com/your-repo/radiant-sdk.git
   cd radiant-sdk
   ```

3. Install the dependencies:
   ```
   poetry install
   ```

## Usage

### Basic Setup

```python
from radiant import Instrumentor, annotate

# Initialize the instrumentor with your Radiant endpoint
Instrumentor.start("http://your-radiant-endpoint.com/api/v0/otel_receiver")

# Use the annotate decorator to trace functions
@annotate
def my_function():
    # Your function code here
    pass
```

### Error Handling

The SDK will raise a `RadiantConfigurationError` if the Radiant endpoint is not provided:

```python
try:
    Instrumentor.start("http://your-radiant-endpoint.com/api/v0/ingest/submit/otel/{YOUR_APP_NAME}", "<YOUR_API_KEY>")
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

## Running Tests

To run the tests using pytest:

```
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.