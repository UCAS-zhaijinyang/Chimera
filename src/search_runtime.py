"""One non-generative search provider shared by legacy and workflow agents."""
from __future__ import annotations

import os
import requests


def search_brave(query: str, source: str = 'text', max_results: int = 5) -> dict:
    """Search Brave's index without generating an AI answer.

    Args:
        query (str): Nonempty search query.
        source (str): Search category: text, images, or videos.
        max_results (int): Maximum results to return, between 1 and 20.

    Returns:
        dict: Provider, query, category and decoded source results. Empty
            results mean no matches, not successful completion of research.
    """
    endpoints = {'text': 'web', 'images': 'images', 'videos': 'videos'}
    if not isinstance(query, str) or not query.strip() or len(query) > 400:
        raise ValueError('search query must contain 1 to 400 characters')
    if source not in endpoints:
        raise ValueError('search source must be text, images, or videos')
    if type(max_results) is not int or not 1 <= max_results <= 20:
        raise ValueError('max_results must be an integer between 1 and 20')
    token = os.getenv('BRAVE_SEARCH_API_KEY', '').strip()
    if not token:
        raise RuntimeError('Brave search requires BRAVE_SEARCH_API_KEY')
    params = {'q': query, 'count': max_results, 'country': 'us',
              'search_lang': 'en', 'safesearch': 'strict', 'spellcheck': 'false'}
    try:
        # No automatic retries, provider fallback or credential-bearing redirect.
        # A timeout after transmission may still incur a search request charge.
        response = requests.get(
            f'https://api.search.brave.com/res/v1/{endpoints[source]}/search',
            params=params, headers={'Accept': 'application/json',
                                   'X-Subscription-Token': token},
            timeout=(5, 30), allow_redirects=False)
    except requests.RequestException as exc:
        raise RuntimeError(f'Brave search transport failed ({type(exc).__name__}); billing may be unknown') from None
    if response.status_code != 200:
        # Do not place raw request/response objects or provider error bodies in
        # agent traces; they could include the private authentication token.
        raise RuntimeError(f'Brave search returned HTTP {response.status_code}')
    try:
        payload = response.json()
        container = payload.get('web', {}) if source == 'text' else payload
        rows = container['results']
        if not isinstance(rows, list): raise ValueError('results must be a list')
        results = []
        for row in rows[:max_results]:
            if not isinstance(row, dict) or not isinstance(row.get('title'), str) or not isinstance(row.get('url'), str):
                raise ValueError('result lacks title or URL')
            result = {'title': row['title'], 'url': row['url'],
                      'description': row.get('description', '')}
            if source == 'images':
                image_url = row.get('properties', {}).get('url')
                if not isinstance(image_url, str): raise ValueError('image lacks source URL')
                result.update(image_url=image_url, thumbnail_url=row.get('thumbnail', {}).get('src'))
            if source == 'videos': result['video'] = row.get('video', {})
            results.append(result)
    except (AttributeError, KeyError, TypeError, ValueError):
        raise RuntimeError('Brave search returned a malformed result payload') from None
    return {'provider': 'brave', 'query': query, 'source': source,
            'request_count': 1, 'results': results}
