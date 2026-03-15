"use client";

import { useCallback, useState } from 'react';
import { useDropzone, FileRejection } from 'react-dropzone';
import { UploadCloud, FileText, CheckCircle, AlertCircle } from 'lucide-react';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

export default function UploadZone({ onFileSelect, isLoading = false }: UploadZoneProps) {
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: FileRejection[]) => {
    setError(null);

    if (fileRejections.length > 0) {
      setError(fileRejections[0].errors[0].message);
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    maxSize: 20 * 1024 * 1024, // 20MB
    disabled: isLoading
  });

  return (
    <div className="w-full max-w-2xl mx-auto mt-8">
      <div 
        {...getRootProps()} 
        className={`glass-card p-10 rounded-2xl border-2 border-dashed text-center cursor-pointer transition-all duration-300
          ${isDragActive ? 'drop-zone-active scale-[1.02]' : 'border-white/10 hover:border-white/30 hover:bg-white/[0.02]'}
          ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
          ${selectedFile && !error ? 'border-teal-500/50 bg-teal-500/5' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center justify-center space-y-4">
          {selectedFile && !error ? (
            <div className="p-4 bg-teal-500/10 rounded-full text-teal-400">
              <CheckCircle size={48} className="animate-in zoom-in duration-300" />
            </div>
          ) : error ? (
            <div className="p-4 bg-red-500/10 rounded-full text-red-400">
              <AlertCircle size={48} />
            </div>
          ) : (
            <div className={`p-4 rounded-full transition-colors duration-300 ${isDragActive ? 'bg-purple-500/20 text-purple-400' : 'bg-white/5 text-gray-400'}`}>
              <UploadCloud size={48} />
            </div>
          )}

          <div className="space-y-2">
            {selectedFile && !error ? (
              <>
                <h3 className="text-xl font-semibold text-white flex items-center justify-center gap-2">
                  <FileText size={20} className="text-teal-400" />
                  {selectedFile.name}
                </h3>
                <p className="text-gray-400 text-sm">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
                <p className="text-teal-400/80 text-sm mt-4 font-medium">Ready to analyze</p>
              </>
            ) : (
              <>
                <h3 className="text-xl font-semibold text-white">
                  {isDragActive ? 'Drop your paper here' : 'Select a research paper'}
                </h3>
                <p className="text-gray-400 text-sm max-w-sm mx-auto">
                  Drag and drop a PDF file here, or click to browse your computer.
                </p>
                <div className="flex items-center justify-center gap-4 text-xs font-medium text-gray-500 mt-6 pt-4 border-t border-white/5">
                  <span>PDF format only</span>
                  <span className="w-1 h-1 rounded-full bg-gray-600"></span>
                  <span>Max size: 20MB</span>
                </div>
              </>
            )}
          </div>
          
          {error && (
            <p className="text-red-400 text-sm font-medium mt-2">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
}
