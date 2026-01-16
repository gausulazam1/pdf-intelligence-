import json
import os
import time
from datetime import datetime
from typing import Dict, List
import PyPDF2
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm


class DocumentProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.model.eval()

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF with page numbers."""
        text_by_page = {}
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                if text and text.strip():
                    text_by_page[page_num + 1] = text
        return text_by_page

    def split_into_sections(self, text: str) -> List[str]:
        """Split text into meaningful sections."""
        sections = []
        current_section = []

        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current_section:
                    sections.append(' '.join(current_section))
                    current_section = []
                continue

            if line.isupper() or line.endswith(':'):
                if current_section:
                    sections.append(' '.join(current_section))
                    current_section = []

            current_section.append(line)

        if current_section:
            sections.append(' '.join(current_section))

        return sections

    def calculate_relevance(self, sections: List[str], task_embedding: torch.Tensor) -> List[float]:
        """Calculate relevance scores for sections based on task."""
        section_embeddings = self.model.encode(sections, convert_to_tensor=True)
        similarities = torch.nn.functional.cosine_similarity(
            section_embeddings, task_embedding.unsqueeze(0)
        )
        return similarities.tolist()

    def process_collection(self, collection_path: str) -> Dict:
        """Process an entire collection of documents."""
        with open(os.path.join(collection_path, 'input.json'), 'r') as f:
            input_data = json.load(f)

        task_text = f"{input_data['persona']['role']}: {input_data['job_to_be_done']['task']}"
        task_embedding = self.model.encode(task_text, convert_to_tensor=True)

        extracted_sections = []
        subsection_analysis = []

        for doc in tqdm(input_data['documents'], desc="Processing documents"):
            pdf_path = os.path.join(collection_path, 'pdfs', doc['filename'])
            text_by_page = self.extract_text_from_pdf(pdf_path)

            for page_num, text in text_by_page.items():
                sections = self.split_into_sections(text)
                relevance_scores = self.calculate_relevance(sections, task_embedding)

                for section, score in zip(sections, relevance_scores):
                    if len(section.split()) > 10:  # Skip very short sections
                        section_title = section.split('\n')[0][:100]
                        extracted_sections.append({
                            "document": doc['filename'],
                            "section_title": section_title,
                            "score": float(score),  # Keep original score for sorting
                            "page_number": page_num
                        })

                        subsection_analysis.append({
                            "document": doc['filename'],
                            "refined_text": section,
                            "page_number": page_num
                        })

        # Sort sections by descending score
        extracted_sections.sort(key=lambda x: x['score'], reverse=True)

        # Take top 20
        extracted_sections = extracted_sections[:20]
        subsection_analysis = subsection_analysis[:20]

        # Assign integer importance rank 1 (most important) to 20
        for i, section in enumerate(extracted_sections):
            section["importance_rank"] = i + 1
            del section["score"]  # Remove raw score if not needed

        output = {
            "metadata": {
                "input_documents": input_data['documents'],
                "persona": input_data['persona'],
                "job_to_be_done": input_data['job_to_be_done'],
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }

        return output


def main():
    processor = DocumentProcessor()
    collections = ['collection 1', 'collection 2', 'collection 3']

    for collection in collections:
        print(f"\nProcessing {collection}...")
        start_time = time.time()

        try:
            output = processor.process_collection(collection)

            output_path = os.path.join(collection, 'output.json')
            with open(output_path, 'w') as f:
                json.dump(output, f, indent=4)

            processing_time = time.time() - start_time
            print(f"Processed {collection} in {processing_time:.2f} seconds")

        except Exception as e:
            print(f"Error processing {collection}: {str(e)}")


if __name__ == "__main__":
    main()
