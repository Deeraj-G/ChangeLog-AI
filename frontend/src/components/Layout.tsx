import Link from 'next/link';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 dark:bg-gray-950 dark:border-gray-800">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            ChangeLog-AI
          </Link>
          <nav className="space-x-6">
            <Link href="/" className="hover:text-blue-600 dark:hover:text-blue-400">
              Home
            </Link>
            <Link href="/generate" className="hover:text-blue-600 dark:hover:text-blue-400">
              Generate
            </Link>
            <Link href="/changelogs" className="hover:text-blue-600 dark:hover:text-blue-400">
              Changelogs
            </Link>
          </nav>
        </div>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-white border-t border-gray-200 dark:bg-gray-950 dark:border-gray-800">
        <div className="container mx-auto px-4 py-6 text-center text-gray-500 dark:text-gray-400">
          <p>© {new Date().getFullYear()} ChangeLog-AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
} 