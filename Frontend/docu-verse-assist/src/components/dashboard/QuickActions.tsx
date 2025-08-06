import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  Upload, 
  MessageSquare, 
  FileEdit, 
  Zap, 
  ArrowRight 
} from "lucide-react";

const actions = [
  {
    id: 1,
    title: "Upload Document",
    description: "Drag & drop or browse files",
    icon: Upload,
    color: "bg-primary",
    route: "/documents"
  },
  {
    id: 2,
    title: "Chat with AI",
    description: "Get instant help & analysis",
    icon: MessageSquare,
    color: "bg-ai-accent",
    route: "/chat"
  },
  {
    id: 3,
    title: "Generate Document",
    description: "Create from templates",
    icon: FileEdit,
    color: "bg-success",
    route: "/generator"
  },
  {
    id: 4,
    title: "Quick Templates",
    description: "Ready-to-use formats",
    icon: Zap,
    color: "bg-warning",
    route: "/templates"
  }
];

export function QuickActions() {
  return (
    <Card className="bg-gradient-card border-border/50 shadow-soft">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-primary" />
          Quick Actions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-3 sm:grid-cols-2">
          {actions.map((action) => (
            <Button
              key={action.id}
              variant="outline"
              className="h-auto p-4 flex flex-col items-start gap-3 group hover:shadow-soft transition-all duration-200"
              asChild
            >
              <a href={action.route}>
                <div className="flex items-center gap-3 w-full">
                  <div className={`w-10 h-10 rounded-lg ${action.color} flex items-center justify-center`}>
                    <action.icon className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1 text-left">
                    <h4 className="font-medium text-foreground group-hover:text-primary transition-colors">
                      {action.title}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {action.description}
                    </p>
                  </div>
                  <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
                </div>
              </a>
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}