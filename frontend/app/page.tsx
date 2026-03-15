"use client";

import { useState } from 'react';
import { uploadPaper, analyzePaper } from './lib/api';
import UploadZone from './components/UploadZone';
import AnalysisProgress from './components/AnalysisProgress';
import PaperSummary from './components/PaperSummary';
import ReviewCard from './components/ReviewCard';
import LiteratureReview from './components/LiteratureReview';
import NoveltyScore from './components/NoveltyScore';
import RecommendedPapers from './components/RecommendedPapers';
import FutureScope from './components/FutureScope';
import { Sparkles, FileText, BarChart2, BookOpen, Layers, Telescope } from 'lucide-react';

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [report, setReport] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('summary');
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    try {
      setError(null);
      setIsAnalyzing(true);
      
      // Step 1: Upload
      const uploadRes = await uploadPaper(file);
      const paperId = uploadRes.paper_id;

      // Step 2: Analyze
      const analyzeRes = await analyzePaper(paperId);
      setReport(analyzeRes);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'An error occurred during analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const tabs = [
    { id: 'summary', label: 'Summary', icon: FileText },
    { id: 'review', label: 'AI Review', icon: Layers },
    { id: 'literature', label: 'Literature Review', icon: BookOpen },
    { id: 'novelty', label: 'Novelty Score', icon: BarChart2 },
    { id: 'future', label: 'Future Scope', icon: Telescope },
    { id: 'recommendations', label: 'Related Papers', icon: Sparkles },
  ];

  return (
    <div className="min-h-screen hero-bg text-white pb-20">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 glass-card rounded-none border-x-0 border-t-0 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg">
            <Sparkles size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">AI Paper Reviewer</h1>
        </div>
        <div className="flex items-center gap-4 text-sm font-medium text-gray-400">
          <span className="hidden sm:inline-block">Powered by Groq & Llama-3</span>
          <div className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></div>
        </div>
      </header>

      <main className="pt-32 px-4 sm:px-6 max-w-7xl mx-auto">
        {!isAnalyzing && !report && (
          <div className="text-center max-w-3xl mx-auto space-y-6 fade-in-up">
            <h2 className="text-5xl sm:text-6xl font-black tracking-tight leading-tight">
              Analyze Research Papers <br className="hidden sm:block" />
              <span className="gradient-text">At Lightning Speed</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed max-w-2xl mx-auto">
              Upload any academic PDF. Our multi-agent AI will extract contributions, generate a peer review, synthesize literature, and assess novelty.
            </p>
            
            <UploadZone onFileSelect={handleFileSelect} isLoading={isAnalyzing} />
            
            {error && (
              <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl inline-block">
                {error}
              </div>
            )}
          </div>
        )}

        {isAnalyzing && (
          <AnalysisProgress />
        )}

        {report && !isAnalyzing && (
          <div className="space-y-8 fade-in-up">
            {/* Action Bar / Tabs */}
            <div className="glass-card p-2 rounded-2xl flex flex-wrap gap-2 justify-center sticky top-24 z-40 bg-black/40 backdrop-blur-xl">
              {tabs.map(tab => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 ${
                      isActive 
                        ? 'bg-white/10 text-white shadow-[inset_0_1px_rgba(255,255,255,0.1)]' 
                        : 'text-gray-400 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    <Icon size={16} className={isActive ? 'text-purple-400' : ''} />
                    {tab.label}
                  </button>
                );
              })}
              <button 
                onClick={() => {
                  setReport(null);
                  setActiveTab('summary');
                }}
                className="ml-auto flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
               >
                Upload Another
              </button>
            </div>

            <div className="pt-4">
              {activeTab === 'summary' && <PaperSummary title={report.title} analysis={report.analysis} />}
              {activeTab === 'review' && <ReviewCard review={report.review} />}
              {activeTab === 'literature' && <LiteratureReview literature={report.literature_review} />}
              {activeTab === 'novelty' && <NoveltyScore novelty={report.novelty} />}
              {activeTab === 'future' && <FutureScope futureScope={report.analysis?.future_scope} />}
              {activeTab === 'recommendations' && <RecommendedPapers recommendations={report.related_papers} />}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
