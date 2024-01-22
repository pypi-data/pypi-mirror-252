"""A python class for performing HTTPS requests (GET, POST)"""

import requests
import base64


class RequestError(Exception):
  """Exception for request error"""
  pass


class HttpsAgent:
  """Wrapper class of requests"""
  def __init__(self, token: str, ssl: bool):
    self.__token = token
    self.__ssl = ssl


  def get(self, url: str, params: dict = None):
    """Perform GET request

      Args:
        url:
          An API endpoint
          Example: https://bioturing.com/api
        params:
          Params of the GET requests, will be encoded to URL's query string
          Example: {"param1": 0, "param2": true}
    """
    if params is None:
      params = {}

    try:
      res = requests.get(
        url=url,
        params=params,
        headers={'bioturing-api-token': self.__token},
        verify=self.__ssl
      )
      return res.json()
    except requests.exceptions.RequestException as e:
      print('Request fail with error: ', e)
      return None


  def post(self, url: str, body: dict = None, check_error=True):
    """
    Perform POST request

    Args:
      url:
        An API endpoint
        Example: https://bioturing.com/api

      body:
        Body of the request
        Example: {"param1": 0, "param2": true}
    """
    if body is None:
      body = {}

    try:
      res = requests.post(
        url=url,
        json=body,
        headers={'bioturing-api-token': self.__token},
        verify=self.__ssl
      )
      res_json = res.json()
      if check_error and res.status_code >= 400:
        if 'traceback' in res_json:
          message = f"Request fail with traceback:\n{res_json['traceback']}"
        else:
          detail = res_json.get('detail', 'Something went wrong, please contact support@bioturing.com.')
          message = f"Request fail with message:\n{detail}"
        raise RequestError(message)
      return res_json
    except requests.exceptions.RequestException as e:
      print('Request fail with error: ', e)
      return None
