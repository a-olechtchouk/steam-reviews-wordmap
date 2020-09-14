def check_assertions(assertion_value, assertion_type):
    if __debug__:
    
        if assertion_type == 'init_stat_code':
            if not assertion_value == 200: raise AssertionError

        elif assertion_type == 'query_success': 
            if not assertion_value == 1: raise AssertionError


def check_empty_query_response(query, prev_c):
    if query.get("query_summary").get("num_reviews") == 0:
        return True

    if query == -1:
        return True

    if prev_c == query.get('cursor'):
        return True
    
    return False