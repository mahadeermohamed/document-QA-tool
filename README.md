# DocQuery — Ask Questions About Any Document

A CLI tool that answers questions about a text document using an LLM, 
grounded strictly in the document's content — no hallucinated answers.

## Why I built this
To practice a core AI-app pattern: giving an LLM context and constraining 
its answers to that context, plus handling documents longer than the 
model's context window.

## How it works
1. User loads a text document
2. User asks a question
3. App finds the most relevant section of the document (basic chunking 
   for longer docs)
4. That section + question are sent to the LLM with instructions to 
   answer only from the given text
5. Answer is printed; if not found in the document, it says so honestly

## Tech stack
Python, requests, Gemini API, python-dotenv

## How to run
1. Clone this repo
2. Add your API key to `.env` (see `.env.example`)
3. `pip install -r requirements.txt`
4. `python main.py`

## Example output
Load document: notes.txt
Ask a question (or 'exit'): What is the refund policy?
Refunds are processed within 7 business days of the return request.
Ask a question (or 'exit'): What is the CEO's name?
I don't know based on this document.

## What I learned
How context window limits work, basic text chunking to handle long 
documents, and prompt design to prevent hallucinated answers — this is 
a simplified version of what's called "RAG" (retrieval-augmented 
generation) in real AI systems.