# Semantic Web: Electronics Taxonomy

## Overview

This part of the project represents an electronics product taxonomy using Semantic Web standards. The taxonomy is modelled as an RDF graph using SKOS.

## 1. SKOS Taxonomy

The taxonomy uses:

- **SKOS ConceptScheme:** Represents the Electronics taxonomy.
- **SKOS Concept:** Represents categories and subcategories.
- **skos:prefLabel:** Provides human-readable category labels.
- **skos:broader:** Represents hierarchical relationships between concepts.
- **skos:inScheme:** Associates concepts with the Electronics concept scheme.

The hierarchy covers Computers, Mobile Devices, Audio, Accessories and Smart Home, along with their respective subcategories.

## 2. SPARQL Queries

The file `sparql_queries.rq` contains queries to:

1. Retrieve taxonomy concepts.
2. Find the direct children of Electronics.
3. Retrieve descendants through hierarchical relationships.
4. List concepts belonging to the Electronics scheme.
5. Count the direct children of Electronics.

## 3. SHACL Validation

The file `validation_shapes.ttl` defines constraints for the taxonomy, including:

- Concepts must have a preferred label.
- Preferred labels must use language-tagged string values.
- Concepts must belong to the Electronics concept scheme.

The validation script loads the RDF graph and applies the SHACL shapes.

**Validation result:** Conforms: True.

## 4. Technologies

- RDF
- Turtle
- SKOS
- SPARQL
- SHACL
- Python
- RDFLib
- pySHACL

## Project Files

- `taxonomy.ttl` — SKOS representation of the Electronics taxonomy.
- `sparql_queries.rq` — SPARQL queries.
- `validation_shapes.ttl` — SHACL validation constraints.
- `validate_taxonomy.py` — Python script for loading, querying and validating the RDF graph.