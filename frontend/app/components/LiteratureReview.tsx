import { BookOpen, TrendingUp, AlertTriangle, Link as LinkIcon } from 'lucide-react';

interface LiteratureReviewProps {
  literature: {
    literature_review: string;
    research_trends: string[];
    existing_limitations: string[];
    key_references: {
      title: string;
      contribution: string;
    }[];
  };
}

export default function LiteratureReview({ literature }: LiteratureReviewProps) {
  let rawText = literature?.literature_review || '';
  
  // Sometimes the LLM returns a stringified JSON object instead of raw text
  if (rawText.trim().startsWith('{')) {
    try {
      const parsed = JSON.parse(rawText);
      if (parsed.literature_review) {
        rawText = parsed.literature_review;
      }
    } catch {
      // If it fails to parse (e.g., truncated JSON), extract via Regex
      const match = rawText.match(/"literature_review"\s*:\s*"([\s\S]*?)(?:",\s*"research_trends"|"\s*})/);
      if (match && match[1]) {
        rawText = match[1];
      } else {
        // Fallback for severely truncated strings
        const partialMatch = rawText.match(/"literature_review"\s*:\s*"([\s\S]*)/);
        if (partialMatch && partialMatch[1]) {
          rawText = partialMatch[1].replace(/"$/, '').replace(/\\"/g, '"');
        }
      }
    }
  }

  // Split review into paragraphs if it isn't already
  const paragraphs = rawText.split('\n\n').filter((p: string) => p.trim() !== '');

  return (
    <div className="space-y-6 fade-in-up">
      {/* Prose Section */}
      <div className="glass-card p-6 md:p-8 rounded-2xl glow-blue">
        <div className="flex items-center gap-3 mb-6">
          <BookOpen className="text-blue-400" size={28} />
          <h2 className="text-2xl font-bold text-white">Literature Synthesis</h2>
        </div>
        
        <div className="prose prose-invert max-w-none text-gray-300">
          {paragraphs.map((para, i) => (
            <p key={i} className="text-lg leading-relaxed mb-4">{para}</p>
          ))}
          {paragraphs.length === 0 && <p>No literature synthesis generated.</p>}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trends */}
        <div className="glass-card p-6 rounded-2xl glass-card-hover border-t-purple-500/30 border-t-2">
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp size={20} className="text-purple-400" />
            <h3 className="text-lg font-bold text-white">Identified Research Trends</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {literature.research_trends?.map((trend, i) => (
              <span key={i} className="px-3 py-1.5 bg-purple-500/10 text-purple-300 border border-purple-500/20 rounded-full text-sm">
                {trend}
              </span>
            ))}
          </div>
        </div>

        {/* Limitations */}
        <div className="glass-card p-6 rounded-2xl glass-card-hover border-t-red-500/30 border-t-2">
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle size={20} className="text-red-400" />
            <h3 className="text-lg font-bold text-white">Current Limitations in Field</h3>
          </div>
          <ul className="space-y-2">
            {literature.existing_limitations?.map((limitation, i) => (
              <li key={i} className="text-gray-300 text-sm leading-relaxed flex items-start gap-2">
                <span className="text-red-400 shrink-0 mt-1">•</span>
                <span>{limitation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Key References */}
      {literature.key_references?.length > 0 && (
        <div className="glass-card p-6 rounded-2xl overflow-hidden glass-card-hover border-t-teal-500/30 border-t-2">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <LinkIcon size={20} className="text-teal-400" />
            Key Foundational References
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-gray-300">
              <thead className="text-xs uppercase bg-white/5 text-gray-400">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Paper Title</th>
                  <th className="px-4 py-3 rounded-tr-lg">Contribution / Relevance</th>
                </tr>
              </thead>
              <tbody>
                {literature.key_references.map((ref, i) => (
                  <tr key={i} className="border-b border-white/5 last:border-0 hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-blue-300 align-top w-1/2">{ref.title}</td>
                    <td className="px-4 py-3 align-top">{ref.contribution}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
