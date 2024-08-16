import os

from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


class RadiantConfigurationError(Exception):
    """Exception raised for errors in the Radiant configuration."""

    pass


class Instrumentor:
    _instance = None

    @classmethod
    def shutdown(cls):
        if cls._instance is not None:
            cls._instance.tracer_provider.shutdown()
            cls._instance.tracer_provider = None
            cls._instance = None
            del os.environ["OTEL_EXPORTER_OTLP_HEADERS"]
            OpenAIInstrumentor().uninstrument()

    @classmethod
    def start(cls, radiant_endpoint=None, api_key=None):
        if cls._instance is None:
            if radiant_endpoint is None:
                raise RadiantConfigurationError("Radiant endpoint must be provided.")
            if api_key is None:
                raise RadiantConfigurationError("API key must be provided.")
            cls._instance = cls(radiant_endpoint, api_key)
        return cls._instance

    def __init__(self, radiant_endpoint, api_key, tracer_provider=None):
        if not radiant_endpoint:
            raise RadiantConfigurationError("Radiant endpoint must be provided.")
        if not api_key:
            raise RadiantConfigurationError("API key must be provided.")
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api-key={api_key}"
        self.tracer_provider = tracer_provider or trace_sdk.TracerProvider()
        exporter = OTLPSpanExporter(radiant_endpoint)
        self.tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
        trace.set_tracer_provider(self.tracer_provider)

        OpenAIInstrumentor().instrument()
