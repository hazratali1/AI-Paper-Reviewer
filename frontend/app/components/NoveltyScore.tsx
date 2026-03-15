import { Compass, Zap, Scale, FileText } from 'lucide-react';
import { useEffect, useState } from 'react';

interface NoveltyScoreProps {
  novelty: {
    novelty_score: number;
    verdict: string;
    novel_contributions: string[];
    overlapping_aspects: string[];
    innovation_type: string;
    comparison_summary: string;
  };
}

export default function NoveltyScore({ novelty }: NoveltyScoreProps) {
  const [dashOffset, setDashOffset] = useState(283); // Circle circumference
  const score = Math.max(0, Math.min(10, novelty.novelty_score));
  
  useEffect(() => {
    // 283 = 2 * pi * 45
    const offset = 283 - (283 * (score / 10));
    const timer = setTimeout(() => setDashOffset(offset), 100);
    return () => clearTimeout(timer);
  }, [score]);

  return (
    <div className="space-y-6 fade-in-up">
      {/* Top Banner */}
      <div className="glass-card p-8 rounded-2xl flex flex-col md:flex-row items-center gap-8 glow-purple border-t-purple-500/30 border-t-2">
        {/* Animated Score Ring */}
        <div className="relative w-40 h-40 shrink-0 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              className="text-gray-800"
              strokeWidth="6"
              stroke="currentColor"
              fill="transparent"
              r="45"
              cx="50"
              cy="50"
            />
            <circle
              className="text-purple-500 score-ring"
              strokeWidth="6"
              strokeDasharray="283"
              strokeDashoffset={dashOffset}
              strokeLinecap="round"
              stroke="currentColor"
              fill="transparent"
              r="45"
              cx="50"
              cy="50"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-br from-purple-400 to-blue-400">
              {score.toFixed(1)}
            </span>
            <span className="text-xs text-gray-400 uppercase tracking-widest mt-1">/ 10</span>
          </div>
        </div>

        {/* Info */}
        <div className="flex-1 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-sm font-bold uppercase tracking-wider mb-4">
            <SparklesIcon /> {novelty.verdict}
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Innovation Type: {novelty.innovation_type}</h2>
          <p className="text-gray-300 text-lg leading-relaxed">
            {novelty.comparison_summary}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Novelty List */}
        <div className="glass-card p-6 rounded-2xl border-t-teal-500/30 border-t-2">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Compass className="text-teal-400" />
            Truly Novel Aspects
          </h3>
          <ul className="space-y-4">
            {novelty.novel_contributions?.length > 0 ? (
              novelty.novel_contributions.map((c, i) => (
                <li key={i} className="flex gap-3 text-gray-300">
                  <span className="text-teal-400 shrink-0 mt-1">
                    <Zap size={16} />
                  </span>
                  <span className="leading-relaxed">{c}</span>
                </li>
              ))
            ) : (
              <p className="text-gray-500 italic">No significantly novel contributions identified.</p>
            )}
          </ul>
        </div>

        {/* Overlap List */}
        <div className="glass-card p-6 rounded-2xl border-t-amber-500/30 border-t-2">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Scale className="text-amber-400" />
            Derivative or Overlapping Aspects
          </h3>
          <ul className="space-y-4">
            {novelty.overlapping_aspects?.length > 0 ? (
              novelty.overlapping_aspects.map((o, i) => (
                <li key={i} className="flex gap-3 text-gray-300">
                  <span className="text-amber-400 shrink-0 mt-1">
                    <FileText size={16} />
                  </span>
                  <span className="leading-relaxed">{o}</span>
                </li>
              ))
            ) : (
              <p className="text-gray-500 italic">No significant overlap detected.</p>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}

function SparklesIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
    </svg>
  );
}
