import { http } from './client'

export const getOrganizationsAPI = async () => {
  return await http.get('/organizations')
}
