# Flask Chatbot with OpenAI and MongoDB

This repository contains a Flask-based chatbot application that integrates OpenAI's GPT model, MongoDB for chat history storage, and FAISS for document retrieval. The chatbot can answer user queries, provide suggestions, and retrieve relevant context from a PDF document.

## Features

- **AI-Powered Chat**: Utilizes OpenAI's GPT model for conversational responses.
- **Document Retrieval**: Processes a PDF file and retrieves relevant information for user queries using FAISS.
- **MongoDB Integration**: Stores and retrieves chat history for personalized interactions.
- **Session Management**: Supports unique user sessions for continuity.
- **CORS Enabled**: Allows cross-origin resource sharing for integration with front-end applications.

## Prerequisites

- Python 3.8+
- MongoDB instance (local or cloud-based)
- OpenAI API Key

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in the root directory and add the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   MONGODB_CONNECTION_STRING=your_mongodb_connection_string
   ```

5. **Prepare the PDF Document**
   Place the PDF file (e.g., `hotel chatbot.pdf`) in the specified directory and update the `pdf_path` variable in the code.

## Usage

1. **Run the Flask App**
   ```bash
   python app.py
   ```

2. **Access the API**
   Use an HTTP client (e.g., Postman or cURL) to send POST requests to the `/chat` endpoint.

   Example Request:
   ```bash
   curl -X POST http://127.0.0.1:5000/chat \
        -d "userID=123" \
        -d "message=What is the best hotel in New York?"
   ```

   Example Response:
   ```json
   {
       "response": "Based on the provided context, the best hotels in New York include...",
       "sessionID": "12345-67890"
   }
   ```

## Project Structure

```plaintext
.
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not included in repo)
├── hotel chatbot.pdf     # Example PDF document (replace with your own)
└── README.md             # Project documentation
```

## Dependencies

- Flask
- Flask-CORS
- python-dotenv
- pymongo
- langchain
- FAISS
- PyPDFLoader
- OpenAI API

## Troubleshooting

- Ensure that your OpenAI API key and MongoDB connection string are set correctly in the `.env` file.
- Verify that the PDF file path is correct and the file exists.
- Check MongoDB connectivity using `mongo_client.admin.command('ping')`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have ideas for improvements or encounter any bugs.

## Acknowledgements

- [OpenAI](https://openai.com/) for the GPT model
- [MongoDB](https://www.mongodb.com/) for the database
- [LangChain](https://docs.langchain.com/) for document and chat management
