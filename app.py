

import os
import uuid
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBChatMessageHistory
from flask_cors import CORS
# Load environment variables
load_dotenv()

# Retrieve and validate OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Retrieve and validate MongoDB connection string
mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
if not mongodb_connection_string:
    raise ValueError("MONGODB_CONNECTION_STRING is not set in the environment variables.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Load and process PDF document
pdf_path = "D:\Agentic AI\hello\hotel chatbot.pdf"  # Replace with the path to your PDF file
loader = PyPDFLoader(file_path=pdf_path)
documents = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30))

# Create embeddings and FAISS vector store
embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_documents(documents, embeddings)
retriever = vectordb.as_retriever()

# Initialize MongoDB client
try:
    mongo_client = MongoClient(mongodb_connection_string)
    # Optionally, verify the connection
    mongo_client.admin.command('ping')
    print("Connected to MongoDB successfully.")
except errors.ConnectionFailure as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")


@app.route('/chat', methods=['POST'])
def chat():
    # Retrieve form data
    user_id = request.form.get('userID')
    session_id = request.form.get('sessionID')
    user_input = request.form.get('message')

    # Validate form data
    if not user_id or not user_input:
        return jsonify({'error': 'userID and message are required fields.'}), 400

    # Generate a new session_id if not provided
    if not session_id:
        session_id = str(uuid.uuid4())
    unique_session_id = f"{user_id}_{session_id}"
    # Initialize chat message history
    chat_history = MongoDBChatMessageHistory(
        connection_string=mongodb_connection_string,
        session_id=unique_session_id
    )

    # Retrieve previous messages
    previous_messages = chat_history.messages
    print("previous messages",previous_messages)

    # Format chat history for the prompt
    formatted_history = ""
    for message in previous_messages:
        role = "User" if message.type == "human" else "AI"
        formatted_history += f"{role}: {message.content}\n"

    # Add the current user input to the history
    formatted_history += f"User: {user_input}\n"
    print("formatted history",formatted_history)
    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(user_input)
    #print("docs",docs)

    if docs:
        # If relevant documents are found, use them to generate a response
        context = " ".join([doc.page_content for doc in docs])
        print("context",context)
        prompt = f"Based on the following context and chat history, answer the question:\n\nContext: {context}\n\nChat History:\n{formatted_history}\nAI: \n and if user ask about certain location or places try your best to give him answer or give him suggestions."
    else:
        # If no relevant documents are found, use chat history only
        prompt = f"Based on the following chat history, answer the question:\n\nChat History:\n{formatted_history}\nAI:"

    # Generate AI response
    ai_message = llm(prompt,max_tokens=150)

    # Extract the content from the AIMessage object
    ai_content = ai_message.content if hasattr(ai_message, 'content') else str(ai_message)

    # Add user and AI messages to history
    chat_history.add_user_message(user_input)
    chat_history.add_ai_message(ai_content)

    return jsonify({'response': ai_content, 'sessionID': session_id})
if __name__ == '__main__':
    app.run(debug=True)

