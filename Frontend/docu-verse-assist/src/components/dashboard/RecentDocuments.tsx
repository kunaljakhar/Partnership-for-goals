import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  FileText, 
  File, 
  FileImage, 
  MoreHorizontal,
  Eye,
  Download
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const documents = [
  {
    id: 1,
    name: "Sales Contract - Q4 2024",
    type: "Contract",
    status: "Processed",
    aiScore: 98,
    date: "2 hours ago",
    icon: FileText,
    size: "2.4 MB"
  },
  {
    id: 2,
    name: "Invoice Template",
    type: "Template",
    status: "Generated",
    aiScore: 95,
    date: "4 hours ago",
    icon: File,
    size: "1.2 MB"
  },
  {
    id: 3,
    name: "Legal Document Scan",
    type: "Scan",
    status: "Analyzing",
    aiScore: null,
    date: "1 day ago",
    icon: FileImage,
    size: "5.8 MB"
  },
  {
    id: 4,
    name: "Partnership Agreement",
    type: "Agreement",
    status: "Reviewed",
    aiScore: 92,
    date: "2 days ago",
    icon: FileText,
    size: "3.1 MB"
  }
];

const getStatusColor = (status: string) => {
  switch (status) {
    case "Processed":
    case "Generated":
    case "Reviewed":
      return "bg-success/10 text-success border-success/20";
    case "Analyzing":
      return "bg-warning/10 text-warning border-warning/20";
    default:
      return "bg-muted text-muted-foreground";
  }
};

export function RecentDocuments() {
  return (
    <Card className="bg-gradient-card border-border/50 shadow-soft">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          Recent Documents
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {documents.map((doc) => (
            <div 
              key={doc.id} 
              className="flex items-center justify-between p-3 rounded-lg bg-background/50 border border-border/50 hover:bg-accent/50 transition-colors"
            >
              <div className="flex items-center gap-3 flex-1">
                <div className="w-10 h-10 rounded-lg bg-gradient-ai flex items-center justify-center">
                  <doc.icon className="w-5 h-5 text-white" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-foreground truncate">{doc.name}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-sm text-muted-foreground">{doc.type}</span>
                    <span className="text-sm text-muted-foreground">•</span>
                    <span className="text-sm text-muted-foreground">{doc.size}</span>
                    <span className="text-sm text-muted-foreground">•</span>
                    <span className="text-sm text-muted-foreground">{doc.date}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Badge className={getStatusColor(doc.status)}>
                  {doc.status}
                </Badge>
                
                {doc.aiScore && (
                  <div className="flex items-center gap-1">
                    <span className="text-sm text-muted-foreground">AI:</span>
                    <span className="text-sm font-medium text-ai-accent">{doc.aiScore}%</span>
                  </div>
                )}

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm" className="w-8 h-8 p-0">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <Eye className="w-4 h-4 mr-2" />
                      View
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}