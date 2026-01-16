# Approach Explanation: Persona-Driven Document Intelligence

Our solution implements an efficient and lightweight document analysis system that processes PDF collections based on specific personas and their tasks. Here's how it works:

## Core Components

1. **Lightweight Language Model**

    - Uses the all-MiniLM-L6-v2 model (size: ~90MB) for semantic understanding
    - Optimized for CPU processing while maintaining high accuracy
    - Runs offline without internet connectivity

2. **Document Processing Pipeline**

    - Extracts text from PDFs using PyPDF2
    - Intelligently splits content into meaningful sections
    - Preserves document structure and page numbers
    - Handles various document formats and layouts

3. **Relevance Ranking System**
    - Creates embeddings for both task description and document sections
    - Computes cosine similarity for precise relevance scoring
    - Ranks sections based on importance to the persona's task
    - Filters out irrelevant or too short sections

## Key Features

1. **Persona-Task Understanding**

    - Combines persona role and task description for context
    - Creates a unified embedding that captures intent
    - Uses this context to evaluate document sections

2. **Efficient Processing**

    - Processes documents in parallel where possible
    - Implements early filtering of irrelevant content
    - Maintains processing time under 60 seconds for 3-5 documents
    - Memory-efficient section processing

3. **Structured Output**
    - Generates clean, hierarchical JSON output
    - Includes metadata, ranked sections, and detailed analysis
    - Preserves document references and page numbers
    - Provides refined text for each relevant section

## Performance Optimization

-   Model size: ~90MB (well under 1GB limit)
-   CPU-only processing with PyTorch
-   Efficient text extraction and processing
-   Smart batching of embedding calculations
-   Early filtering of irrelevant sections

This approach provides a robust, efficient, and accurate solution for persona-driven document analysis while meeting all technical constraints.
