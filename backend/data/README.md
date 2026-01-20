# Data Folder

This folder contains the documents that Isabella uses for her knowledge base.

## Supported File Types

- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.docx` - Word documents

## How It Works

1. **Add Documents**: Place your documents in this folder
2. **Auto-Indexing**: The system will automatically detect and index new files
3. **RAG Retrieval**: Isabella can now search and reference these documents in her responses

## Sample Documents

To help you get started, here are some sample documents you can create:

### Example 1: About Your Company (company_info.md)
```markdown
# About Our Company

Founded in 2020, we are a leading provider of AI solutions...

## Our Services
- AI Consulting
- Machine Learning Development
- Data Analytics

## Contact
Email: info@example.com
Phone: 555-0123
```

### Example 2: FAQ (faq.txt)
```
Frequently Asked Questions

Q: How do I reset my password?
A: Click "Forgot Password" on the login page...

Q: What are your business hours?
A: Monday-Friday, 9am-5pm EST...
```

### Example 3: Technical Documentation (api_docs.md)
```markdown
# API Documentation

## Authentication
Use Bearer token in the Authorization header...

## Endpoints
GET /api/users - List all users
POST /api/users - Create new user
```

## Tips for Better Results

1. **Clear Structure**: Use headings and organize content logically
2. **Chunk-Friendly**: Break long documents into sections
3. **Relevant Content**: Add documents related to questions users will ask
4. **Update Regularly**: Add new documents as your knowledge base grows
5. **Quality Over Quantity**: Well-written documents get better results

## Re-indexing

The system automatically re-indexes when:
- New files are added
- Existing files are modified
- Files are deleted

You can also upload files via the web interface using the "📤 Upload Document" button.

## Current Status

To see how many documents are indexed, visit the `/api/stats` endpoint or check the backend logs on startup.

---

**Ready to add your knowledge base? Just drop your files here!** 📚
