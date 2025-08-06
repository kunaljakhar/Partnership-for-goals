import { AppLayout } from "@/components/layout/AppLayout";
import { DashboardStats } from "@/components/dashboard/DashboardStats";
import { RecentDocuments } from "@/components/dashboard/RecentDocuments";
import { AIInsights } from "@/components/dashboard/AIInsights";
import { QuickActions } from "@/components/dashboard/QuickActions";

const Index = () => {
  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Welcome back, Kunal 👋
          </h1>
          <p className="text-muted-foreground">
            Here's what's happening with your AI workflow today
          </p>
        </div>

        {/* Stats */}
        <DashboardStats />

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6">
            <RecentDocuments />
            <AIInsights />
          </div>
          
          <div className="space-y-6">
            <QuickActions />
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default Index;
