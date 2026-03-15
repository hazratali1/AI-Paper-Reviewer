import { LayoutTemplate, Lightbulb, Target, FlaskConical, Database, AlertTriangle } from 'lucide-react';

interface PaperSummaryProps {
  title: string;
  analysis: {
    summary: string;
    research_problem: string;
    detailed_methodology: string;
    contributions: string[];
    results: string;
    datasets?: string;
    limitations?: string[];
  };
}

export default function PaperSummary({ title, analysis }: PaperSummaryProps) {
  return (
    <div className="space-y-6 fade-in-up">
      {/* Header section */}
      <div className="glass-card p-6 md:p-8 rounded-2xl glow-blue">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-blue-500/10 rounded-xl shrink-0 mt-1">
            <LayoutTemplate size={24} className="text-blue-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-4 leading-tight">{title}</h2>
            <p className="text-gray-300 leading-relaxed text-lg">{analysis.summary}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Research Problem */}
        <div className="glass-card p-6 rounded-2xl glass-card-hover">
          <div className="flex items-center gap-3 mb-4">
            <Target size={20} className="text-amber-400" />
            <h3 className="text-lg font-semibold text-white">Research Problem</h3>
          </div>
          <p className="text-gray-400 leading-relaxed">{analysis.research_problem || 'Not explicitly stated.'}</p>
        </div>

        {/* Methodology */}
        <div className="glass-card p-6 rounded-2xl md:col-span-2 glass-card-hover border-t-teal-500/30 border-t-2">
          <div className="flex items-center gap-3 mb-4">
            <FlaskConical size={20} className="text-teal-400" />
            <h3 className="text-lg font-semibold text-white">Detailed Methodology</h3>
          </div>
          <div className="text-gray-400 leading-relaxed space-y-3">
            {analysis.detailed_methodology ? (
              analysis.detailed_methodology.split('\n\n').map((para, i) => (
                <p key={i}>{para}</p>
              ))
            ) : 'Not explicitly stated.'}
          </div>
        </div>
      </div>

      {/* Key Contributions */}
      <div className="glass-card p-6 md:p-8 rounded-2xl glass-card-hover border-t-purple-500/30 border-t-2">
        <div className="flex items-center gap-3 mb-6">
          <Lightbulb size={24} className="text-purple-400" />
          <h3 className="text-xl font-bold text-white">Key Contributions</h3>
        </div>
        <ul className="space-y-4">
          {analysis.contributions?.length > 0 ? (
            analysis.contributions.map((contribution, idx) => (
              <li key={idx} className="flex gap-4">
                <span className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-sm">
                  {idx + 1}
                </span>
                <p className="text-gray-300 leading-relaxed pt-1">{contribution}</p>
              </li>
            ))
          ) : (
            <p className="text-gray-400">No explicit contributions extracted.</p>
          )}
        </ul>
      </div>

      {/* Limitations */}
      <div className="glass-card p-6 rounded-2xl glass-card-hover border-t-red-500/30 border-t-2">
        <div className="flex items-center gap-3 mb-6">
          <AlertTriangle size={24} className="text-red-400" />
          <h3 className="text-xl font-bold text-white">Limitations</h3>
        </div>
        <ul className="space-y-3">
          {analysis.limitations && analysis.limitations.length > 0 ? (
            analysis.limitations.map((lim, idx) => (
              <li key={idx} className="flex gap-3">
                <span className="text-red-400 shrink-0 mt-1">•</span>
                <p className="text-gray-300 leading-relaxed text-sm">{lim}</p>
              </li>
            ))
          ) : (
            <p className="text-gray-400">No explicit limitations extracted.</p>
          )}
        </ul>
      </div>

      {/* Meta attributes */}
      {analysis.datasets && analysis.datasets !== 'None' && (
        <div className="flex flex-wrap gap-4">
          <div className="glass-card px-4 py-3 rounded-xl flex items-center gap-3 text-sm text-gray-400">
            <Database size={16} className="text-blue-400" />
            <span className="font-medium text-white">Datasets:</span>
            <span className="truncate max-w-xs">{analysis.datasets}</span>
          </div>
        </div>
      )}
    </div>
  );
}
