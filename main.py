import requests, time, os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

#Document file
def load_document(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
#AI prompt
def build_prompt(document_text, question):
    return f"""Answer ONLY using the document below. Do not use any outside knowledge.
If the information is not explicitly stated in the document, respond 
exactly with: "I don't know based on this document."

Document: {document_text}
Question: {question}
"""
# AI Answer
def get_answer(document_text, question):
    prompt = build_prompt(document_text, question)
    response = ask_llm(prompt)
    return response

#Ask LLM
def ask_llm(prompt, retries=3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            if "error" in data:
                print(f"API error: {data['error']['message']}")
                if data["error"].get("status") in ["UNAVAILABLE", "RESOURCE_EXHAUSTED"]:
                    time.sleep(5)
                    continue
                return "Sorry, the AI service returned an error."

            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return reply

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Sorry, couldn't reach the AI service right now."

    return "Sorry, the AI service is currently overloaded. Please try again shortly."

#Split the chunks into size 500 words
def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Find best related words
def find_best_chunk(chunks, question):
    question_words = set(question.lower().split())
    best_chunk = ""
    best_score = 0
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        overlap = len(question_words & chunk_words)
        if overlap > best_score:
            best_score = overlap
            best_chunk = chunk
    return best_chunk

# Give input to get output
def main():
    filename = input("Enter document filename: ")
    document_text = load_document(filename)

    print("Document loaded. Ask your questions (type 'exit' to quit)\n")

    while True:
        question = input("Your question: ")

        if question.lower() == "exit":
            print("Thank you for your question.")
            break

        answer = get_answer(document_text, question)
        print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()
