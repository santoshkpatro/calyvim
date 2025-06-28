import { http } from '@/api/client'

export const loginAPI = (data) => {
  return http.post('/accounts/login', data)
}
