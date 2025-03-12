'use client';

import * as React from 'react';
import {
   AudioWaveform,
   BookOpen,
   Bot,
   Command,
   Frame,
   NotepadText,
   Map,
   PieChart,
   Settings2,
   PiggyBank,
   Bug,
   GalleryVerticalEnd,
} from 'lucide-react';

import { NavMain } from '@/components/nav-main';
import { NavUser } from '@/components/nav-user';
import { TeamSwitcher } from '@/components/team-switcher';
import {
   Sidebar,
   SidebarContent,
   SidebarFooter,
   SidebarHeader,
   SidebarMenu,
   SidebarMenuButton,
   SidebarMenuItem,
   SidebarRail,
} from '@/components/ui/sidebar';

// This is sample data.
const data = {
   navMain: [
      {
         title: 'FabBank',
         url: 'fabbank',
         icon: PiggyBank,
         isActive: true,
         items: [
            {
               title: 'Extrato',
               url: 'extrato',
            },
            {
               title: 'Transferir',
               url: '#',
            },
            {
               title: 'Loja',
               url: '#',
            },
         ],
      },
      {
         title: 'Baygon',
         url: '#',
         icon: Bug,
         items: [],
      },
      {
         title: 'Debriefing',
         url: '#',
         icon: NotepadText,
         items: [],
      },
   ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
   return (
      <Sidebar collapsible="icon" {...props}>
         <SidebarHeader>
            <SidebarMenu>
               <SidebarMenuItem>
                  <SidebarMenuButton size="lg" asChild>
                     <a href="#">
                        <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                           <Bot className="size-4" />
                        </div>
                        <div className="flex flex-col gap-0.5 leading-none">
                           <span className="font-semibold">Nuxer's House</span>
                           <span className="">A casa do Nuxer</span>
                        </div>
                     </a>
                  </SidebarMenuButton>
               </SidebarMenuItem>
            </SidebarMenu>
         </SidebarHeader>
         <SidebarContent>
            <NavMain items={data.navMain} />
         </SidebarContent>
         <SidebarFooter>
            <NavUser />
         </SidebarFooter>
         <SidebarRail />
      </Sidebar>
   );
}
