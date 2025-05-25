import ReactMarkdown from 'react-markdown';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ChangelogDisplayProps {
  content: string;
  title: string;
}

export default function ChangelogDisplay({ content, title }: ChangelogDisplayProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="prose prose-sm md:prose-base lg:prose-lg dark:prose-invert max-w-none">
        <ReactMarkdown>{content}</ReactMarkdown>
      </CardContent>
    </Card>
  );
} 