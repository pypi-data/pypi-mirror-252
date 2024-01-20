import os

from guided_molecule_gen.inference_client import BioNemoTritonClient

TRITON_SERVER_LIVE = False
BIONEMO_SERVER_LIVE = False


def _check_triton_server():
    global TRITON_SERVER_LIVE
    try:
        _test_client = BioNemoTritonClient()
    except RuntimeError:
        return
    try:
        TRITON_SERVER_LIVE = _test_client.ping_connection()
    except ConnectionError:
        pass


_check_triton_server()


def bionemo_env_credentials():
    bionemo_host_url: str = os.getenv("BIONEMO_SERVICE_HOST", "https://stg.bionemo.ngc.nvidia.com/v1")
    bionemo_key: str = os.getenv("BIONEMO_SERVICE_KEY", None)
    return bionemo_host_url, bionemo_key


def _check_bionemo_server():
    try:
        from bionemo.api import BionemoClient
        from bionemo.error import AuthorizationError
    except ImportError:
        return

    bionemo_host_url, bionemo_key = bionemo_env_credentials()

    try:
        BionemoClient(api_key=bionemo_key, api_host=bionemo_host_url)
    except (ConnectionError, AuthorizationError):
        return
    global BIONEMO_SERVER_LIVE
    BIONEMO_SERVER_LIVE = True


_check_bionemo_server()
