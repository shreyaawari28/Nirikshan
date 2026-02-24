import { useState } from 'react'
import { uploadCSV } from '../services/api'

function UploadSection({ onDataLoaded, onUploadStart, onUploadEnd }) {
  const [selectedFile, setSelectedFile] = useState(null)

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files?.[0] ?? null)
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return

    onUploadStart?.()
    try {
      const response = await uploadCSV(selectedFile)
      onDataLoaded(response)
    } catch (error) {
      console.error(error)
    } finally {
      onUploadEnd?.()
    }
  }

  return (
    <div className="upload-card">
      <h3>Upload Dataset</h3>
      <div className="upload-section">
        <div className="file-upload">
          <input
            type="file"
            id="fileInput"
            accept=".csv,text/csv"
            onChange={handleFileChange}
            hidden
          />
          <label htmlFor="fileInput" className="file-label">
            {selectedFile ? selectedFile.name : 'Choose CSV File'}
          </label>
        </div>
        <button type="button" onClick={handleAnalyze}>
          Analyze
        </button>
      </div>
    </div>
  )
}

export default UploadSection
