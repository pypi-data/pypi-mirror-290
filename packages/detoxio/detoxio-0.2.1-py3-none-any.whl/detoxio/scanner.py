# Description: This file contains the LLMScanner class that provides a simple interface
# to test LLM models for security vulnerabilities by using detoxio.ai APIs

import base64
import detoxio.config as config
import proto.dtx.messages.common.llm_pb2 as llm_pb2

from collections.abc import Callable
from .models import LLMPrompt, LLMResponse, LLMScanResult
from .filter import PromptFilter

from detoxio.adapters.grpc import get_secure_channel_with_token
from detoxio.adapters.prompts import get_prompts_service

# Define the type for a function that handles a generated prompt
# and provides the response from the LLM model. The actual model inferencing
# is decoupled from our scanning logic.
LLMPromptHandler = Callable[[LLMPrompt], LLMResponse]

class LLMScanner:
    """
    LLMScanner provides a simple interface to test LLM models for security vulnerabilities
    by using detoxio.ai APIs to generate prompts and evaluate LLM responses for security
    vulnerabilities.

    args:
        count (int): The number of prompts to generate for each scan.
        key (str): The API key for the detoxio.ai API.
    """
    def __init__(self, count: int =10, key: str = None,
                 grpc_channel=None, filter: PromptFilter = None):
        """
        Initialize the LLMScanner with configuration parameters.

        Args:
            count (int): The number of prompts to generate for each scan.
            key (str): The API key for the detoxio.ai API.
            grpc_channel (grpc.Channel): The gRPC channel to use for communication.
            filter (PromptFilter): The filter to use for filtering prompts.
        """
        self.count = count
        self.batch_size = 1
        self.filter = filter

        if key is None:
            key = config.load_key_from_env()
        if not key:
            raise ValueError("DETOXIO_API_KEY environment variable is not set.")

        if grpc_channel is None:
            grpc_channel = get_secure_channel_with_token(config.get_api_host(), config.get_api_port(), key)

        self.grpc_channel = grpc_channel
        self.prompt_service = get_prompts_service(self.grpc_channel)

        self.model_type = llm_pb2.LLM_EVALUATION_MODEL_TYPE_COMPREHENSIVE

    def use_fast_evaluation(self):
        """
        Use the fast evaluation mode for the LLM model response evaluation.
        This mode is faster but less accurate.
        """
        self.model_type = llm_pb2.LLM_EVALUATION_MODEL_TYPE_FAST

    def use_comprehensive_evaluation(self):
        """
        Use the comprehensive evaluation mode for the LLM model response evaluation.
        This mode is slower but more accurate.
        """
        self.model_type = llm_pb2.LLM_EVALUATION_MODEL_TYPE_COMPREHENSIVE

    def start(self, prompt_handler: LLMPromptHandler,
              ignore_error: bool = False) -> LLMScanResult:
        """
        Assist in scanning an LLM model for security vulnerabilities.

        Args:
            prompt_handler (PromptHandler): A function that takes a LLMPrompt and returns a LLMResponse.
            ignore_error (bool): If True, ignore errors during scanning.
        """

        # Ping the service to verify connectivity
        self.prompt_service.ping()

        batch_size = self.batch_size
        count = self.count

        # Normalize the batch size
        if count < batch_size:
            batch_size = count

        # Create the result object to be hydrated during scan
        results = LLMScanResult()

        # Fetch in batches to optimize RTT
        while count > 0:
            # Build the filter if available
            filter = self.filter.build() if self.filter else None

            # Top level exception handler start
            try:
                # Fetch a batch of prompts
                # https://buf.build/detoxio/api/docs/main:dtx.services.prompts.v1#dtx.services.prompts.v1.PromptService.GeneratePrompts
                res = self.prompt_service.generate_prompt(count=batch_size,
                                                        filter=filter)

                # Invoke the handler for each prompt
                for prompt in res.prompts:
                    
                    ## If the prompt is base64 encoded, decode it
                    prompt_str = prompt.data.content
                    prompt_encoding = prompt.source_labels.get("_prompt_encoding")
                    if prompt_encoding == 'base64':
                        decoded_prompt_str = base64.b64decode(prompt_str).decode('utf-8')
                    else:
                        decoded_prompt_str = prompt_str
                    
                    llm_response = prompt_handler(LLMPrompt(content=decoded_prompt_str))

                    if llm_response is None:
                        raise ValueError("Prompt handler returned None")
                    if not isinstance(llm_response, LLMResponse):
                        raise ValueError("Prompt handler must return an LLMResponse")

                    if llm_response.is_skipped():
                        continue

                    # Evaluate response
                    evaluation_response = self.prompt_service.evaluate_prompt_response(prompt,
                                                                                    llm_response.content,
                                                                                    model_type=self.model_type)

                    # Store response
                    results.add_raw_result(evaluation_response)

            # Top level exception handling
            except Exception as e:
                if ignore_error:
                    results.add_error(e)
                else:
                    raise e

            count -= batch_size

        return results

