#!/usr/bin/env python
# coding: utf-8

import chromadb

def main():
    # Initialize ChromaDB client
    chroma_client = chromadb.Client()

    # Create a collection
    collection = chroma_client.create_collection(name="my_collection")

    # Add documents to the collection
    collection.add(
        ids=["id1", "id2"],
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges"
        ]
    )

    # Query the collection
    results = collection.query(
        query_texts=["This is a query document about hawaii"],
        n_results=2
    )
    print(results)

if __name__ == "__main__":
    main()
