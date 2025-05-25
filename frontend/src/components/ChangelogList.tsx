import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Changelog, getChangelogs } from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function ChangelogList() {
  const [changelogs, setChangelogs] = useState<Changelog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChangelogs = async () => {
      try {
        const data = await getChangelogs();
        setChangelogs(data);
      } catch (err) {
        console.error('Error fetching changelogs:', err);
        setError('Failed to load changelogs');
      } finally {
        setIsLoading(false);
      }
    };

    fetchChangelogs();
  }, []);

  if (isLoading) {
    return <div className="text-center py-8">Loading changelogs...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-500">{error}</div>;
  }

  if (changelogs.length === 0) {
    return (
      <div className="text-center py-8">
        No changelogs found. <Link href="/generate" className="text-blue-500 hover:underline">Generate one</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Recent Changelogs</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {changelogs.map((changelog) => (
          <Link key={changelog.id} href={`/changelog/${changelog.id}`}>
            <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle>{changelog.title}</CardTitle>
                <CardDescription>
                  {new Date(changelog.created_at).toLocaleDateString()}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 truncate">
                  {changelog.repository_url}
                </p>
                {changelog.description && (
                  <p className="mt-2 line-clamp-2">{changelog.description}</p>
                )}
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
} 