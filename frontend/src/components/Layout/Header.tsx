import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8">
        <div className="flex lg:flex-1">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl">🧠</span><span className="text-xl font-bold text-primary-600">EvoBrain</span>
          </Link>
        </div>
        <div className="flex lg:hidden">
          <button type="button" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-gray-700 dark:text-gray-200">
            {mobileMenuOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
          </button>
        </div>
        <div className="hidden lg:flex lg:gap-x-8">
          {['dashboard','simulation','agents','reports','upload'].map((item) => <Link key={item} to={`/${item}`} className="text-gray-700 hover:text-primary-600 dark:text-gray-200">{item[0].toUpperCase()+item.slice(1)}</Link>)}
        </div>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end"><div className="flex items-center gap-2"><div className="h-2 w-2 rounded-full bg-green-500"></div><span className="text-sm text-gray-500">Online</span></div></div>
      </nav>
      {mobileMenuOpen && <div className="lg:hidden"><div className="space-y-1 px-4 pb-3 pt-2">{['dashboard','simulation','agents','reports','upload'].map((item)=><Link key={item} to={`/${item}`} className="block py-2 text-gray-700 dark:text-gray-200">{item[0].toUpperCase()+item.slice(1)}</Link>)}</div></div>}
    </header>
  );
}
