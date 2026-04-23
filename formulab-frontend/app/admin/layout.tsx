import Sidebar from "@/components/layout/Sidebar";
export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return <div className="flex min-h-screen"><Sidebar /><main className="flex-1 ml-64"><div className="max-w-6xl mx-auto px-8 py-8">{children}</div></main></div>;
}
