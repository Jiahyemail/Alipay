#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def get_proxies(uri, seller):
    url = '%s/api/v2/proxies/' % uri
    params = {
        "seller": seller,
        "limit": "1",
        "server_type": "ecs"
    }

    try:
        response = requests.get(url, params=params)
        result = response.json().get('data', [{}])[0]

        return {
            'http': result['proxies'],
            'https': result['proxies']
        }
        logging.debug('%s\t%s', params, response.text)
    except:
        pass
        logging.exception('%s\t%s', params, response.text)
    return None