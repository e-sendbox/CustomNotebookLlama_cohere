import os
from typing import Optional, Dict, Any
from llama_cloud.client import AsyncLlamaCloud
from llama_cloud_services import LlamaExtract, LlamaParse
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# LlamaCloud regional endpoints
LLAMACLOUD_REGIONS = {
    "us": "https://api.cloud.llamaindex.ai",
    "eu": "https://api.cloud.eu.llamaindex.ai",
}


def get_llamacloud_base_url() -> Optional[str]:
    """
    Get the appropriate LlamaCloud base URL based on region configuration.

    Returns:
        str: The base URL for LlamaCloud API, or None if using default
    """
    base_url = os.getenv("LLAMACLOUD_BASE_URL")
    if base_url:
        return base_url

    region = os.getenv("LLAMACLOUD_REGION", "").lower()
    if region in LLAMACLOUD_REGIONS:
        return LLAMACLOUD_REGIONS[region]

    return None


def get_llamacloud_config() -> Dict[str, Any]:
    """
    Get LlamaCloud configuration including base URL.

    Returns:
        dict: Configuration dictionary with token and optional base_url
    """
    config = {"token": os.getenv("LLAMACLOUD_API_KEY")}

    base_url = get_llamacloud_base_url()
    if base_url:
        config["base_url"] = base_url

    return config


def create_llamacloud_client() -> AsyncLlamaCloud:
    """
    Create a configured AsyncLlamaCloud client with regional support.

    Returns:
        AsyncLlamaCloud: Configured client instance
    """
    config = get_llamacloud_config()
    return AsyncLlamaCloud(**config)


def create_llama_extract_client() -> LlamaExtract:
    """
    Create a configured LlamaExtract client with regional support.

    Returns:
        LlamaExtract: Configured client instance
    """
    config = get_llamacloud_config()
    return LlamaExtract(**config)


def create_llama_parse_client(result_type: str = "markdown") -> LlamaParse:
    """
    Create a configured LlamaParse client with regional support.

    Args:
        result_type: The result type for parsing (default: "markdown")

    Returns:
        LlamaParse: Configured client instance
    """
    config = get_llamacloud_config()
    base_url = config.get("base_url")
    if base_url:
        return LlamaParse(
            api_key=config["token"], result_type=result_type, base_url=base_url
        )
    else:
        return LlamaParse(api_key=config["token"], result_type=result_type)


def create_llamacloud_index(api_key: str, pipeline_id: str) -> LlamaCloudIndex:
    """
    Create a configured LlamaCloudIndex with regional support.

    Args:
        api_key: The API key for authentication
        pipeline_id: The pipeline ID to use

    Returns:
        LlamaCloudIndex: Configured index instance
    """
    base_url = get_llamacloud_base_url()
    if base_url:
        return LlamaCloudIndex(
            api_key=api_key, pipeline_id=pipeline_id, base_url=base_url
        )
    else:
        return LlamaCloudIndex(api_key=api_key, pipeline_id=pipeline_id)
