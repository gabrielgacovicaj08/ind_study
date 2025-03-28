# Introduction
Retrieving information about a college has never been easy—whether it's finding out which classes are offered next semester, the deadline to drop a class, or how to apply for a scholarship. Typically, searching for these answers online leads to the school’s website, which is filled with numerous tabs and pages, requiring time and effort to navigate. This process can be frustrating and discouraging, especially for students who need quick and accurate information.<br>

This led me to think: why not leverage AI to simplify and streamline this experience? That’s when I discovered Retrieval-Augmented Generation (RAG) models—a powerful AI approach that combines the ability to retrieve relevant information from an external knowledge base with the natural language generation capabilities of large language models. By implementing a RAG model, we can create an intuitive and efficient system that allows students to get precise answers instantly, without the hassle of searching through multiple pages.

## What is RAG?
RAG (Retrieval-Augmented Generation) is an AI approach that enables the creation of a chatbot capable of answering questions based on a specific set of information—in simple terms, it allows AI to retrieve and generate responses using a knowledge source of your choice.<br>
A RAG model consists of three key components:<br>
**External Knowledge Database** – Stores and organizes relevant information.<br>
**Retriever** – Searches the database to find the most relevant documents based on the user’s query.<br>
**LLM (Large Language Model)** – Processes the retrieved data and generates a natural-language response.<br>
Here’s a visual representation of how the pipeline works:
![Screenshot 2025-03-25 215821](https://github.com/user-attachments/assets/c5e86aed-1060-4bd5-96ea-893778a658cc)<br>
As you can see from the picture the most important part of a RAG model is the External Knowledge Database. 

## External Knowledge Database 
The external knowledge database is the backbone of a Retrieval-Augmented Generation (RAG) model because it ensures accuracy, relevance, and adaptability. Unlike traditional language models that rely solely on pre-trained data, a RAG model retrieves real-time, domain-specific information from an indexed database before generating a response. This significantly reduces hallucinations and enhances reliability by grounding responses in factual sources. Additionally, the external database allows for dynamic updates, ensuring the system remains current without requiring costly model retraining. Whether applied in legal, medical, or enterprise AI, the ability to retrieve precise and up-to-date knowledge makes the external database the most critical component of an effective RAG system.

## What is the reason of this independent study
The purpose of this study is to develop the most reliable and accurate chatbot designed to assist students and the community in accessing important college-related information quickly and effortlessly. Traditional search methods can be time-consuming and frustrating, often requiring users to navigate through multiple web pages to find the answers they need. By leveraging Retrieval-Augmented Generation (RAG) models, I aim to create an AI-driven solution that provides precise and contextual responses in real time. To achieve this, I will conduct an in-depth exploration of each core component of the RAG model—the External Knowledge Database, Retriever, and Large Language Model (LLM)—to understand how they work together to enhance information retrieval and response generation. Through this research, I seek to refine and optimize the chatbot, ensuring it delivers fast, accurate, and user-friendly assistance to students and the broader community.
