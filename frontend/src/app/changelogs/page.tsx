'use client';

import Layout from '@/components/Layout';
import ChangelogList from '@/components/ChangelogList';

export default function ChangelogsPage() {
  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">All Changelogs</h1>
        <ChangelogList />
      </div>
    </Layout>
  );
} 