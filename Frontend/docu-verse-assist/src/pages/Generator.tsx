import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { 
  FileEdit, 
  FileText, 
  Download, 
  Eye, 
  Sparkles,
  ArrowRight,
  File,
  FileCheck
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const documentTypes = [
  {
    id: "contract",
    title: "Contract",
    description: "Business contracts and agreements",
    icon: FileText,
    fields: ["Party Names", "Terms", "Duration", "Payment Terms"],
    color: "bg-primary"
  },
  {
    id: "invoice",
    title: "Invoice",
    description: "Professional invoices and bills",
    icon: File,
    fields: ["Client Details", "Items", "Amount", "Due Date"],
    color: "bg-success"
  },
  {
    id: "proposal",
    title: "Proposal",
    description: "Project proposals and quotes",
    icon: FileCheck,
    fields: ["Project Scope", "Timeline", "Budget", "Deliverables"],
    color: "bg-warning"
  },
  {
    id: "report",
    title: "Report",
    description: "Business reports and analysis",
    icon: FileText,
    fields: ["Title", "Summary", "Data", "Conclusions"],
    color: "bg-ai-accent"
  }
];

const Generator = () => {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDocument, setGeneratedDocument] = useState<string | null>(null);
  const { toast } = useToast();

  const selectedTemplate = documentTypes.find(type => type.id === selectedType);

  const handleGenerate = async () => {
    if (!selectedTemplate || Object.keys(formData).length === 0) return;

    setIsGenerating(true);
    
    // Simulate document generation
    setTimeout(() => {
      setGeneratedDocument(`Generated ${selectedTemplate.title} document based on your inputs.`);
      setIsGenerating(false);
      toast({
        title: "Document Generated!",
        description: `Your ${selectedTemplate.title} has been created successfully.`,
      });
    }, 2000);
  };

  const handleFieldChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (selectedType && selectedTemplate) {
    return (
      <AppLayout>
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Generate {selectedTemplate.title}
              </h1>
              <p className="text-muted-foreground">
                Fill in the details and let AI create your document
              </p>
            </div>
            <Button 
              variant="outline" 
              onClick={() => {
                setSelectedType(null);
                setFormData({});
                setGeneratedDocument(null);
              }}
            >
              Back to Templates
            </Button>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Form */}
            <Card className="bg-gradient-card border-border/50 shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <selectedTemplate.icon className="w-5 h-5 text-primary" />
                  Document Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {selectedTemplate.fields.map((field) => (
                  <div key={field} className="space-y-2">
                    <Label htmlFor={field}>{field}</Label>
                    {field.toLowerCase().includes("description") || field.toLowerCase().includes("summary") ? (
                      <Textarea
                        id={field}
                        placeholder={`Enter ${field.toLowerCase()}...`}
                        value={formData[field] || ""}
                        onChange={(e) => handleFieldChange(field, e.target.value)}
                        className="min-h-[100px]"
                      />
                    ) : (
                      <Input
                        id={field}
                        placeholder={`Enter ${field.toLowerCase()}...`}
                        value={formData[field] || ""}
                        onChange={(e) => handleFieldChange(field, e.target.value)}
                      />
                    )}
                  </div>
                ))}

                <Button 
                  onClick={handleGenerate}
                  disabled={isGenerating || Object.keys(formData).length === 0}
                  className="w-full mt-6"
                >
                  {isGenerating ? (
                    <>
                      <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <FileEdit className="w-4 h-4 mr-2" />
                      Generate Document
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Preview */}
            <Card className="bg-gradient-card border-border/50 shadow-soft">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="w-5 h-5 text-ai-accent" />
                  Live Preview
                </CardTitle>
              </CardHeader>
              <CardContent>
                {generatedDocument ? (
                  <div className="space-y-4">
                    <div className="p-4 bg-background/50 rounded-lg border border-border/50">
                      <p className="text-sm text-muted-foreground mb-2">Generated Content:</p>
                      <p className="text-foreground">{generatedDocument}</p>
                    </div>
                    
                    <div className="flex gap-2">
                      <Button size="sm" className="flex-1">
                        <Download className="w-4 h-4 mr-2" />
                        Download PDF
                      </Button>
                      <Button variant="outline" size="sm" className="flex-1">
                        <Eye className="w-4 h-4 mr-2" />
                        Full Preview
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <FileEdit className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">
                      Fill in the form to see live preview
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Document Generator
          </h1>
          <p className="text-muted-foreground">
            Choose a template and let AI generate professional documents for you
          </p>
        </div>

        {/* Template Selection */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {documentTypes.map((type) => (
            <Card 
              key={type.id}
              className="bg-gradient-card border-border/50 shadow-soft hover:shadow-elegant cursor-pointer transition-all duration-300 group"
              onClick={() => setSelectedType(type.id)}
            >
              <CardContent className="p-6">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className={`w-16 h-16 rounded-2xl ${type.color} flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
                    <type.icon className="w-8 h-8 text-white" />
                  </div>
                  
                  <div>
                    <h3 className="font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                      {type.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      {type.description}
                    </p>
                  </div>

                  <div className="w-full">
                    <p className="text-xs text-muted-foreground mb-2">Includes:</p>
                    <div className="flex flex-wrap gap-1">
                      {type.fields.slice(0, 2).map((field) => (
                        <Badge key={field} variant="secondary" className="text-xs">
                          {field}
                        </Badge>
                      ))}
                      {type.fields.length > 2 && (
                        <Badge variant="secondary" className="text-xs">
                          +{type.fields.length - 2} more
                        </Badge>
                      )}
                    </div>
                  </div>

                  <Button variant="outline" size="sm" className="w-full group-hover:bg-primary group-hover:text-primary-foreground">
                    Create Document
                    <ArrowRight className="w-3 h-3 ml-2 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* AI Features */}
        <Card className="bg-gradient-card border-border/50 shadow-soft">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Sparkles className="w-6 h-6 text-ai-accent" />
              <h3 className="text-lg font-semibold text-foreground">AI-Powered Features</h3>
            </div>
            
            <div className="grid gap-4 md:grid-cols-3">
              <div className="text-center">
                <div className="w-12 h-12 rounded-lg bg-gradient-ai flex items-center justify-center mx-auto mb-2">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-medium text-foreground mb-1">Smart Content</h4>
                <p className="text-sm text-muted-foreground">AI generates contextually relevant content</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 rounded-lg bg-gradient-ai flex items-center justify-center mx-auto mb-2">
                  <FileCheck className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-medium text-foreground mb-1">Auto Formatting</h4>
                <p className="text-sm text-muted-foreground">Professional layouts and styling</p>
              </div>
              
              <div className="text-center">
                <div className="w-12 h-12 rounded-lg bg-gradient-ai flex items-center justify-center mx-auto mb-2">
                  <Eye className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-medium text-foreground mb-1">Live Preview</h4>
                <p className="text-sm text-muted-foreground">See changes in real-time</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  );
};

export default Generator;