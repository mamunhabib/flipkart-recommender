import pandas as pd
from langchain_core.documents import Document

class DataConverter:
    def __init__(self, file_path: str = "data/flipkart_product_review.csv"):
        self.file_path = file_path

    def convert(self):
        """Reads the CSV and converts rows into LangChain Documents"""
        print(f"Reading dataset from: {self.file_path}...")
        
        # Load the CSV using Pandas, selecting only the necessary columns
        df = pd.read_csv(self.file_path)[["product_title", "review"]]   

        # Loop through each row and convert it into a LangChain Document object
        docs = [
            Document(
                page_content=row['review'], 
                metadata={"product_name": row["product_title"]}
            )
            for _, row in df.iterrows()
        ]
        
        print(f"Successfully converted {len(docs)} reviews into Document objects.")
        return docs
