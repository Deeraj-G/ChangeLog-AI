import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { generateChangelog, ChangelogGenerateRequest } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const formSchema = z.object({
  repository_url: z.string().url('Please enter a valid URL'),
  title: z.string().min(3, 'Title must be at least 3 characters'),
  from_commit: z.string().optional(),
  to_commit: z.string().optional(),
});

type FormValues = z.infer<typeof formSchema>;

interface ChangelogFormProps {
  onSuccess: (content: string) => void;
}

export default function ChangelogForm({ onSuccess }: ChangelogFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      repository_url: '',
      title: '',
      from_commit: '',
      to_commit: '',
    },
  });

  const onSubmit = async (data: FormValues) => {
    setIsLoading(true);
    setError(null);

    try {
      const request: ChangelogGenerateRequest = {
        repository_url: data.repository_url,
        title: data.title,
      };

      if (data.from_commit) {
        request.from_commit = data.from_commit;
      }

      if (data.to_commit) {
        request.to_commit = data.to_commit;
      }

      const content = await generateChangelog(request);
      onSuccess(content);
    } catch (err) {
      console.error('Error generating changelog:', err);
      setError('Failed to generate changelog. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Generate Changelog</CardTitle>
        <CardDescription>
          Enter your repository details to generate a changelog
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="repository_url"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Repository URL</FormLabel>
                  <FormControl>
                    <Input placeholder="https://github.com/username/repo.git" {...field} />
                  </FormControl>
                  <FormDescription>
                    The URL of the git repository
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input placeholder="Release v1.0.0" {...field} />
                  </FormControl>
                  <FormDescription>
                    A title for your changelog
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="from_commit"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>From Commit (Optional)</FormLabel>
                    <FormControl>
                      <Input placeholder="e.g., abc123" {...field} />
                    </FormControl>
                    <FormDescription>
                      Starting commit hash
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="to_commit"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>To Commit (Optional)</FormLabel>
                    <FormControl>
                      <Input placeholder="e.g., def456" {...field} />
                    </FormControl>
                    <FormDescription>
                      Ending commit hash
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            {error && (
              <div className="text-red-500 text-sm">{error}</div>
            )}
            <Button type="submit" disabled={isLoading} className="w-full">
              {isLoading ? 'Generating...' : 'Generate Changelog'}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
} 