# FHIR-Aggregator
FHIR client for python3. 

This package provides:
* A low level API for Search/Read operations over multiple FHIR resources.
* Managing client side credentials for FHIR servers.
* Support for broadcasting a query to multiple FHIR servers.
* A high level API for common operations on returned FHIR resources.


## overview

[websequence](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgZmhpci1hZ2dyZWdhdG9yCgphY3RvciBSZXNlYXJjaGVyCnBhcnRpY2lwYW50AB0RABAMc2VydmVyX0EAARRCABYUQwoKb3B0IGRlcGVuZGVuY2llcwoAbgotLT4Aewo6IGNvbXBvc2UgRkhJUiBxdWVyABEdb2J0YWluIGNyZWRlbnRpYWxzCmVuZABqBnJlZ2lzdGVyAGAMPisAgXkPOgAeCS0AOgsoAIFcCCwAgVAJLCAuLi4pCgCCOA8tPgBAEHNhdmUoY29uZmlnX2RpcgAgEi0-LQCBZAxPSwCBKAoAgwUGCgCBEh8AgysGKACCFQcpCgpsb29wIGFzeW5jOmZvciBhbGwAgjAJbm90ZSByaWdodCBvZgCDdBA6IHRocmVhZCBmb3IAg00JAIFmDACDNwkAgVUhIG5vcm1hbGl6ZQCBEwV5AIIWEwCELwgAgTQNeSkKYWN0aXZhdACFEBIAhGAILQBcE3Jlc3VsdAAiGgBjGwA1BihuZXh0KQBHHXBhZ2UKZGUAgQcZAAEaABocCmVuZCAKAIQDEwCFdw5uc29saWRhdGVkIHJlc291cmNlcwA3BQCGRgZwb3N0LXByb2Nlc3MAhCIOAIVPEW1ldHJpY3MoAD4JAIJYGwCDRiJjb25mb3JtYW5jZQBGDACBMR4AfAcAgXodAIEnHQCEVAoAgQBGAIUlCS10ZXJtAIIPDQCCex4AgwIKAIN-GwCIfQUAhnUFbGVmAIZ0BQCJVQxkb3duc3RyZWFtIGFuYWx5c2lz&s=default) diagram for the high level API:
![image](docs/overview.png)


## Installation

```bash
pip install fhir_aggregator
```

## Usage

```bash
fhir-aggregator 
Usage: fhir-aggregator [OPTIONS] COMMAND [ARGS]...

  FHIR Aggregator Command Line Interface.

Options:
  --help  Show this message and exit.

Commands:
  create-metrics        Creates metrics from search results stored in a...
  normalize-results     Normalizes search results stored in a file.
  register-credentials  Registers a credentials file.
  search-queries        Reads a YAML file of queries and searches all...

```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to the project.
