import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { 
  Search, 
  Filter, 
  FileText, 
  File, 
  FileImage, 
  MoreHorizontal,
  Eye,
  Download,
  Edit,
  Trash2,
  Calendar,
  SortAsc
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const documents = [
  {
    id: 1,
    name: "Sales Contract - Q4 2024",
    type: "Contract",
    status: "Processed",
    aiScore: 98,
    createdAt: "2024-12-01",
    modifiedAt: "2 hours ago",
    icon: FileText,
    size: "2.4 MB",
    tags: ["Legal", "Q4", "Sales"]
  },
  {
    id: 2,
    name: "Invoice Template v2",
    type: "Template",
    status: "Generated",
    aiScore: 95,
    createdAt: "2024-11-28",
    modifiedAt: "4 hours ago",
    icon: File,
    size: "1.2 MB",
    tags: ["Invoice", "Template"]
  },
  {
    id: 3,
    name: "Legal Document Scan",
    type: "Scan",
    status: "Analyzing",
    aiScore: null,
    createdAt: "2024-11-27",
    modifiedAt: "1 day ago",
    icon: FileImage,
    size: "5.8 MB",
    tags: ["Legal", "Scan"]
  },
  {
    id: 4,
    name: "Partnership Agreement - TechCorp",
    type: "Agreement",
    status: "Reviewed",
    aiScore: 92,
    createdAt: "2024-11-25",
    modifiedAt: "2 days ago",
    icon: FileText,
    size: "3.1 MB",
    tags: ["Partnership", "Legal"]
  },
  {
    id: 5,
    name: "Marketing Proposal - Brand Campaign",
    type: "Proposal",
    status: "Draft",
    aiScore: 88,
    createdAt: "2024-11-24",
    modifiedAt: "3 days ago",
    icon: FileText,
    size: "1.8 MB",
    tags: ["Marketing", "Proposal"]
  },
  {
    id: 6,
    name: "Financial Report Q3",
    type: "Report",
    status: "Processed",
    aiScore: 96,
    createdAt: "2024-11-20",
    modifiedAt: "1 week ago",
    icon: File,
    size: "4.2 MB",
    tags: ["Finance", "Q3", "Report"]
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
    case "Draft":
      return "bg-muted text-muted-foreground border-border";
    default:
      return "bg-muted text-muted-foreground";
  }
};

const MyDocuments = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [sortBy, setSortBy] = useState("modified");

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesFilter = selectedFilter === "all" || doc.type.toLowerCase() === selectedFilter;
    return matchesSearch && matchesFilter;
  });

  return (
    <AppLayout>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            My Documents
          </h1>
          <p className="text-muted-foreground">
            Manage and organize all your AI-processed documents
          </p>
        </div>

        {/* Filters and Search */}
        <Card className="bg-gradient-card border-border/50 shadow-soft">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search documents, tags..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              <div className="flex gap-2">
                <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                  <SelectTrigger className="w-[150px]">
                    <Filter className="w-4 h-4 mr-2" />
                    <SelectValue placeholder="Filter by type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="contract">Contracts</SelectItem>
                    <SelectItem value="template">Templates</SelectItem>
                    <SelectItem value="scan">Scans</SelectItem>
                    <SelectItem value="agreement">Agreements</SelectItem>
                    <SelectItem value="proposal">Proposals</SelectItem>
                    <SelectItem value="report">Reports</SelectItem>
                  </SelectContent>
                </Select>

                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-[150px]">
                    <SortAsc className="w-4 h-4 mr-2" />
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="modified">Last Modified</SelectItem>
                    <SelectItem value="created">Date Created</SelectItem>
                    <SelectItem value="name">Name</SelectItem>
                    <SelectItem value="size">File Size</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Documents Grid */}
        <div className="grid gap-4">
          {filteredDocuments.map((doc) => (
            <Card 
              key={doc.id} 
              className="bg-gradient-card border-border/50 shadow-soft hover:shadow-elegant transition-all duration-300 group"
            >
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1 min-w-0">
                    <div className="w-12 h-12 rounded-lg bg-gradient-ai flex items-center justify-center flex-shrink-0">
                      <doc.icon className="w-6 h-6 text-white" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-foreground truncate group-hover:text-primary transition-colors">
                          {doc.name}
                        </h3>
                        <Badge className={getStatusColor(doc.status)}>
                          {doc.status}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm text-muted-foreground mb-2">
                        <span>{doc.type}</span>
                        <span>•</span>
                        <span>{doc.size}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {doc.modifiedAt}
                        </span>
                        {doc.aiScore && (
                          <>
                            <span>•</span>
                            <span className="flex items-center gap-1">
                              <span className="text-ai-accent font-medium">AI: {doc.aiScore}%</span>
                            </span>
                          </>
                        )}
                      </div>

                      <div className="flex flex-wrap gap-1">
                        {doc.tags.map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 flex-shrink-0">
                    <Button variant="ghost" size="sm">
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Download className="w-4 h-4" />
                    </Button>

                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="w-8 h-8 p-0">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>
                          <Edit className="w-4 h-4 mr-2" />
                          Edit
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </DropdownMenuItem>
                        <DropdownMenuItem className="text-destructive">
                          <Trash2 className="w-4 h-4 mr-2" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredDocuments.length === 0 && (
          <Card className="bg-gradient-card border-border/50 shadow-soft">
            <CardContent className="p-12 text-center">
              <FileText className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">No documents found</h3>
              <p className="text-muted-foreground mb-4">
                {searchQuery || selectedFilter !== "all" 
                  ? "Try adjusting your search or filters"
                  : "Upload your first document to get started"
                }
              </p>
              <Button>
                Upload Documents
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </AppLayout>
  );
};

export default MyDocuments;