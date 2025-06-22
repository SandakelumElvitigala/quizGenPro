# MCQ Generator AI Agent

A powerful FastAPI-based application that generates multiple-choice questions (MCQs) from PDF documents or topics using the Groq API.

## ✨ Features

- 🎯 **Topic-based MCQ Generation** - Generate questions from any topic
- 📄 **PDF-based MCQ Generation** - Extract text from PDFs and create questions
- 🤖 **Groq API Integration** - Powered by advanced language models
- ⚙️ **Configurable Parameters** - Adjust difficulty, question types, and quantity
- 🔧 **Robust Error Handling** - Comprehensive error management and logging
- 🚀 **Production Ready** - Docker support, health checks, and monitoring
- 📚 **Interactive API Docs** - Built-in Swagger/OpenAPI documentation
- 🧪 **Comprehensive Tests** - Unit tests and integration tests included

## 🏗️ Project Structure

```
mcq-generator-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── utils/               # Utilities and helpers
│   └── routers/             # API route handlers
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
├── docker/                  # Docker configuration
├── docs/                    # Documentation
└── requirements.txt         # Dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key ([Get it here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcq-generator-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the server**
   ```bash
   python scripts/start_server.py
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📖 API Usage

### Generate MCQs from Topic

```bash
curl -X POST "http://localhost:8000/api/v1/generate/topic" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "Machine Learning Basics",
       "num_questions": 5,
       "difficulty": "medium",
       "question_type": "general"
     }'
```

### Generate MCQs from PDF

```bash
curl -X POST "http://localhost:8000/api/v1/generate/pdf" \
     -F "file=@document.pdf" \
     -F "num_questions=3" \
     -F "difficulty=easy"
```

### Response Format

```json
{
  "questions": [
    {
      "question": "What is machine learning?",
      "options": [
        {"option": "A) A type of hardware", "is_correct": false},
        {"option": "B) A subset of AI", "is_correct": true},
        {"option": "C) A programming language", "is_correct": false},
        {"option": "D) A database system", "is_correct": false}
      ],
      "explanation": "Machine learning is a subset of artificial intelligence..."
    }
  ],
  "generated_at": "2024-01-01T12:00:00",
  "source_type": "topic",
  "total_questions": 1
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `GROQ_MODEL` | Groq model to use | `llama-3.1-8b-instant` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_FILE_SIZE` | Max PDF file size | `10MB` |
| `MAX_QUESTIONS` | Maximum questions per request | `20` |

### Difficulty Levels

- **easy**: Basic questions testing recall and understanding
- **medium**: Moderate questions requiring analysis
- **hard**: Advanced questions requiring critical thinking

### Question Types

- **general**: Mixed question types
- **analytical**: Analysis and reasoning focused
- **factual**: Fact-based questions

## 🐳 Docker Deployment

### Using Docker Compose

```bash
cd docker
docker-compose up -d
```

### Using Docker directly

```bash
docker build -f docker/Dockerfile -t mcq-generator .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key mcq-generator
```

## 🧪 Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 📊 Monitoring

### Health Checks

- **Health**: `GET /health` - Overall application health
- **Ready**: `GET /ready` - Readiness probe for deployments
- **Live**: `GET /live` - Liveness probe for deployments

### Logging

The application uses structured logging with configurable levels:

- **ERROR**: Error conditions
- **WARNING**: Warning conditions  
- **INFO**: General information (default)
- **DEBUG**: Detailed debugging information

## 🔧 Development

### Code Quality

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## 🚨 Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found"**
   - Ensure your API key is set in environment variables or `.env` file

2. **"PDF extraction failed"**
   - Check if PDF is password-protected
   - Ensure PDF contains extractable text

3. **"Token limit exceeded"**
   - Large PDFs are automatically truncated
   - Consider splitting large documents

4. **Connection errors**
   - Check your internet connection
   - Verify Groq API service status

### Debugging

Enable debug mode:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the AI API
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing

## 📞 Support

For support, please open an issue on GitHub or contact [your.email@example.com](mailto:your.email@example.com).

---

Made with ❤️ by [Your Name]