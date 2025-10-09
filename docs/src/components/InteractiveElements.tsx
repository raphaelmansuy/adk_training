import React, { useState, useEffect } from 'react';
import styles from './InteractiveElements.module.css';

// Animated Progress Indicator
export function ProgressIndicator({ completed, total, label }: { completed: number; total: number; label: string }) {
  const [animatedProgress, setAnimatedProgress] = useState(0);
  const percentage = Math.round((completed / total) * 100);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedProgress(percentage);
    }, 300);
    return () => clearTimeout(timer);
  }, [percentage]);

  return (
    <div className={styles.progressContainer}>
      <div className={styles.progressLabel}>
        {label}: {completed}/{total} completed
      </div>
      <div className={styles.progressBar}>
        <div 
          className={styles.progressFill}
          style={{ width: `${animatedProgress}%` }}
        />
      </div>
      <div className={styles.progressPercentage}>{percentage}%</div>
    </div>
  );
}

// Interactive Tutorial Card with hover effects
export function InteractiveTutorialCard({ 
  title, 
  description, 
  difficulty, 
  duration, 
  completed, 
  link 
}: {
  title: string;
  description: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  duration: string;
  completed: boolean;
  link: string;
}) {
  const [isHovered, setIsHovered] = useState(false);

  const difficultyColors = {
    'Beginner': '#10b981',
    'Intermediate': '#f59e0b',
    'Advanced': '#ef4444'
  };

  return (
    <div 
      className={`${styles.tutorialCard} ${completed ? styles.completed : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={styles.cardHeader}>
        <div className={styles.cardStatus}>
          {completed ? '✅' : '📚'}
        </div>
        <div 
          className={styles.difficulty}
          style={{ backgroundColor: difficultyColors[difficulty] }}
        >
          {difficulty}
        </div>
      </div>
      
      <h3 className={styles.cardTitle}>{title}</h3>
      <p className={styles.cardDescription}>{description}</p>
      
      <div className={styles.cardFooter}>
        <span className={styles.duration}>⏱️ {duration}</span>
        <a 
          href={link}
          className={`${styles.cardButton} ${isHovered ? styles.buttonHovered : ''}`}
        >
          {completed ? 'Review' : 'Start'} →
        </a>
      </div>
    </div>
  );
}

// GitHub Stats Component with live data
export function GitHubStats() {
  const [stats, setStats] = useState({
    stars: 0,
    forks: 0,
    watchers: 0,
    loading: true
  });

  useEffect(() => {
    // Simulate API call - in real implementation, fetch from GitHub API
    const timer = setTimeout(() => {
      setStats({
        stars: 15,
        forks: 3,
        watchers: 8,
        loading: false
      });
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (stats.loading) {
    return <div className={styles.loading}>Loading GitHub stats...</div>;
  }

  return (
    <div className={styles.githubStats}>
      <div className={styles.statItem}>
        <span className={styles.statIcon}>⭐</span>
        <span className={styles.statNumber}>{stats.stars}</span>
        <span className={styles.statLabel}>Stars</span>
      </div>
      <div className={styles.statItem}>
        <span className={styles.statIcon}>🔱</span>
        <span className={styles.statNumber}>{stats.forks}</span>
        <span className={styles.statLabel}>Forks</span>
      </div>
      <div className={styles.statItem}>
        <span className={styles.statIcon}>👁️</span>
        <span className={styles.statNumber}>{stats.watchers}</span>
        <span className={styles.statLabel}>Watchers</span>
      </div>
    </div>
  );
}

// Learning Path Selector Quiz
export function LearningPathQuiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [showResult, setShowResult] = useState(false);

  const questions = [
    {
      question: "What's your experience with AI/ML?",
      options: ["Complete beginner", "Some experience", "Advanced user"]
    },
    {
      question: "Programming background?",
      options: ["New to programming", "Some Python experience", "Experienced developer"]
    },
    {
      question: "What's your goal?",
      options: ["Learn concepts", "Build a prototype", "Production deployment"]
    }
  ];

  const handleAnswer = (answer: string) => {
    const newAnswers = [...answers, answer];
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResult(true);
    }
  };

  const getRecommendation = () => {
    const score = answers.reduce((acc, answer) => {
      if (answer.includes('beginner') || answer.includes('New')) return acc + 1;
      if (answer.includes('Some')) return acc + 2;
      return acc + 3;
    }, 0);

    if (score <= 4) return { path: "Foundation Track", color: "#10b981" };
    if (score <= 7) return { path: "Advanced Workflows", color: "#f59e0b" };
    return { path: "Production Ready", color: "#ef4444" };
  };

  const reset = () => {
    setCurrentQuestion(0);
    setAnswers([]);
    setShowResult(false);
  };

  if (showResult) {
    const recommendation = getRecommendation();
    return (
      <div className={styles.quizResult}>
        <h3>Recommended Learning Path:</h3>
        <div 
          className={styles.recommendedPath}
          style={{ borderColor: recommendation.color }}
        >
          {recommendation.path}
        </div>
        <button onClick={reset} className={styles.retakeButton}>
          Retake Quiz
        </button>
      </div>
    );
  }

  return (
    <div className={styles.quiz}>
      <div className={styles.quizProgress}>
        Question {currentQuestion + 1} of {questions.length}
      </div>
      
      <h3 className={styles.question}>
        {questions[currentQuestion].question}
      </h3>
      
      <div className={styles.options}>
        {questions[currentQuestion].options.map((option, index) => (
          <button
            key={index}
            onClick={() => handleAnswer(option)}
            className={styles.optionButton}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}

// Animated Counter Component
export function AnimatedCounter({ 
  end, 
  duration = 2000, 
  label 
}: { 
  end: number; 
  duration?: number; 
  label: string; 
}) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const increment = end / (duration / 16);
    const timer = setInterval(() => {
      setCount(prev => {
        const next = prev + increment;
        if (next >= end) {
          clearInterval(timer);
          return end;
        }
        return next;
      });
    }, 16);

    return () => clearInterval(timer);
  }, [end, duration]);

  return (
    <div className={styles.animatedCounter}>
      <div className={styles.counterNumber}>
        {Math.floor(count)}
        {label.includes('%') && '%'}
      </div>
      <div className={styles.counterLabel}>{label}</div>
    </div>
  );
}