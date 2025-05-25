import { IconLayoutDashboard, IconHeart, IconDatabase } from '@tabler/icons-react'
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
          title: 'New Monitoring Experiment',
          url: '/monitoring/new-experiment',
          icon: IconHeart,
        },
        {
          title: 'Data History',
          url: '/data-history',
          icon: IconDatabase,
        },
      ],
    },
  ],
}
