import urllib.request
import urllib.parse
import urllib.error
import json

_server = "https://techathonai.onrender.com"
_key = None

class ApiException(Exception):
    pass

def _q(string):
    return urllib.parse.quote(string.encode("utf-8"))

def _fetch(request):
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read())
    except urllib.error.HTTPError as e:
        data = json.loads(e.read())

    if data["status"] == "error":
        raise ApiException(data["message"])

    return data

def _post(url, data):
    request = urllib.request.Request(url, data = json.dumps(data).encode("utf-8"))

    request.add_header("Content-Type", "application/json")

    return _fetch(request)

def _checkKey():
    if _key == None:
        raise ApiException("No user key provided (use `connect` to provide your user key)")

def connect(key, server = _server):
    """
    Connect to the Techathon AI server using your given user key.

    :param str key: The key assigned to your team.
    :param str server: The server to use. The main Techathon AI server will be used by default. |default| :code:`"https://techathonai.onrender.com"`
    :raises ApiException: This exception is raised if the user key doesn't exist.
    """

    global _key, _server

    _key = key
    _server = server

    _fetch(f"{_server}/api/balance?key={_q(_key)}")

def getBalance():
    """
    Get the number of tokens you have remaining for your user key.

    :returns int: The number of tokens you have remaining.
    :raises ApiException: This exception is raised if you haven't called :code:`connect` yet.
    """

    _checkKey()

    return int(_fetch(f"{_server}/api/balance?key={_q(_key)}")["tokens"])

def complete(prompt, temperature = 0.7):
    """
    Using the prompt, generate a completion using a GPT large language model.

    This will deduct from your token balance the sum of prompt tokens and completion tokens.

    :param str prompt: The prompt text to generate the completion with.
    :param float temperature: The temperature value (between 0 and 1) to use. |default| :code:`0.7`
    :returns str: The completion text (excludes the prompt text).
    :raises ApiException: This exception is raised if you have run out of tokens, you haven't called :code:`connect` yet, or if a server error occurs.
    """

    _checkKey()

    return _post(
        f"{_server}/api/complete?key={_q(_key)}&temperature={_q(str(temperature))}",
        {"prompt": prompt}
    )["completion"]