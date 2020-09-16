from requests import Response
import simplejson as json

def is_query_response_valid(r: Response):
    if r.status_code != 200: return False            # ensure response status code is 200 
    if r.text == '{"response":{}}': return False     # ensure the (JSON-encoded) response list isnt empty


    json_dict = r.json()                                    # at this point we can try to decode the JSON into a dict
    if json_dict['success'] != 1: return False              # ensure the query was successful
    
    query_summary = json_dict['query_summary']   
    if query_summary['num_reviews'] <= 0: return False      # ensure we got some reviews in the response (more than 0)

    return json_dict                                        # at this point we should be okay to return json_dict