from urllib.parse import urljoin, urlparse


def remove_query_params_from_url(url: str):
    try:
        url = urlparse(url)
        return urljoin(url.geturl(), url.path)
    except Exception as exception:
        print("Something go wrong during processing external_path")