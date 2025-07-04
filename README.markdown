# RAG-PDF-QA: Interactive PDF Question Answering with RAG, Gemini, and Astra DB

![image](https://github.com/user-attachments/assets/24a1f511-46cb-4ab6-8b67-6107d3a254fb)

## Overview

RAG-PDF-QA is a Streamlit-based application designed to let users upload a PDF document and ask questions about its content through a user-friendly web interface. It employs a Retrieval-Augmented Generation (RAG) system, integrating Google Gemini models for advanced language understanding and generation with DataStax Astra DB for efficient storage and retrieval of document embeddings. The application extracts text from the uploaded PDF, splits it into manageable chunks, generates embeddings, and stores them in Astra DB. When a user asks a question, the system retrieves relevant document sections and uses the Gemini model to generate precise, contextually relevant answers.

This project is ideal for students, researchers, or professionals who need to quickly extract information from PDF documents, such as legal texts, academic papers, or technical manuals, without manually searching through pages.

## Features

- **PDF Upload and Processing**: Upload any PDF file, with text extracted and processed for analysis.
- **Interactive Question Answering**: Pose questions about the PDF content and receive accurate, AI-generated answers.
- **Streamlit Interface**: A clean, web-based interface for uploading PDFs and entering queries.
- **Advanced RAG Architecture**: Combines document retrieval with generative AI for contextually relevant responses.
- **Scalable Vector Storage**: Uses Astra DB to store and retrieve document embeddings efficiently.
- **Error Handling**: Checks for missing environment variables and provides clear error messages.

## Requirements

To run RAG-PDF-QA, you need the following:

### Software
- **Python**: Version 3.8 or higher.
- **Python Packages**:
  - `streamlit`: For the web-based user interface.
  - `python-dotenv`: For loading environment variables.
  - `langchain`: Core framework for building the RAG system.
  - `langchain-google-genai`: For Google Gemini model integration.
  - `langchain-community`: For Astra DB vector store integration.
  - `PyPDF2`: For extracting text from PDF files.
  - `cassio`: For connecting to Astra DB.

### Accounts and Credentials
- **Google Cloud Account**: Required for accessing Google Gemini models. Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).
- **Astra DB Account**: Required for vector storage. Sign up at [DataStax Astra DB](https://www.datastax.com/products/datastax-astra) and create a database with a table named "qa_streamlit_demo".
- **PDF File**: Any readable PDF document you wish to query.

### Environment Variables
Create a `.env` file in the project root directory with the following variables:
| Variable Name                | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `GOOGLE_API_KEY`             | Your Google API key for accessing Gemini models.                            |
| `ASTRA_DB_APPLICATION_TOKEN` | Your Astra DB application token for database access.                        |
| `ASTRA_DB_ID`                | Your Astra DB database ID.                                                 |
| `ASTRA_DB_KEYSPACE`          | The keyspace name in your Astra DB where the table is located.              |

Example `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_ID=your_astra_db_id
ASTRA_DB_KEYSPACE=your_astra_db_keyspace
```

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/RAG-PDF-QA.git
   cd RAG-PDF-QA
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install streamlit python-dotenv langchain langchain-google-genai langchain-community PyPDF2 cassio
   ```
   Alternatively, if a `requirements.txt` file is provided, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root with the environment variables listed above. Ensure all variables are correctly set, as the application checks for missing variables and will display an error if any are absent.

4. **Run the Application**:
   Launch the Streamlit app (assuming the script is named `app.py`):
   ```bash
   streamlit run app.py
   ```
   This will open the application in your default web browser.

## Usage

1. **Launch the Application**: Run the Streamlit command above to start the app.
2. **Upload a PDF**: Use the file uploader in the Streamlit interface to select and upload a PDF document.
3. **Processing**: The application will extract text from the PDF, split it into chunks, generate embeddings, and store them in Astra DB. A success message will appear when processing is complete.
4. **Ask Questions**: Enter a question about the PDF content in the provided text input field.
5. **View Answers**: The system will retrieve relevant document sections and display an AI-generated answer below the input field.

### Example Interaction
**Scenario**: A user uploads a PDF of the Art Of War.

**Question**: "how to deal with powerful foe, explain me in 50 words and chapters refer too"

**Answer**: To defeat a powerful foe, understand both your own strengths and weaknesses, and those of your enemy (Chapter 4, 18). Employ stratagem to lure them into disadvantageous positions (Chapter 4, 36), and avoid pushing a desperate enemy too hard (Chapter 4). Discover their plans and vulnerabilities (Chapter 7, 22-24).

![Screenshot 2025-07-04 160343](https://github.com/user-attachments/assets/0bf1cece-c3e1-43d4-8063-ad3d0fc9ed41)

## Comparison with Direct Gemini Answer
To highlight the effectiveness of the RAG system, here’s a comparison between the answer generated by RAG-PDF-QA and a direct answer from the Gemini model without retrieval.

**Question**: "how to deal with powerful foe, explain me in 50 words and chapters refer too"

**Answer**: To deal with a powerful foe, Sun Tzu advises deception and exploiting their weaknesses. Appear weak when strong, strong when weak, and attack where they are unprepared. Avoid their strengths and strike their vulnerabilities. Victory comes from knowing yourself and your enemy. (Chapters 1, 3, 6)

![Screenshot 2025-07-04 160321](https://github.com/user-attachments/assets/2b263936-5843-415a-95da-59341aa85857)

## How It Works

The application processes PDFs and answers questions through the following steps:

1. **PDF Text Extraction**: Uses `PyPDF2` to extract raw text from the uploaded PDF.
2. **Text Chunking**: Splits the text into smaller chunks (1000 characters with 200-character overlap) using `RecursiveCharacterTextSplitter` for efficient processing.
3. **Vector Storage**: Generates embeddings for each chunk using Google Gemini’s embedding model (`models/embedding-001`) and stores them in Astra DB’s vector store (`qa_streamlit_demo` table).
4. **Retriever Setup**: Creates a retriever from the vector store to fetch relevant chunks based on query embeddings.
5. **Prompt and RAG Chain**: Defines a conversational prompt template and builds a RAG chain that combines retrieved chunks with the Gemini language model (`models/gemini-1.5-flash-latest`) to generate answers.
6. **User Interaction**: Processes user queries through the Streamlit interface, retrieving relevant context and displaying AI-generated answers.

## Technology Stack

- **Frontend**: Streamlit for the web-based user interface.
- **Language Model**: Google Gemini (`models/gemini-1.5-flash-latest`) for answer generation.
- **Embeddings**: Google Gemini Embeddings (`models/embedding-001`) for vectorizing text.
- **Vector Store**: DataStax Astra DB via `langchain-community` for storing and retrieving embeddings.
- **PDF Processing**: `PyPDF2` for text extraction from PDFs.
- **Text Splitting**: LangChain’s `RecursiveCharacterTextSplitter` for chunking text.

## Setting Up Astra DB

1. Sign up for an account at [DataStax Astra DB](https://www.datastax.com/products/datastax-astra).
2. Create a new database in the Astra DB dashboard.
3. Generate an application token with permissions to access the database.
4. Note the database ID and keyspace name from the dashboard.
5. Create a table named `qa_streamlit_demo` in your keyspace using the Astra DB interface or CQL commands.
6. Update your `.env` file with the `ASTRA_DB_APPLICATION_TOKEN`, `ASTRA_DB_ID`, and `ASTRA_DB_KEYSPACE`.

For detailed instructions, refer to the [Astra DB Documentation](https://docs.datastax.com/en/astra/docs/).

## Obtaining Google API Key

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Generative AI API (or equivalent for Gemini models).
4. Create an API key under the “Credentials” section.
5. Copy the API key and add it to your `.env` file as `GOOGLE_API_KEY`.

Follow Google’s [API guidelines](https://cloud.google.com/docs/authentication/api-keys) for secure usage.

## Configuration Options

- **Model Selection**: The default language model is `models/gemini-1.5-flash-latest`. Modify the `model` parameter in the `ChatGoogleGenerativeAI` initialization to use other Gemini models.
- **Text Chunking**:
  - **Chunk Size**: Set to 1000 characters. Adjust in the `RecursiveCharacterTextSplitter` initialization.
  - **Chunk Overlap**: Set to 200 characters for context continuity. Modify as needed.
  ```python
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  ```
- **Astra DB Table**: The default table name is `qa_streamlit_demo`. Update the `table_name` in the `Cassandra` initialization if using a different table.
- **Temperature**: The language model’s temperature is set to 0.6 for balanced creativity. Adjust in the `ChatGoogleGenerativeAI` initialization for more deterministic or creative outputs.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Missing Environment Variables** | Check the `.env` file for `GOOGLE_API_KEY`, `ASTRA_DB_APPLICATION_TOKEN`, `ASTRA_DB_ID`, and `ASTRA_DB_KEYSPACE`. The app will display missing variables if any are absent. |
| **Astra DB Connection Failure** | Verify that the database ID, keyspace, and token are correct, and the `qa_streamlit_demo` table exists. Ensure network access to Astra DB. |
| **PDF Processing Errors** | Ensure the PDF is readable and not corrupted. Test with a different PDF if issues persist. |
| **Streamlit Not Running** | Confirm Streamlit is installed (`pip install streamlit`) and run the command from the correct directory. |
| **Dependency Errors** | Install all required packages listed in the Installation section. Use `pip list` to verify. |

For additional support, consult:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Google Gemini API Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Astra DB Documentation](https://docs.datastax.com/en/astra/docs/)

## Used cassandra vector db through DataStax Astra

![image](https://github.com/user-attachments/assets/e3dcad50-14c0-44b4-9266-e6f430250478)
