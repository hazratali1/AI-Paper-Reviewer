import { Telescope, ChevronRight } from 'lucide-react';

interface FutureScopeProps {
  futureScope: string[];
}

export default function FutureScope({ futureScope }: FutureScopeProps) {
  if (!futureScope || futureScope.length === 0) {
    return (
      <div className="space-y-6 fade-in-up">
        <div className="glass-card p-6 md:p-8 rounded-2xl glow-blue">
          <div className="flex items-center gap-3 mb-6">
            <Telescope className="text-blue-400" size={28} />
            <h2 className="text-2xl font-bold text-white">Future Scope & Improvements</h2>
          </div>
          <p className="text-gray-400">No future scope generated.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in-up">
      <div className="glass-card p-6 md:p-8 rounded-2xl glow-blue">
        <div className="flex items-center gap-3 mb-6">
          <Telescope className="text-blue-400" size={28} />
          <h2 className="text-2xl font-bold text-white">Future Scope & Improvements</h2>
        </div>
        
        <div className="space-y-4">
          <p className="text-lg text-gray-300 mb-6">
            Based on the limitations and methodology of this paper, here are actionable improvements and directions for future research:
          </p>
          
          <ul className="space-y-4">
            {futureScope.map((item, idx) => (
              <li key={idx} className="flex items-start gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg shrink-0 mt-0.5">
                  <ChevronRight size={16} />
                </div>
                <p className="text-gray-200 leading-relaxed">{item}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
