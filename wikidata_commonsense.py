import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql_query(query: str, target_kg: str) -> pd.DataFrame:
    """
    Executes a SPARQL query on the specified knowledge graph and returns the results as a pandas DataFrame.

    Args:
        query (str): The SPARQL query to execute.
        target_kg (str): The target knowledge graph. Must be one of ['wikidata', 'dbpedia', 'yago'].

    Returns:
        pd.DataFrame: A DataFrame containing the results of the query.
    """
    # Define SPARQL endpoints for each knowledge graph
    endpoints = {
        "wikidata": "https://query.wikidata.org/sparql",
        "dbpedia": "http://dbpedia.org/sparql",
        "yago": "https://yago-knowledge.org/sparql/query"
    }

    if target_kg not in endpoints:
        raise ValueError(f"Invalid target_kg. Must be one of {list(endpoints.keys())}.")

    # Set up the SPARQL wrapper
    sparql = SPARQLWrapper(endpoints[target_kg])
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and process the results
    try:
        results = sparql.query().convert()
        bindings = results.get("results", {}).get("bindings", [])
        # Convert the bindings to a pandas DataFrame
        data = []
        columns = []  # Ensure columns is a list
        for row in bindings:
            record = {}
            for key, value in row.items():
                record[key] = value.get("value", None)
                if key not in columns:  # Avoid duplicates while maintaining order
                    columns.append(key)
            data.append(record)
        # Create the DataFrame with the ordered list of columns
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        raise RuntimeError(f"Failed to execute SPARQL query: {e}")
    
if __name__ == "__main__":
    # Define the label to search for
    label = "orange"  # You can change this to any other label

    # Define the SPARQL query to find subclasses of entities with the specified label
    query = f"""
    SELECT ?subclass ?subclassLabel WHERE {{
        ?entity rdfs:label "{label}"@en.
        ?subclass wdt:P279 ?entity.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 10
    """

    # Execute the query with 'wikidata' as the target knowledge graph
    try:
        results_df = execute_sparql_query(query, target_kg="wikidata")
        print(results_df)
    except Exception as e:
        print(f"An error occurred: {e}")