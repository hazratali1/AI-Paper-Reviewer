"use client";

import { useEffect, useState } from 'react';
import { Brain, FileSearch, Sparkles, BookOpen, Layers } from 'lucide-react';

const AGENTS = [
  { id: 'parser', name: 'Parsing Document Structure', icon: FileSearch, color: 'text-blue-400', bg: 'bg-blue-400/10' },
  { id: 'analyzer', name: 'Extracting Contributions', icon: Brain, color: 'text-purple-400', bg: 'bg-purple-400/10' },
  { id: 'literature', name: 'Synthesizing Literature Review', icon: BookOpen, color: 'text-teal-400', bg: 'bg-teal-400/10' },
  { id: 'novelty', name: 'Assessing Novelty', icon: Sparkles, color: 'text-amber-400', bg: 'bg-amber-400/10' },
  { id: 'reviewer', name: 'Generating Peer Review', icon: Layers, color: 'text-pink-400', bg: 'bg-pink-400/10' },
];

export default function AnalysisProgress() {
  const [currentStep, setCurrentStep] = useState(0);

  // Fake progress cycle for visual feedback
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < AGENTS.length - 1 ? prev + 1 : prev));
    }, 4000); // Step every 4 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col items-center justify-center py-16 px-4 fade-in-up">
      <div className="relative w-32 h-32 mb-12">
        {/* Pulsing rings */}
        <div className="absolute inset-0 rounded-full border border-purple-500/30 animate-[ping_3s_ease-in-out_infinite]"></div>
        <div className="absolute inset-2 rounded-full border border-blue-500/20 animate-[ping_3s_ease-in-out_infinite_0.5s]"></div>
        
        {/* Core brain icon */}
        <div className="absolute inset-4 rounded-full bg-gradient-to-br from-purple-600/20 to-blue-600/20 glass-card flex items-center justify-center pulse-glow">
          <Brain size={48} className="text-purple-400 animate-pulse" />
        </div>
      </div>

      <h2 className="text-3xl font-bold mb-4 gradient-text text-center">Analyzing Research Paper</h2>
      <p className="text-gray-400 mb-12 text-center max-w-md">
        Our multi-agent AI system is processing the document, extracting contributions, and evaluating novelty. This takes about 30 seconds.
      </p>

      {/* Steps List */}
      <div className="w-full max-w-md space-y-4">
        {AGENTS.map((agent, index) => {
          const isActive = index === currentStep;
          const isDone = index < currentStep;
          const Icon = agent.icon;

          return (
            <div 
              key={agent.id}
              className={`flex items-center gap-4 p-4 rounded-xl border transition-all duration-500 ${
                isActive ? 'glass-card border-white/20 scale-105' : 
                isDone ? 'border-white/5 opacity-60' : 'border-transparent opacity-30'
              }`}
            >
              <div className={`p-3 rounded-lg ${isActive ? agent.bg : 'bg-white/5'}`}>
                <Icon size={24} className={`${isActive || isDone ? agent.color : 'text-gray-500'} ${isActive ? 'animate-pulse' : ''}`} />
              </div>
              <div className="flex-1">
                <h4 className={`font-medium ${isActive ? 'text-white' : 'text-gray-400'}`}>
                  {agent.name}
                </h4>
                {isActive && (
                  <div className="mt-2 h-1 w-full bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-purple-500 to-blue-500 w-1/2 rounded-full shimmer"></div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
