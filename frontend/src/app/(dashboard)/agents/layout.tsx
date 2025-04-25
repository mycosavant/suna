import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Agent Conversation | Kortix Ptah",
  description: "Interactive agent conversation powered by Kortix Ptah",
  openGraph: {
    title: "Agent Conversation | Kortix Ptah",
    description: "Interactive agent conversation powered by Kortix Ptah",
    type: "website",
  },
};

export default function AgentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
} 