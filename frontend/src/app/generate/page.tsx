'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import ChangelogForm from '@/components/ChangelogForm';
import ChangelogDisplay from '@/components/ChangelogDisplay';

export default function GeneratePage() {
  const [generatedChangelog, setGeneratedChangelog] = useState<string | null>(null);
  const [title, setTitle] = useState<string>('');

  const handleSuccess = (content: string) => {
    setGeneratedChangelog(content);
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Generate Changelog</h1>
        
        <div className="space-y-8">
          {!generatedChangelog ? (
            <div className="flex justify-center">
              <ChangelogForm 
                onSuccess={(content) => {
                  // Extract title from form
                  const formTitle = document.querySelector('input[name="title"]') as HTMLInputElement;
                  if (formTitle) {
                    setTitle(formTitle.value);
                  }
                  handleSuccess(content);
                }} 
              />
            </div>
          ) : (
            <div className="space-y-6">
              <ChangelogDisplay content={generatedChangelog} title={title} />
              <div className="flex justify-center">
                <button
                  onClick={() => setGeneratedChangelog(null)}
                  className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 rounded"
                >
                  Generate Another
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
} 