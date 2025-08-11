# 📚 Vector QA App

A document-based question answering system that supports both Bangla and English languages. Upload PDF or text documents and ask questions to get relevant answers from your documents using vector similarity search.

## ✨ Features

- **Multi-language Support**: Works with both Bangla and English documents and queries
- **Document Upload**: Support for PDF and plain text files
- **Vector Search**: Uses ChromaDB for efficient similarity search
- **Real-time Processing**: Instant document processing and chunking
- **Web Interface**: Clean Streamlit-based user interface
- **Docker Support**: Easy deployment with Docker

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **PDF Processing**: PDFPlumber
- **Text Processing**: Tiktoken
- **Similarity Search**: Scikit-learn

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd vectorqa-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🐳 Docker Setup

### Build and Run with Docker

1. **Build the Docker image**
   ```bash
   docker build -t vectorqa-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 vectorqa-app
   ```

3. **Access the application**
   Open `http://localhost:8501` in your browser

### Docker Compose (Optional)

Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  vectorqa-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
```

Run with:
```bash
docker-compose up
```

## 📖 How to Use

1. **Upload Documents**
   - Use the sidebar to upload PDF or text files
   - Supported formats: `.pdf`, `.txt`
   - Both Bangla and English documents are supported

2. **Process Documents**
   - Click "Process Document" after uploading
   - The system will chunk and embed your document

3. **Ask Questions**
   - Enter your question in Bangla or English
   - Click "Search" to find relevant answers
   - View similarity scores and source chunks

## 📁 Project Structure

```
vectorqa-app/
├── app/
│   ├── main.py          # Main Streamlit application
│   ├── embed.py         # Embedding model handling
│   ├── ingest.py        # Document processing and chunking
│   ├── search.py        # Search engine logic
│   └── vector_store.py  # ChromaDB vector store operations
├── data/
│   ├── uploaded_docs/   # Uploaded documents storage
│   └── vectors/         # ChromaDB vector database
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ⚙️ Configuration

### Environment Variables

- `CHUNK_SIZE`: Text chunk size (default: 500)
- `OVERLAP`: Chunk overlap (default: 100)
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)

### Model Configuration

The app uses `all-MiniLM-L6-v2` for embeddings. To change the model, modify the `model_name` parameter in `app/embed.py`.

## 🔧 Development

### Running in Development Mode

```bash
streamlit run app/main.py --server.runOnSave true
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 API Reference

### Core Components

- **DocumentIngestor**: Handles file upload and text extraction
- **EmbeddingModel**: Generates vector embeddings
- **VectorStore**: Manages ChromaDB operations
- **SearchEngine**: Performs similarity search

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Memory Issues**
   - Reduce chunk size in `app/ingest.py`
   - Use smaller embedding models

3. **Docker Issues**
   - Ensure Docker is running
   - Check port availability (8501)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.