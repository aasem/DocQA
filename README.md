# Document Question & Answer App
This application provides a simple interface to upload a document file (txt, pdf, docx, csv, xlsx) and then ask questions related to the content of the document. The system uses language processing models to extract relevant answers from the uploaded document.

## Setup
The project requires Python 3.7+ and some dependencies from the Python Package Index.

Dependencies:

- Flask (for the web server)
- python-docx (to read Word files)
- PyPDF2 (to read PDF files)
- pandas (to read CSV and Excel files)
- OpenAI's language models (for question answering)

You can install these dependencies like this:

```
pip install Flask python-docx PyPDF2 pandas openai
```

## Configuration
You need an API key from OpenAI to use their language models. You can get one from their [website](https://openai.com/).

The API key should be set in an environment variable like this:

```
export OPENAI_KEY=your-key-here
```

## Running the Application
You can start the web server like this:

```
python app.py
```

Once the server is running, you can access the application at http://localhost:5000 in your web browser.

## Usage
- Upload a document file using the "Choose a file" button.
- Click the "Upload" button to proceed.
- You will be directed to a new page where you can enter your questions about the document content.
- The application will display the answers to your questions on the same page.

## Contributing
Feel free to fork the project, make some changes, and submit pull requests. The project is open-source and welcomes contributions.

## License
The project is licensed under the terms of the MIT license.