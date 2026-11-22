# Product Information Management (PIM), Taxonomy & Semantic Web

## Overview

This project explores product information management through a practical workflow combining product taxonomy design, supplier data normalization, data validation and Semantic Web technologies.

It brings together concepts from PIM, computational linguistics, knowledge representation and data engineering.

## Project Objectives

- Design a structured product taxonomy for an electronics catalogue.
- Understand product attributes, families, categories and product data relationships.
- Map supplier product data to standardized attributes.
- Clean and validate supplier data using Python.
- Represent taxonomy concepts using SKOS and RDF.
- Query taxonomy relationships using SPARQL.
- Define data quality constraints using SHACL.
- Build a small ontology using Protégé.

## Repository Structure

```text
pim_product_data_and_ontology/
│
├── documentation/
│   ├── ontology-documentation.md
│   ├── product-data-workflow.md
│   └── semantic-web-documentation.md
│
├── ontology/
│   └── language_ontology.rdf
│
├── taxonomy/
│   └── electronics_taxonomy.md
│
├── product_data/
│   ├── supplier_products.csv
│   └── attribute_mapping.xlsx
│
├── python_pipeline/
│   ├── pipeline.py
│   └── tests/
│
├── semantic_web/
│   ├── taxonomy.ttl
│   ├── sparql_queries.rq
│   ├── validation_shapes.ttl
│   └── validate_taxonomy.py
│
├── output/
│   ├── cleaned_products.csv
│   └── error_report.csv
│
└── README.md
```

## 1. Product Taxonomy

Designed a hierarchical taxonomy for an electronics catalogue.

The main categories include:

- Computers
- Mobile Devices
- Audio
- Accessories
- Smart Home

The taxonomy defines category relationships and provides a foundation for consistent product classification.

## 2. Supplier Data Processing

Created a sample supplier product dataset and an attribute mapping specification.

A Python pipeline using Pandas performs:

- Supplier data loading and schema checks.
- Brand name standardization.
- RAM and storage extraction.
- Weight unit normalization.
- Required-field validation.
- Duplicate product identification for review.
- Export of cleaned records and validation errors.

### Output

- `cleaned_products.csv`
- `error_report.csv`

## 3. Semantic Web and Knowledge Representation

Represented the electronics taxonomy using RDF and SKOS.

Implemented:

- A SKOS concept scheme.
- Concepts and hierarchical relationships.
- Preferred labels and scheme membership.
- SPARQL queries to retrieve concepts and explore hierarchy.
- SHACL shapes to validate labels and concept scheme membership.

The taxonomy was loaded and queried using RDFLib, with SHACL validation performed using pySHACL.

**Validation result: Conforms: True.**

## 4. Ontology Development

Created a language ontology using Protégé.

The ontology includes:

- Language and LanguageFamily classes.
- DravidianLanguage and IndoEuropeanLanguage subclasses.
- Telugu, Kannada, English and German individuals.
- WritingSystem concepts.
- The `hasISOCode` data property.
- The `usesWritingSystem` object property.

The ontology explores how languages and writing systems can be represented through structured relationships.

## 5. PIM Concepts Explored

The project also covers core PIM concepts:

- Product attributes and attribute groups.
- Product families and variants.
- Product models.
- Locales and channels.
- Product data enrichment and completeness.
- Supplier data integration.
- PIM and ERP concepts.

Akeneo concepts and workflows were studied through guided exercises; this project does not represent a live Akeneo implementation.

## Technologies

- Python
- Pandas
- RDFLib
- pySHACL
- RDF / Turtle
- SKOS
- SPARQL
- SHACL
- Protégé
- CSV and Excel

## Project Scope

This is a learning and portfolio project demonstrating practical work with product data, taxonomy modelling, data quality and semantic technologies.

It uses sample supplier data and a locally developed ontology and taxonomy. It is not connected to a production PIM, ERP or supplier system.