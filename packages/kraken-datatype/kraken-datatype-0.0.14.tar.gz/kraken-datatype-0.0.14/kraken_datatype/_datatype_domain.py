
from functools import lru_cache
from urllib.parse import urlparse
import validators

"""Normalize domain
"""



def validate(data):

    if validators.domain(data):
        return True
    else:
        return False


@lru_cache(maxsize=32)
def normalize(data):

    if not data.startswith('http'):
        data = 'https://' + data
    
    domain = urlparse(data).netloc
    domain = domain.replace('www.', '')

    return domain