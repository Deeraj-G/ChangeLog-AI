import Link from 'next/link';
import Layout from '@/components/Layout';
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          Welcome to ChangeLog-AI
        </h1>
        <p className="text-xl mb-8 max-w-2xl">
          Generate beautiful changelogs from your git repositories using AI.
          Save time and keep your users informed about the latest changes.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Button asChild size="lg">
            <Link href="/generate">
              Generate Changelog
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/changelogs">
              View Changelogs
            </Link>
          </Button>
        </div>
        
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-3">Easy to Use</h2>
            <p>
              Simply provide your repository URL and commit range, and let AI do the rest.
              No more manual changelog writing!
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-3">AI-Powered</h2>
            <p>
              Our AI analyzes your commits and generates human-readable changelogs
              that focus on what matters to your users.
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-3">Beautiful Format</h2>
            <p>
              Changelogs are formatted in Markdown and categorized by type of change,
              making them easy to read and understand.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
