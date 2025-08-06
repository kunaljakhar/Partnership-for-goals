import { AppLayout } from "@/components/layout/AppLayout";
import { FileUpload } from "@/components/upload/FileUpload";

const Documents = () => {
  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Documents
          </h1>
          <p className="text-muted-foreground">
            Upload and manage your documents with AI-powered processing
          </p>
        </div>

        <FileUpload />
      </div>
    </AppLayout>
  );
};

export default Documents;