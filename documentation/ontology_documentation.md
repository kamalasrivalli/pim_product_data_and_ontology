# Language Ontology – Ontology Modelling with Protégé

## 1. Overview

This project models languages and their writing systems using an ontology developed in Protégé.

The ontology represents language categories, individual languages, writing systems and relationships between them.

## 2. Ontology Classes

The following classes were created:

| Class | Description |
|---|---|
| Language | Represents languages |
| LanguageFamily | Represents language families |
| WritingSystem | Represents writing systems |
| DravidianLanguage | Subclass of Language |
| IndoEuropeanLanguage | Subclass of Language |

## 3. Class Hierarchy

- Language
  - DravidianLanguage
  - IndoEuropeanLanguage
- LanguageFamily
- WritingSystem

## 4. Individuals

| Class | Individuals |
|---|---|
| DravidianLanguage | Telugu, Kannada |
| IndoEuropeanLanguage | English, German |
| WritingSystem | TeluguScript, KannadaScript, LatinScript |

## 5. Data Properties

### hasISOCode

Associates a language with its ISO 639-3 language code.

- Domain: Language
- Range: xsd:string

| Language | ISO 639-3 code |
|---|---|
| Telugu | tel |
| Kannada | kan |
| English | eng |
| German | deu |

## 6. Object Properties

### usesWritingSystem

Connects a language with its writing system.

- Domain: Language
- Range: WritingSystem

Relationships modelled:

- Telugu → TeluguScript
- Kannada → KannadaScript
- English → LatinScript
- German → LatinScript

### isWritingSystemOf

Inverse property of `usesWritingSystem`.

Represents the reverse relationship between a writing system and a language.

## 7. OWL Modelling Concepts Explored

The ontology work also explored:

- Class hierarchies and subclass relationships.
- Individuals and class membership.
- Object properties and data properties.
- Domain and range restrictions.
- Inverse properties.
- Disjoint classes.
- Existential, universal and cardinality restrictions.
- Reasoner-based consistency checking using HermiT.

## 8. Technologies and Tools

- Protégé Desktop
- Web Ontology Language (OWL)
- Resource Description Framework (RDF)
- RDF Schema (RDFS)
- HermiT reasoner

## 9. Project File

The ontology is stored in RDF/XML format:

`ontology/language_ontology.rdf`

## 10. Learning Outcome

This project provided practical experience in representing structured knowledge through ontology classes, individuals, properties and relationships, alongside an introduction to logical constraints and ontology reasoning.