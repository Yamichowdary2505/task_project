from faq_service import get_faq_answer

print("🎬 Movie Recommendation Chatbot")
print("Type 'exit' to quit\n")

while True:
    user_input = input("Ask me about movies: ")
    if user_input.lower() == "exit":
        break
    answer = get_faq_answer(user_input)
    print(f"Bot: {answer}\n")
