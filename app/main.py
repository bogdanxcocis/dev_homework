from app.book_service import get_summary_by_title, is_valid_input, build_recommendation, generate_ai_response
from database import is_collection_empty, insert_books_into_db

if __name__ == "__main__":
    if is_collection_empty():
        try:
            print("Inserting data into the database.")
            insert_books_into_db()
            print("Data was inserted successfully into ChromaDB.")
        except Exception as error:
            print(f"There was a problem inserting data into the database: {error}")
    print("\nChoose an option:")
    print("1. Get full summary by title")
    print("2. Get book recommendation")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == "1":
        title = input("Enter a book title: ").strip()
        summary = get_summary_by_title(title)

        print(f'\nFull summary for "{title}":\n')
        print(summary)
    elif choice == "2":
        user_input = input("Tell me what kind of book you want: ").strip()
        if is_valid_input(user_input):
            recommendation = build_recommendation(user_input)
            if recommendation is None:
                print("I could not find a matching book.")
            else:
                response = generate_ai_response(user_input, recommendation)

                print("\nResponse:\n")
                print(response)
    else:
        print("Invalid option. Please select 1 or 2.")
