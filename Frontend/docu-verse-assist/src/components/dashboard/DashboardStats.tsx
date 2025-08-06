import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  FileText, 
  Clock, 
  TrendingUp, 
  Zap 
} from "lucide-react";

const stats = [
  {
    title: "Documents Processed",
    value: "1,247",
    change: "+12%",
    changeType: "positive" as const,
    icon: FileText,
    description: "This month"
  },
  {
    title: "Time Saved",
    value: "142h",
    change: "+8%",
    changeType: "positive" as const,
    icon: Clock,
    description: "AI automation"
  },
  {
    title: "Accuracy Rate",
    value: "98.5%",
    change: "+2.1%",
    changeType: "positive" as const,
    icon: TrendingUp,
    description: "AI processing"
  },
  {
    title: "Active Workflows",
    value: "23",
    change: "+5",
    changeType: "positive" as const,
    icon: Zap,
    description: "Running now"
  }
];

export function DashboardStats() {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title} className="bg-gradient-card border-border/50 shadow-soft hover:shadow-elegant transition-all duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {stat.title}
            </CardTitle>
            <div className="w-8 h-8 rounded-lg bg-gradient-ai flex items-center justify-center">
              <stat.icon className="w-4 h-4 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{stat.value}</div>
            <div className="flex items-center gap-2 mt-1">
              <Badge 
                variant="secondary" 
                className={`text-xs ${
                  stat.changeType === 'positive' 
                    ? 'bg-success/10 text-success' 
                    : 'bg-destructive/10 text-destructive'
                }`}
              >
                {stat.change}
              </Badge>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}