import axios from 'axios'

export async function checkAuthStatus() {
  try {
    const { data } = await axios.get('/api/accounts/me')

    if (data.result.isAuthenticated) {
      return data.result.user
    }

    return null
  } catch (error) {
    console.error('Auth check failed:', error)

    return null
  }
}
