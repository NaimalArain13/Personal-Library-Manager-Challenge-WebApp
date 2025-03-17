import streamlit as st
import json


# Load the library data from a file
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save the library data to a file
def save_library(library):
    with open("library.json", "w") as file:
        json.dump(library, file)


library = load_library()


st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add a Book",
        "Remove a Book",
        "Search for a Book",
        "Display All Books",
        "Statistics",
        "Clear Your Library"
    ],
)

# 📌 **1. Add a Book**
if menu == "Add a Book":
    # # Initialize session state variables (only runs on first load)
    # if "title" not in st.session_state:
    #     st.session_state.title = ""
    # if "author" not in st.session_state:
    #     st.session_state.author = ""
    # if "year" not in st.session_state:
    #     st.session_state.year =  ""
    # if "genre" not in st.session_state:
    #     st.session_state.genre = ""
    # if "read" not in st.session_state:
    #     st.session_state.read = ""


    # 📌 **Function to Reset Form**
    # def reset_form():
    #     # Resetting session state variables
    #     st.session_state.title = ""
    #     st.session_state.author = ""
    #     st.session_state.year = ""
    #     st.session_state.genre = ""
    #     st.session_state.read = ""

    
    # 📌 **Add a Book Section**
    st.header("➕ Add a Book")
    title = st.text_input("Enter Book Title", key="title")
    author = st.text_input("Enter Author", key="author")
    year = st.number_input(
    "Publication Year", min_value=0, max_value=2050, step=1, key="year"
    )
    genre = st.text_input("Enter Genre", key="genre")
    read = st.checkbox("Have you read this book?", key="unread")

    if st.button("Add Book"):
        book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read,
        }

        # Append book to the library
        library.append(book)

        # Save the library (Ensure this function is defined in your script)
        save_library(library)

        st.success(f"📖 '{title}' added successfully!")

        # Reset form fields **AFTER** book is added
        # reset_form()


elif menu == "Remove a Book":
    st.header("❌ Remove a Book")
    book_titles = [book["title"] for book in library]
    selected_book = st.selectbox("Select a Book to remove: ", book_titles)

    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != selected_book]
        save_library(library)
        st.success(f"🗑️ '{selected_book}' Remove successfully!")

# 📌 **3. Search for a Book**
elif menu == "Search for a Book":
    st.header("🔍 Search for a Book")

    search_option = st.radio("Search by:", ["Title", "Author"])
    search_query = st.text_input("Enter search query")

    if st.button("Search"):
        if search_option == "Title":
            results = [
                book
                for book in library
                if search_query.lower() in book["title"].lower()
            ]
        else:
            results = [
                book
                for book in library
                if search_query.lower() in book["author"].lower()
            ]

        if results:
            st.write("📖 **Matching Books:**")
            for book in results:
                st.write(
                    f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}"
                )
        else:
            st.warning("No matching books found.")


# 📌 **4. Display All Books**
elif menu == "Display All Books":
    st.header("📚 Your Library")

    if not library:
        st.info("Your library is empty.")
    else:
        for book in library:
            st.write(
                f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}"
            )


# 📌 **5. Display Statistics**
elif menu == "Statistics":
    st.header("📊 Library Statistics")

    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"📖 **Books Read:** {read_books}")
    st.write(f"📊 **Percentage Read:** {read_percentage:.2f}%")
    
    
# 📌 **5. Display Statistics**
elif menu == "Clear Your Library":
   library.clear()
   st.write("Your Library is Empty")

# Save changes
save_library(library)
