from SPARQLWrapper import SPARQLWrapper, JSON


def Sparql(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    answer = ""
    for result in results["results"]["bindings"]:
        answer += result["label"]["value"] + "\n"
    return answer
