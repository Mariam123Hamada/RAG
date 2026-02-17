from .provider.cohereprovider import cohereProvider
from .provider.gemmniprovider import geminiProvider


class EmbeddingFactory:

    @staticmethod
    def create(provider_name: str, api_key: str):
        if not provider_name:
            raise ValueError("Provider name must be provided")

        provider_name = provider_name.lower()

        if provider_name == "cohere":
            return cohereProvider(api_key=api_key)

        elif provider_name == "gemini":
            return geminiProvider(api_key=api_key)

        else:
            raise ValueError(f"Unsupported embedding provider: {provider_name}")
