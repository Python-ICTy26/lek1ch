import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 5


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url

        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"],
            backoff_factor=backoff_factor,
        )

        http_adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retry_strategy)
        self._session = requests.Session()
        self._session.mount("http://", http_adapter)
        self._session.mount("https://", http_adapter)
        self._session.hooks["response"] = [
            lambda response, *args, **kwargs: response.raise_for_status()
        ]

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self._make_request(url, "get", *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self._make_request(url, "post", *args, **kwargs)

    def _make_request(
        self, url, method: tp.Literal["get", "post"], *args: tp.Any, **kwargs: tp.Any
    ):
        request_url = f"{self.base_url}/{url}"
        if method == "get":
            response = self._session.get(request_url, *args, **kwargs)
        elif method == "post":
            response = self._session.post(request_url, *args, **kwargs)
        else:
            raise ValueError(f"{method} is not supported")

        return response.json()
