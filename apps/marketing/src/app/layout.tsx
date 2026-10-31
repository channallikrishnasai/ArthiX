import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ArthiX — AI-native ERP',
  description:
    'ArthiX connects your finance, HR, CRM, projects and inventory — with an AI assistant that understands your business.',
  openGraph: {
    title: 'ArthiX — AI-native ERP',
    description:
      'The AI-native ERP that works the way you think. Finance, HR, CRM, inventory and more in one platform.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white font-sans antialiased">{children}</body>
    </html>
  );
}
