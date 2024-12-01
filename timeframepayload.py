def get_timeframe_payload(unique_id, search_query):
    """Returns the payload dictionary for the Splunk query with time parameters."""
    return {
        'id': unique_id,
        'max_count': '2000',
        'search': search_query,
        'earliest_time': '-720h',
        'latest_time': 'now'
    }
