# BioAgent

A multi-agent bioinformatics tool that combines BLAST sequence analysis with scientific literature search, powered by LLM interpretation.

## Features

- **BLAST Agent**: Runs BLAST searches against NCBI databases and interprets results using GPT-4
- **PubMed Agent**: Searches scientific literature based on BLAST hits and synthesizes findings
- **Combined Analysis**: Provides integrated interpretation of sequence identity and relevant research

## Installation

```bash
pip install biopython openai python-dotenv
```

## Configuration

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
ENTREZ_EMAIL=your_email@example.com
```

## Usage

```python
from agents.blast_agent import blast_agent
from agents.pubmed_agent import pubmed_agent

# Analyze a protein sequence
sequence = "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"

# Run BLAST analysis
blast_results = blast_agent(sequence, sequence_type="protein")

# Search related literature
literature_results = pubmed_agent(blast_results["hits"])
```

## Project Structure

```
bioagent/
├── agents/
│   ├── blast_agent.py    # BLAST search and LLM interpretation
│   └── pubmed_agent.py   # PubMed search and literature synthesis
├── utils/
│   └── blast_utils.py    # NCBI BLAST utilities
└── main.py               # Example usage
```
