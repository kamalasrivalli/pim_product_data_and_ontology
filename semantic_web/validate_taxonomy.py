
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "taxonomy.ttl"
SHAPES_FILE = BASE_DIR / "validation_shapes.ttl"
QUERY_FILE = BASE_DIR / "sparql_queries.rq"


# 1. Load RDF data
data_graph = Graph()
data_graph.parse(DATA_FILE, format="turtle")

print(f"RDF triples loaded: {len(data_graph)}")


# 2. Execute SPARQL queries
# Run all SPARQL queries
query_text = QUERY_FILE.read_text(encoding="utf-8")

parts = query_text.split("# Query ")

prefixes = parts[0]

for part in parts[1:]:
    query_number, query_body = part.split("\n", 1)

    sparql_query = prefixes + "\n" + query_body.strip()

    print(f"\n--- SPARQL QUERY {query_number.strip()} ---")

    results = data_graph.query(sparql_query)

    for row in results:
        print(row)


# 3. Load SHACL shapes
shapes_graph = Graph()
shapes_graph.parse(SHAPES_FILE, format="turtle")


# 4. Validate RDF data
conforms, report_graph, report_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference="none",
    abort_on_first=False
)

print("\n--- SHACL VALIDATION REPORT ---")
print(report_text)

print(f"\nConforms: {conforms}")
