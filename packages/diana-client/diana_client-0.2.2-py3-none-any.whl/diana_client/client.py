import os
import sys
import requests
import time
from typing import Optional, Sequence, Dict, Union
from .utils import generate_uuid
import asyncio


class HTTPClient:
    """The base client for communicating with an DIANA server and it's model registry.

    The client is used to register, patch, delete and infer on models with the DIANA server.

    Attributes:
        diana_server_url (str): The url of the DIANA server.
        model_registry_url (str): The url of the model registry.
        header_payload (Dict[str, str]): The headers for the request.
        inference_timer (List[float]): A list of inference times.
        inference_counter (List[int]): A list of inference counts (number of inputs per inference call).
    """

    def __init__(
        self,
        diana_server_url: str = "https://diana.distributive.network",
        model_registry_url: str = "https://models.diana.distributive.network",
        header_key: str = "diana-secret-key",
    ):
        """
        Initializes the client with the DIANA server url and model registry url.

        Args:
            diana_server_url (str): The url of the DIANA server.
            model_registry_url (str): The url of the model registry.
            header_key (str): The header key for the request.
        """
        self.diana_server_url = diana_server_url
        self.model_registry_url = model_registry_url
        self.header_payload = {"key": header_key}
        self.inference_timer = []
        self.inference_counter = []
        self._password = None
        self._email = None

        self.request_session = requests.Session()
        self.request_session.headers.update(self.header_payload)
        self.request_session.headers.update(
            {"prediction-key": self.header_payload["key"]}
        )

    def check_diana_server_connection(self) -> bool:
        """
        Checks if the DIANA server is reachable.

        Returns:
            Bool: True if the DIANA server is reachable.
        """
        try:
            response = self.request_session.get(
                f"{self.diana_server_url}/status")
            response.raise_for_status()
            return True
        except requests.exceptions.ConnectionError:
            return False

    def __get_file__(self, file_path: str) -> bytes:
        """
        Retrieves the contents of a file from disk and returns it as bytes.

        Args:
            file_path (str): The path to the file.

        Returns:
            bytes: The contents of the file as bytes.
        """
        with open(file_path, "rb") as f:
            ret_bytes: bytes = f.read()
        return ret_bytes

    def signup(self, email: str, password: str, keystore_path: str = "~/.dcp/default.keystore", **kwargs) -> requests.Response:
        url = f"{self.model_registry_url}/users/signup"

        files_payload = {
            "keystore": self.__get_file__(os.path.expanduser(keystore_path))
        }

        resp = self.request_session.post(
            url=url,
            data={
                "email": email,
                "password": password,
                **kwargs
            },
            files=files_payload
        )

        self._email = email
        self._password = password

        try:
            self._session = resp.json()
            self.request_session.headers.update(
                {
                    "Authorization": f'Bearer {self._session["session"]["access_token"]}'
                }
            )
        except Exception as e:
            print(resp.text)
            raise RuntimeError("Bad response from the server: " + str(e))

        return resp

    def signin(
        self, email: Optional[str] = None, password: Optional[str] = None
    ) -> requests.Response:
        if email is None:
            email = self._email
        else:
            self._email = email

        if password is None:
            password = self._password
        else:
            self._password = password

        if email is None or password is None:
            raise ValueError(
                "Email and password are required. Make sure to sign in or sign up before running any other methods."
            )

        url = f"{self.model_registry_url}/auth/signin"

        resp = self.request_session.post(
            url=url, data={"email": email, "password": password}
        )

        try:
            self._session = resp.json()
            self.request_session.headers.update(
                {
                    "Authorization": f'Bearer {self._session["session"]["access_token"]}'
                }
            )
        except Exception as e:
            print(resp.text)
            raise RuntimeError("Bad response from the server: " + str(e))

        return resp

    def register_model_with_bytes(
        self,
        model_name: str,
        model_bytes: bytes,
        preprocess_bytes: bytes,
        postprocess_bytes: bytes,
        password: str = "DefaultPassword",
        language: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
    ) -> requests.Response:
        """
        Registers a new model with the model registry. Will throw if the model already exists.

        Args:
            model_name (str): The name of the model to register.
            model_bytes (bytes): The bytes of the model.
            preprocess_bytes (bytes): The bytes of the preprocess file for this model.
            postprocess_bytes (bytes): The bytes of the postprocess file for this model.
            password (str): The password for this model.
            language (str): The language for this model. Can be either javascript or python.
            packages (Sequence[str]): A list of packages required for this model.

        Returns:
            requests.Resposne: The response from the model registry.
        """

        url = f"{self.model_registry_url}/models"
        data_payload = {
            "modelName": model_name,
            "password": password,
            "reqPackages": packages if packages is not None else [],
            "language": "javascript" if language is None else language,
        }

        files_payload = {
            "model": model_bytes,
            "preprocess": preprocess_bytes,
            "postprocess": postprocess_bytes,
        }

        response = self.request_session.post(
            url,
            data=data_payload,
            files=files_payload,
        )
        return response

    def register_model(
        self,
        model_name: str,
        model_path: str,
        preprocess_path: str,
        postprocess_path: str,
        password: str = "DefaultPassword",
        language: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
    ) -> requests.Response:
        """
        Registers a new model with the model registry. Will throw if the model already exists.

        Args:
            model_name (str): The name of the model to register.
            model_path (str): The path to the model.
            preprocess_path (str): The path to the preprocess file for this model.
            postprocess_path (str): The path to the postprocess file for this model.
            password (str): The password for this model.
            language (str): The language for this model. Can be either javascript or python.
            packages (Sequence[str]): A list of packages required for this model.

        Returns:
            requests.Resposne: The response from the model registry.
        """

        return self.register_model_with_bytes(
            model_name,
            self.__get_file__(model_path),
            self.__get_file__(preprocess_path),
            self.__get_file__(postprocess_path),
            password,
            language,
            packages,
        )

    def patch_model(
        self,
        model_name: str,
        model_path: str,
        preprocess_path: str,
        postprocess_path: str,
        password: str = "DefaultPassword",
        language: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
    ) -> requests.Response:
        """
        Patches a specified model from the model registry with provided information.

        Args:
            model_name(str): The name of the model to patch.
            model_path(str): The path to the model.
            preprocess_path(str): The path to the preprocess file for this model.
            postprocess_path(str): The path to the postprocess file for this model.
            password(str): The password for this model.
            language(str): The language for this model. Can be either javascript or python.
            packages(Sequence[str]): A list of packages required for this model.

        Returns:
            requests.Response: The response from the model registry.
        """
        url = f"{self.model_registry_url}/models/{model_name}"
        data_payload = {
            "modelID": model_name,
            "password": password,
            "reqPackages": packages if packages is not None else [],
            "language": "javascript" if language is None else language,
        }

        files_payload = {
            "model": self.__get_file__(model_path),
            "preprocess": self.__get_file__(preprocess_path),
            "postprocess": self.__get_file__(postprocess_path),
        }

        response = self.request_session.patch(
            url,
            data=data_payload,
            files=files_payload,
        )

        response.raise_for_status()

        return response

    def delete_model(
        self, model_name: str, password: str = "DefaultPassword"
    ) -> requests.Response:
        """
        Deletes the specified model from the model registry.

        Args:
            model_name (str): The name of the model to delete.
            password (str): The associated password for the modelself.

        Returns:
            requests.Response: The response object from the model registry after deleting the model.
        """
        url = f"{self.model_registry_url}/models/{model_name}"

        self.request_session.headers.update({"password": password})

        response = self.request_session.delete(
            url,
        )

        self.request_session.headers.pop("password")

        response.raise_for_status()

        return response

    def get_model(self, model_name: str) -> requests.Response:
        """
        Retrieves a model from the model registry.

        Args:
            model_name (str): The name of the model to retrieve.

        Returns:
            requests.Response: The response object from the model registry.
        """
        url = f"{self.model_registry_url}/models/{model_name}"

        response = self.request_session.get(url)

        response.raise_for_status()

        return response

    def infer(
        self,
        inputs: Union[Dict, Sequence[bytes]],
        model_name: str,
        slice_batch: int = 1,
        inference_id: Optional[str] = None,
        compute_group_info: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """
        Performs an inference on the provided inputs using the model specified. Returns
        the inference results as a dictionary.

        Args:
            inputs(Sequence[bytes]): A list of inputs in byte format.
            model_name(str): The model name we will be inferencing on.
            slice_batch(int): The number of inputs to run per slice.
            inference_id(Optional[str]): A special ID for this inference instance (Optional).
            compute_group_info(Optional[str]): Compute group information in the form of "<joinKey>/<joinSecret>".

        Returns:
            Dict: The inference results as a dictionary.
        """
        if self._email and self._password:
            self.signin()

        inference_id = (
            inference_id
            if inference_id is not None
            else f"{model_name}_{generate_uuid()}"
        )
        url = f"{self.diana_server_url}/Prediction/{inference_id}/detect/iterations/{model_name}/{slice_batch}"
        if compute_group_info is not None:
            url = f"{url}/{compute_group_info}"

        files = {}
        if type(inputs) is dict:
            files = inputs
            for key in files:
                assert (
                    type(files[key]) is bytes
                ), f"Inputs must be bytes but got {type(files[key])} for key {key}"
        elif type(inputs) is list:
            for ind, elem in enumerate(inputs):
                assert (
                    type(elem) is bytes
                ), f"Inputs must be bytes but got {type(elem)} for index {ind}"
                files[f"{ind}"] = elem
        else:
            raise TypeError("inputs must be a list or dict")

        start_time = time.time()

        response = self.request_session.post(
            url,
            files=files,
            data=kwargs,
        )

        response.raise_for_status()

        end_time = time.time()

        self.inference_timer.append(end_time - start_time)
        self.inference_counter.append(len(inputs))

        return response.json()

    async def infer_async(
        self,
        inputs: Union[Dict, Sequence[bytes]],
        model_name: str,
        slice_batch: int = 1,
        inference_id: Optional[str] = None,
        compute_group_info: Optional[str] = None,
    ) -> Dict:
        """
        Performs an asynchronous inference on the provided inputs using the model specified. Returns
        the inference results as a dictionary.

        To use asynchronous API, please make sure to use asyncio to create task:
            ```python
            import asyncio


            def callback(task):
                results = task.result()

            loop = asyncio.get_event_loop()
            task = loop.create_task(client.infer_async(...))
            task.add_done_callback(callback)

            ```

        Args:
            inputs(Sequence[bytes]): A list of inputs in byte format.
            model_name(str): The model name we will be inferencing on.
            slice_batch(int): The number of inputs to run per slice.
            inference_id(Optional[str]): A special ID for this inference instance (Optional).
            compute_group_info(Optional[str]): Compute group information in the form of "<joinKey>/<joinSecret>".

        Returns:
            Dict: The inference results as a dictionary.
        """
        inference_id = (
            inference_id
            if inference_id is not None
            else f"{model_name}_{generate_uuid()}"
        )
        url = f"{self.diana_server_url}/Prediction/{inference_id}/detect/iterations/{model_name}/{slice_batch}"
        if compute_group_info is not None:
            url = f"{url}/{compute_group_info}"

        files = {}
        if type(inputs) is dict:
            files = inputs
            for key in files:
                assert (
                    type(files[key]) is bytes
                ), f"Inputs must be bytes but got {type(files[key])} for key {key}"
        elif type(inputs) is list:
            for ind, elem in enumerate(inputs):
                assert (
                    type(elem) is bytes
                ), f"Inputs must be bytes but got {type(elem)} for index {ind}"
                files[f"{ind}"] = elem
        else:
            raise TypeError("inputs must be a list or dict")

        start_time = time.time()

        if self._password is None or self._email is None:
            response = self.request_session.post(
                url,
                files=files,
            )
        else:
            response = self.request_session.post(
                url,
                data={"email": self._email, "password": self._password},
                files=files,
            )

        response.raise_for_status()

        end_time = time.time()

        self.inference_timer.append(end_time - start_time)
        self.inference_counter.append(len(inputs))

        return response.json()
