import React from 'react';
import { NavLink } from 'react-router-dom';
import { ChartBarIcon, CloudArrowUpIcon, Cog6ToothIcon, CpuChipIcon, DocumentTextIcon, UserGroupIcon } from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: ChartBarIcon },
  { name: 'Simulação', href: '/simulation', icon: CpuChipIcon },
  { name: 'Agentes', href: '/agents', icon: UserGroupIcon },
  { name: 'Relatórios', href: '/reports', icon: DocumentTextIcon },
  { name: 'Upload', href: '/upload', icon: CloudArrowUpIcon },
  { name: 'Configurações', href: '/settings', icon: Cog6ToothIcon },
];

export default function Sidebar() {
  return <aside className="hidden lg:block w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700"><nav className="flex flex-col gap-1 p-4">{navigation.map((item)=><NavLink key={item.name} to={item.href} className={({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${isActive ? 'bg-primary-50 text-primary-600 dark:bg-primary-900/50 dark:text-primary-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700'}`}><item.icon className="h-5 w-5" />{item.name}</NavLink>)}</nav></aside>;
}
