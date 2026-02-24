import axios from 'axios'

export async function uploadCSV(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await axios.post('https://nirikshan-pfxs.onrender.com/dashboard', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}
