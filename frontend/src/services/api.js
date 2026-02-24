import axios from 'axios'

export async function uploadCSV(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await axios.post('http://127.0.0.1:8000/dashboard', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}
