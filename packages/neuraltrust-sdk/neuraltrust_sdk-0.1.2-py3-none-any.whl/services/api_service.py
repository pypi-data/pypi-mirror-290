import pkg_resources
import requests
from retrying import retry
from typing import List, Optional, Dict
from errors.exceptions import NoNeuralTrustApiKeyException
from interfaces.neuraltrust import (
    NeuralTrustFilters,
    NeuralTrustInference,
    NeuralTrustEvalRequestCreateRequest,
    NeuralTrustExperiment,
)
from interfaces.result import EvalPerformanceReport
from api_keys import NeuralTrustApiKey
from utils.constants import API_BASE_URL
from errors.exceptions import CustomException
import json

SDK_VERSION = pkg_resources.get_distribution("neuraltrust").version


class NeuralTrustApiService:
    @staticmethod
    def _headers():
        neuraltrust_api_key = NeuralTrustApiKey.get_key()
        return {
            "token": neuraltrust_api_key,
        }

    @staticmethod
    # TODO: this is for getting the real user data instead of the synthetic data
    def fetch_runs(
        filters: Optional[NeuralTrustFilters], limit: int
    ) -> List[NeuralTrustInference]:
        """
        Load data from NeuralTrust API.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/sdk/prompt_run/fetch-by-filter"
            filters_dict = filters.to_dict() if filters is not None else {}
            json = {
                "limit": limit,
                **filters_dict,
            }
            json = {k: v for k, v in json.items() if v is not None}
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=json,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            inferences = response.json()["data"]["inferences"]
            return list(map(lambda x: NeuralTrustInference(**x), inferences))
        except Exception as e:
            print("Exception fetching inferences", e)
            pass

    @staticmethod
    def create_testset(
        testset: List[Dict]
    ):
        """
        Creates a testset by calling the NeuralTrust API
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/testset"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=testset,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    
    @staticmethod
    def update_testset(
        testset_id: str,
        update_data: Dict
    ):
        """
        Updates a testset by calling the NeuralTrust API.

        Parameters:
        - testset_id (str): The ID of the testset to update.
        - update_data (Dict): A dictionary containing the data to update in the testset.

        Returns:
        The API response data for the updated testset.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/testset/{testset_id}"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=update_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    
    @staticmethod
    def create_evaluation_set(evaluation_set_data: Dict):
        """
        Creates a new evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_data (Dict): A dictionary containing the data for the new evaluation set.

        Returns:
        The API response data for the created evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=evaluation_set_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def update_evaluation_set(evaluation_set_id: str, update_data: Dict):
        """
        Updates an existing evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_id (str): The ID of the evaluation set to update.
        - update_data (Dict): A dictionary containing the data to update in the evaluation set.

        Returns:
        The API response data for the updated evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set/{evaluation_set_id}"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=update_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    

    @staticmethod
    def load_evaluation_set(evaluation_set_id: str):
        """
        Loads an existing evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_id (str): The ID of the evaluation set to load.

        Returns:
        The API response data for the loaded evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set/{evaluation_set_id}"
            response = requests.get(
                endpoint,
                headers=NeuralTrustApiService._headers(),
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
        
    @staticmethod
    def fetch_testset_rows(
        testset_id: str,
        number_of_rows: Optional[int] = None
    ):
        """
        Fetch the testset rows by calling the NeuralTrust API

        """
        try:
            if number_of_rows is None:
                number_of_rows = 20
            endpoint = f"{API_BASE_URL}/v1/testset/fetch-by-id/{testset_id}?offset=0&limit={number_of_rows}"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers()
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def add_testset_rows(testset_id: str, rows: List[Dict]):
        """
        Adds rows to a testset by calling the NeuralTrust API.

        Parameters:
        - testset_id (str): The ID of the testset to which rows are added.
        - rows (List[Dict]): A list of rows to add to the testset, where each row is represented as a dictionary.

        Returns:
        The API response data for the dataset after adding the rows.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/testset/{testset_id}"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json={"testset_rows": rows},
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get('details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def create_eval_request(
        neuraltrust_eval_request_create_request: NeuralTrustEvalRequestCreateRequest,
    ):
        """
        Create eval request
        """
        try:
            endpoint = f"{API_BASE_URL}/api/v1/eval_request"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=neuraltrust_eval_request_create_request,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            print(
                f"An error occurred while creating eval request",
                str(e),
            )
            raise

    @staticmethod
    def log_experiment(
        eval_request_id: str,
        experiment: NeuralTrustExperiment,
    ):
        """
        Logs the experiment metadata to NeuralTrust.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/experiment"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json={
                    "eval_request_id": eval_request_id,
                    "experiment_name": experiment["experiment_name"],
                    "experiment_description": experiment["experiment_description"],
                    "language_model_provider": experiment["language_model_provider"],
                    "language_model_id": experiment["language_model_id"],
                    "prompt_template": experiment["prompt_template"],
                    "dataset_name": experiment["dataset_name"],
                },
            )
            print(response.status_code)
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            print(
                f"An error occurred while posting experiment metadata",
                str(e),
            )
            raise
    
    @staticmethod
    def log_eval_details(eval_results: dict):
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-run/details"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=eval_results,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
    
    def log_eval_run(eval_run: dict):
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-run"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=eval_run,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

    def update_testsets(testsets: List[Dict]):
        try:
            endpoint = f"{API_BASE_URL}/v1/testset"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=testsets,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
