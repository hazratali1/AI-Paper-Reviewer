import { Users, ExternalLink, Activity } from 'lucide-react';

interface RecommendedPaper {
  title: string;
  authors: string[];
  year?: string | number;
  summary: string;
  relevance: string;
  url?: string;
}

interface RecommendedPapersProps {
  recommendations: {
    recommended_papers: RecommendedPaper[];
  };
}

export default function RecommendedPapers({ recommendations }: RecommendedPapersProps) {
  const papers = recommendations.recommended_papers || [];

  if (papers.length === 0) {
    return (
      <div className="glass-card p-8 rounded-2xl text-center text-gray-400">
        No relevant papers could be found for this topic.
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in-up">
      <div className="glass-card p-6 md:p-8 rounded-2xl glow-blue">
        <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-3">
          <Activity className="text-blue-400" />
          Recommended Reading
        </h2>
        <p className="text-gray-400 text-lg">
          The top {papers.length} most relevant related papers based on the uploaded document&apos;s contributions and methodology.
        </p>
      </div>

      <div className="space-y-4">
        {papers.map((paper, idx) => (
          <div key={idx} className="glass-card p-6 rounded-2xl glass-card-hover group border-l-[3px] border-l-purple-500/50 hover:border-l-purple-400 transition-all">
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
              <div>
                <h3 className="text-xl font-bold text-white group-hover:text-blue-300 transition-colors">
                  {paper.title}
                </h3>
                
                <div className="flex flex-wrap items-center gap-2 mt-2 text-sm text-gray-400 font-medium">
                  {paper.year && (
                    <span className="bg-white/10 px-2 py-0.5 rounded text-white mix-blend-screen">
                      {paper.year}
                    </span>
                  )}
                  {paper.authors?.length > 0 && (
                    <div className="flex items-center gap-1.5">
                      <Users size={14} className="text-purple-400" />
                      <span>{paper.authors.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
              
              {paper.url && (
                <a 
                  href={paper.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0 inline-flex items-center gap-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 px-4 py-2 rounded-xl text-sm font-bold transition-colors"
                >
                  View Paper <ExternalLink size={16} />
                </a>
              )}
            </div>

            <div className="space-y-3">
              <p className="text-gray-300 leading-relaxed text-sm">
                <span className="font-semibold text-gray-500 uppercase tracking-wider text-xs mr-2">Abstract</span>
                {paper.summary || 'No abstract available.'}
              </p>
              
              <div className="bg-amber-500/5 border border-amber-500/10 rounded-xl p-3 text-sm">
                <p className="text-amber-200/80 leading-relaxed">
                  <span className="font-bold text-amber-500/60 uppercase tracking-wider text-xs mr-2">Why it&apos;s relevant</span>
                  {paper.relevance}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
