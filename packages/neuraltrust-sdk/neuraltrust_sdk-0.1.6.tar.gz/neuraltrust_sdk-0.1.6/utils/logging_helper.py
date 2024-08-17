import time
from typing import List
from interfaces.neuraltrust import (
    NeuralTrustEvalRequestCreateRequest,
    NeuralTrustEvalRequestSource,
    NeuralTrustEvalResult,
    NeuralTrustJobType,
    NeuralTrustEvalRunResult,
    NeuralTrustInterfaceHelper,
)
from interfaces.result import EvalResult
from services.api_service import NeuralTrustApiService
from api_keys import NeuralTrustApiKey
from errors import NeuralTrustMessages

class NeuralTrustLoggingHelper:
    @staticmethod
    def log_eval_performance_report(*args, **kwargs):
        """
        Passthrough method: Checks if the user has set a NeuralTrust API key
        """
        if NeuralTrustApiKey.is_set():
            return NeuralTrustApiService.log_eval_performance_report(*args, **kwargs)
        
    @staticmethod
    def log_experiment(*args, **kwargs):
        """
        Passthrough method: Checks if the user has set a NeuralTrust API key
        """
        if NeuralTrustApiKey.is_set():
            return NeuralTrustApiService.log_experiment(*args, **kwargs)

    @staticmethod
    def create_eval_request(eval_name: str, request_data: dict, request_type: str):
        try:
            if not NeuralTrustApiKey.is_set():
                return None
            # Create eval request
            eval_request = NeuralTrustEvalRequestCreateRequest(
                request_label=eval_name + "_eval_" + str(time.time()),
                request_data=request_data,
                request_data_type=request_type,
                source=NeuralTrustEvalRequestSource.DEV_SDK.value,
            )
            eval_request_id = NeuralTrustApiService.create_eval_request(eval_request)[
                "data"
            ]["eval_request"]["id"]
            return eval_request_id
        except Exception as e:
            print(
                f"An error occurred while creating eval request",
                str(e),
            )
            raise

    @staticmethod
    def log_eval_results(
        eval_request_id: str,
        eval_results: List[EvalResult],
    ):
        try:
            if not NeuralTrustApiKey.is_set():
                return
            neuraltrust_eval_result_create_many_request = []

            for eval_result in eval_results:
                # Construct eval result object
                failed_percent = float(eval_result.get("failure")) if "failure" in eval_result else None
                metrics = eval_result.get("metrics", [])
                datapoint_field_annotations = eval_result.get("datapoint_field_annotations", None)
                neuraltrust_eval_result = NeuralTrustEvalResult(
                    job_type=NeuralTrustJobType.LLM_EVAL.value,
                    failed_percent=failed_percent,
                    number_of_runs=1,
                    flakiness=0.0,
                    run_results=[
                        NeuralTrustEvalRunResult(
                            failed=eval_result["failure"] if "failure" in eval_result else None,
                            runtime=eval_result["runtime"],
                            reason=eval_result["reason"],
                            datapoint_field_annotations=datapoint_field_annotations,
                        )
                    ],
                    data=eval_result["data"],
                    runtime=eval_result["runtime"],
                    metrics=metrics,
                    display_name=eval_result["display_name"],
                )
                # log eval results to NeuralTrust
                neuraltrust_eval_result_create_request = (
                    NeuralTrustInterfaceHelper.eval_result_to_create_request(
                        eval_request_id=eval_request_id,
                        eval_type=eval_result["name"],
                        language_model_id=eval_result["model"] if "model" in eval_result else None,
                        eval_result=neuraltrust_eval_result,
                    )
                )
                neuraltrust_eval_result_create_request_dict = {
                    k: v
                    for k, v in neuraltrust_eval_result_create_request.items()
                    if v is not None
                }
                neuraltrust_eval_result_create_many_request.append(
                    neuraltrust_eval_result_create_request_dict
                )
            NeuralTrustApiService.log_eval_details(neuraltrust_eval_result_create_many_request)

        except Exception as e:
            print(
                f"An error occurred while posting eval results",
                str(e),
            )
            raise

    @staticmethod
    def log_eval_results_with_config(eval_results_with_config: dict, dataset_id: str):
        try:
            def remove_none_values(data: dict) -> dict:
                return {k: v for k, v in data.items() if v is not None}

            eval_results = eval_results_with_config.get("eval_results", [])
            # Limit to the first 1000 items
            sliced_eval_results = eval_results[:1000]
            cleaned_eval_results = []

            for eval_result in sliced_eval_results:
                cleaned_eval_result = {
                    "metrics": eval_result.get("metrics"),
                    "reason": eval_result.get("reason")
                }
                cleaned_eval_results.append(remove_none_values(cleaned_eval_result))

            development_eval_config = remove_none_values(eval_results_with_config.get("development_eval_config", {}))

            cleaned_results = {
                "dataset_id": dataset_id,
                "eval_results": cleaned_eval_results,
                "development_eval_config": development_eval_config
            }

            # Replace with your logging mechanism
            NeuralTrustApiService.log_eval_details(cleaned_results)
        except Exception as e:
            raise
