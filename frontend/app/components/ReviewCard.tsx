import { CheckCircle2, XCircle, HelpCircle, ChevronDown, Award } from 'lucide-react';
import { useState } from 'react';

interface ReviewCardProps {
  review: {
    summary: string;
    strengths: string[];
    weaknesses: string[];
    methodology_evaluation: string;
    clarity_score: number;
    technical_quality_score: number;
    novelty_rating: string;
    questions_for_authors: string[];
    recommendation: string;
    recommendation_reason: string;
  };
}

export default function ReviewCard({ review }: ReviewCardProps) {
  const [questionsOpen, setQuestionsOpen] = useState(false);

  const getRecommendationBadge = (rec: string) => {
    switch (rec.toLowerCase()) {
      case 'accept':
        return <span className="badge badge-accept">Accept</span>;
      case 'reject':
        return <span className="badge badge-reject">Reject</span>;
      default:
        return <span className="badge badge-revision">Revision Required</span>;
    }
  };

  const ScoreBar = ({ label, score }: { label: string; score: number }) => (
    <div className="mb-4">
      <div className="flex justify-between mb-1 text-sm font-medium">
        <span className="text-gray-300">{label}</span>
        <span className="text-purple-400">{score}/10</span>
      </div>
      <div className="progress-bar">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${(score / 10) * 100}%` }}
        ></div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6 fade-in-up">
      {/* Top section: Summary & Verdict */}
      <div className="glass-card p-6 md:p-8 rounded-2xl border-t-blue-500/30 border-t-2">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <Award className="text-blue-400" />
            AI Peer Review
          </h2>
          <div className="flex items-center gap-3 bg-white/5 p-2 pr-4 rounded-full border border-white/10">
            {getRecommendationBadge(review.recommendation)}
            <span className="text-sm font-medium text-gray-300 uppercase tracking-wider">
              {review.novelty_rating} Novelty
            </span>
          </div>
        </div>
        
        <p className="text-gray-300 leading-relaxed text-lg mb-6 pb-6 border-b border-white/5">
          {review.summary}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <ScoreBar label="Clarity Score" score={review.clarity_score} />
            <ScoreBar label="Technical Quality" score={review.technical_quality_score} />
          </div>
          <div className="bg-blue-500/5 border border-blue-500/20 p-4 rounded-xl text-sm text-blue-200">
            <h4 className="font-bold text-blue-400 mb-1">Recommendation Reasoning</h4>
            <p className="leading-relaxed">{review.recommendation_reason}</p>
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6 rounded-2xl border-t-teal-500/30 border-t-2">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-teal-400" />
            Strengths
          </h3>
          <ul className="space-y-3">
            {review.strengths.map((s, i) => (
              <li key={i} className="flex gap-3 text-gray-300">
                <span className="text-teal-400 shrink-0">+</span>
                <span className="leading-relaxed">{s}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-card p-6 rounded-2xl border-t-red-500/30 border-t-2">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <XCircle className="text-red-400" />
            Weaknesses
          </h3>
          <ul className="space-y-3">
            {review.weaknesses.map((w, i) => (
              <li key={i} className="flex gap-3 text-gray-300">
                <span className="text-red-400 shrink-0">-</span>
                <span className="leading-relaxed">{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Methodology Evaluation */}
      <div className="glass-card p-6 rounded-2xl">
        <h3 className="text-lg font-bold text-white mb-3">Methodology Evaluation</h3>
        <p className="text-gray-400 leading-relaxed">
          {review.methodology_evaluation}
        </p>
      </div>

      {/* Questions for Authors */}
      {review.questions_for_authors?.length > 0 && (
        <div className="glass-card rounded-2xl overflow-hidden glass-card-hover">
          <button 
            onClick={() => setQuestionsOpen(!questionsOpen)}
            className="w-full p-6 flex items-center justify-between text-left"
          >
            <div className="flex items-center gap-3">
              <HelpCircle className="text-amber-400" />
              <h3 className="text-lg font-bold text-white">Questions for Authors</h3>
              <span className="bg-amber-500/20 text-amber-400 text-xs px-2 py-0.5 rounded-full font-bold">
                {review.questions_for_authors.length}
              </span>
            </div>
            <ChevronDown className={`text-gray-400 transition-transform ${questionsOpen ? 'rotate-180' : ''}`} />
          </button>
          
          {questionsOpen && (
            <div className="px-6 pb-6 pt-0 border-t border-white/5 animate-in slide-in-from-top-2">
              <ul className="space-y-4 pt-4">
                {review.questions_for_authors.map((q, i) => (
                  <li key={i} className="flex gap-4">
                    <span className="shrink-0 w-6 h-6 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-xs mt-0.5">
                      ?
                    </span>
                    <p className="text-gray-300 leading-relaxed">{q}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
