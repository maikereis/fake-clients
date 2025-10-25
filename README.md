# Client Data Generator
A Python utility for generating realistic Brazilian client data (individuals and companies) for testing and development purposes.

---
## Overview
This tool creates synthetic client records with authentic Brazilian formatting, including CPF/CNPJ numbers, names with proper prefixes, and localized date formats. It's designed for populating test databases, development environments, or data analysis scenarios.
## Features

* Individual Clients: Generates personal data with CPF, birth date, mother's name, and genre
* Company Clients: Creates business entities with CNPJ and company names
* Brazilian Localization: Uses pt_BR locale for authentic names and document formats
* Configurable Ratios: Adjustable person-to-company ratio
* CSV Export: Outputs randomized records to CSV format

## Usage
Basic Generation
```python
from main import generate_clients, save_clients_to_csv

# Generate 9,900 individuals and 99 companies (default 100:1 ratio)
clients = generate_clients(population_size=9900, ratio=100)
save_clients_to_csv(clients, filename="data/clients.csv")
```
