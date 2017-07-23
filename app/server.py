from sanic import Sanic
from sanic import response
import search
import sys
import json
import itertools
import math
from operator import itemgetter

with open('./facebase.json', 'r') as f:
    records = json.load(f)

def get_normalized(record):
    record['norm_name'] = search.normalize_name(record['l_name'])
    record['norm_role'] = search.normalize_role(record['l_role'])
    record['norm_proj'] = search.normalize_ico_name(record['l_proj'])
    return record

normalized_records = list(map(get_normalized, records))


app = Sanic()

@app.route("/")
async def test(request):
    if 'q' not in request.args.keys() or len(request.args['q']) != 1:
        return response.HTTPResponse(status=404, content_type="text/html; charset=utf-8")

    results = []

    query_name 	   = search.normalize_name(request.args['q'][0])
    query_role 	   = search.normalize_role(request.args['q'][0])
    query_ico_name = search.normalize_ico_name(request.args['q'][0])

    for record in normalized_records:
        match_score = 0

        for token1, token2 in itertools.product(query_name, record['norm_name']):

            if token1 == token2:
                match_score += 3
            elif search.fuzzy_match(token1, token2, dist=int(math.sqrt(min(len(token1), len(token2))))):
                match_score += 1

        for token1, token2 in itertools.product(query_role, record['norm_role']):

            if token1 == token2:
                match_score += 3
            if search.fuzzy_match(token1, token2, dist=int(math.sqrt(min(len(token1), len(token2))))):
                match_score += 1

        for token1, token2 in itertools.product(query_ico_name, record['norm_proj']):

            if token1 == token2:
                match_score += 3
            if search.fuzzy_match(token1, token2, dist=int(math.sqrt(min(len(token1), len(token2))))):
                match_score += 1

        if match_score != 0:
            new_result = record.copy()
            new_result.pop('l_name', None)
            new_result.pop('l_role', None)
            new_result.pop('l_proj', None)
            new_result.pop('norm_name', None)
            new_result.pop('norm_role', None)
            new_result.pop('norm_proj', None)
            new_result.pop('aws_result', None)
            new_result['score'] = match_score 
            results.append(new_result)
    
    results = sorted(results, key=itemgetter('score'), reverse=True)
    return response.json(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8086)
