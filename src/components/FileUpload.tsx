import { useState } from 'react';
import { chatAPI } from '../services/api';
import './FileUpload.css';

const FileUpload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setMessage('');

    try {
      const result = await chatAPI.uploadFile(file);
      setMessage(`✅ ${result.filename} uploaded and indexed successfully!`);
    } catch (error) {
      console.error('Upload error:', error);
      setMessage('❌ Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
      // Reset input
      e.target.value = '';
    }
  };

  return (
    <div className="file-upload">
      <label className="upload-button">
        {isUploading ? '⏳ Uploading...' : '📤 Upload Document'}
        <input
          type="file"
          accept=".txt,.md,.pdf,.docx"
          onChange={handleFileChange}
          disabled={isUploading}
          style={{ display: 'none' }}
        />
      </label>
      {message && <div className="upload-message">{message}</div>}
    </div>
  );
};

export default FileUpload;
