import axios from 'axios'
import Cookies from 'js-cookie'

export const http = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'X-CSRFToken': Cookies.get('csrftoken'),
  },
})
