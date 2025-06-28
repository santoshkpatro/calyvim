import { createAvatar } from '@dicebear/core'
import { initials } from '@dicebear/collection'

export const teamAvatar = (name) => {
  return createAvatar(initials, {
    seed: name,
    radius: 10,
    backgroundColor: ['D8DBD3'],
    textColor: ['000000'],
    fontSize: 50,
    fontWeight: 800,
  }).toDataUri()
}
