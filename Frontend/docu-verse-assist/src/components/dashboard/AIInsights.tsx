import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Brain, 
  AlertTriangle, 
  CheckCircle, 
  TrendingUp, 
  ArrowRight
} from "lucide-react";

const insights = [
  {
    id: 1,
    type: "recommendation",
    title: "Optimize Contract Processing",
    description: "AI detected 3 similar contracts that could use a template to save 2.5 hours",
    icon: TrendingUp,
    priority: "medium",
    action: "Create Template"
  },
  {
    id: 2,
    type: "alert",
    title: "Missing Clause Detected",
    description: "Recent partnership agreement is missing standard liability clause",
    icon: AlertTriangle,
    priority: "high",
    action: "Review Document"
  },
  {
    id: 3,
    type: "success",
    title: "Workflow Completed",
    description: "All Q4 invoices successfully processed and validated",
    icon: CheckCircle,
    priority: "low",
    action: "View Results"
  }
];

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case "high":
      return "bg-destructive/10 text-destructive border-destructive/20";
    case "medium":
      return "bg-warning/10 text-warning border-warning/20";
    case "low":
      return "bg-success/10 text-success border-success/20";
    default:
      return "bg-muted text-muted-foreground";
  }
};

const getIconColor = (type: string) => {
  switch (type) {
    case "alert":
      return "text-destructive";
    case "recommendation":
      return "text-warning";
    case "success":
      return "text-success";
    default:
      return "text-muted-foreground";
  }
};

export function AIInsights() {
  return (
    <Card className="bg-gradient-card border-border/50 shadow-soft">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-ai-accent" />
          AI Insights
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {insights.map((insight) => (
            <div 
              key={insight.id} 
              className="p-4 rounded-lg bg-background/50 border border-border/50 hover:bg-accent/50 transition-colors"
            >
              <div className="flex items-start gap-3">
                <div className={`w-8 h-8 rounded-lg bg-gradient-ai flex items-center justify-center`}>
                  <insight.icon className={`w-4 h-4 text-white`} />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-medium text-foreground">{insight.title}</h4>
                    <Badge className={getPriorityColor(insight.priority)}>
                      {insight.priority}
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-muted-foreground mb-3">
                    {insight.description}
                  </p>
                  
                  <Button variant="outline" size="sm" className="group">
                    {insight.action}
                    <ArrowRight className="w-3 h-3 ml-2 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}