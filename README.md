# Document Q & A

This is a Streamlit application that allows users to chat with the content of multiple PDFs. The application reads and processes the text from the PDFs, generates embeddings for the text chunks, and uses a retrieval-based conversation model to answer user questions about the content of the PDFs.

The application uses OpenAI's language model for embeddings and generating responses, the FAISS library for efficient similarity search, and a conversation buffer memory to keep track of the chat history.

## Dependencies

You need to install the following dependencies to run the application:

- Python 3.8 or later
- `streamlit`
- `python-decouple`
- `PyPDF2`
- `langchain`
- `htmllayouts`

## Environment Variables

You need to set the following environment variable:

- `OPENAI_KEY` - Your OpenAI API key. If this is not set, the application will not run.

## Usage

1. Install the required dependencies.
2. Set the `OPENAI_KEY` environment variable.
3. Run the application with the command `streamlit run app.py`.

## Interface

The application has a text input where you can ask a question about the content of your PDFs. Below it, the conversation history is displayed.

In the sidebar, there is a file uploader where you can upload your PDFs. After uploading your PDFs, click on the "Process" button. The application will read the PDFs, split the text into chunks, create embeddings for the chunks, and prepare the conversation model.

After processing the PDFs, you can ask questions about the content of the PDFs in the text input.

## How It Works

1. The PDFs are read and the text is extracted.
2. The extracted text is split into chunks. Each chunk is a separate "document" for the conversation model.
3. The chunks are embedded using OpenAI's language model. The embeddings are stored in a vector store using FAISS.
4. A conversation chain is created. The conversation chain uses the vector store to retrieve relevant chunks based on a user's question and a language model to generate a response. The conversation history is stored in a buffer.
5. When a user asks a question, the conversation chain retrieves the most relevant chunks, generates a response, and updates the conversation history.
6. The conversation history is displayed in the main part of the application.

## Note

This application is meant to be a demonstration of how one can build a retrieval-based conversation model using OpenAI's language model and other open-source libraries. It is not intended to be used for sensitive information or at scale.

## License

This project is licensed under the terms of the MIT license.
