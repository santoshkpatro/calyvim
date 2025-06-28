import { http } from '@/api/client'

export const getTeamDetailsAPI = (teamId) => {
  return http.get(`/teams/${teamId}`)
}
