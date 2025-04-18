import { IconLayoutDashboard, IconHeart } from '@tabler/icons-react'
import { type SidebarData } from '../types'

export const sidebarData: SidebarData = {
  user: {
    name: 'Rubem',
    email: 'joserubem@ua.pt',
    avatar: '/avatars/shadcn.jpg',
  },
  navGroups: [
    {
      title: 'General',
      items: [
        {
          title: 'Dashboard',
          url: '/',
          icon: IconLayoutDashboard,
        },
        {
          title: 'New Monitoring Session',
          url: '/monitoring/new-experiment',
          icon: IconHeart,
        },
      ],
    },
  ],
}
