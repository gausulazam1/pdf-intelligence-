# PDF Intelligence - Round 1B

A persona-driven document intelligence system that extracts and prioritizes relevant sections from PDF collections based on specific personas and their tasks.

## Features

-   Process multiple PDF collections
-   Persona and task-based relevance ranking
-   Efficient CPU-only processing
-   Offline capable
-   Structured JSON output

## Requirements

-   Python 3.9+
-   CPU with 4GB+ RAM
-   Docker (optional)

## Quick Start

### Using Docker

1. Build the Docker image:

```bash
docker build -t pdf-intelligence-r1b .
```

2. Run the container:

```bash
docker run -v ${pwd}:/app pdf-intelligence-r1b
```

### Manual Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Input Format

Place your collections in separate directories with the following structure:

```
collection_n/
├── input.json
├── output.json
└── pdfs/
    └── document1.pdf
    └── document2.pdf
    ...
```

The input.json should follow this format:

```json
{
    "challenge_info": {
        "challenge_id": "round_1b_XXX",
        "test_case_name": "test_case_name"
    },
    "documents": [
        {
            "filename": "doc.pdf",
            "title": "Document Title"
        }
    ],
    "persona": {
        "role": "User Persona"
    },
    "job_to_be_done": {
        "task": "Task Description"
    }
}
```

## Output Format

The system generates an output.json with:

-   Metadata (input documents, persona, task, timestamp)
-   Extracted sections with importance ranking
-   Detailed subsection analysis

## Performance

-   Processing time: < 60 seconds for 3-5 documents
-   Model size: ~90MB
-   CPU-only processing
-   No internet required during execution

## Technical Details

See `approach_explanation.md` for detailed information about the implementation approach and methodology.
