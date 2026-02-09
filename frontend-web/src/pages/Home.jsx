import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { 
  TrendingUp, Shield, Zap, BarChart3, FileCheck, Lock, 
  Cloud, Users, Award, CheckCircle2, ArrowRight, Sparkles 
} from 'lucide-react';
import { motion } from 'framer-motion';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900 transition-colors duration-300">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10 dark:from-blue-600/5 dark:to-purple-600/5"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32 relative">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-6">
              <Sparkles size={16} className="text-blue-600 dark:text-blue-400" />
              <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">AI-Powered Analytics Platform</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 dark:text-white mb-6 leading-tight">
              Transform Equipment Data<br />
              Into <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Actionable Insights</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
              Enterprise-grade chemical equipment monitoring and analysis platform powered by Google Gemini AI. 
              Upload, analyze, and optimize your industrial operations in seconds.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <Link 
                to="/signup" 
                className="group px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition shadow-lg hover:shadow-blue-500/50 flex items-center justify-center gap-2"
              >
                Start Free Trial
                <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                to="/login" 
                className="px-8 py-4 bg-white dark:bg-slate-800 text-gray-800 dark:text-white border-2 border-gray-300 dark:border-slate-700 rounded-xl font-bold text-lg hover:border-blue-600 dark:hover:border-blue-500 transition"
              >
                Sign In
              </Link>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center gap-8 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center gap-2">
                <CheckCircle2 size={16} className="text-green-600" />
                <span>No Credit Card Required</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 size={16} className="text-green-600" />
                <span>256-bit Encryption</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 size={16} className="text-green-600" />
                <span>GDPR Compliant</span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-white dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Everything You Need for Equipment Analytics
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Comprehensive tools designed for chemical engineers and process optimization teams
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<BarChart3 size={32} />}
              title="Real-Time Analytics" 
              desc="Instant statistical analysis with health scoring, outlier detection, and correlation matrices. Get insights in seconds, not hours."
              color="blue"
            />
            <FeatureCard 
              icon={<Sparkles size={32} />}
              title="AI-Powered Insights" 
              desc="Google Gemini AI generates professional analysis reports with risk assessment and actionable recommendations."
              color="purple"
            />
            <FeatureCard 
              icon={<Shield size={32} />}
              title="Enterprise Security" 
              desc="Bank-level encryption, JWT authentication, and password-protected exports. Your data stays confidential."
              color="green"
            />
            <FeatureCard 
              icon={<TrendingUp size={32} />}
              title="Trend Analysis" 
              desc="Time-series visualization and predictive analytics to identify patterns and prevent equipment failures."
              color="orange"
            />
            <FeatureCard 
              icon={<FileCheck size={32} />}
              title="Professional Reports" 
              desc="Generate encrypted PDF and Excel reports with comprehensive analysis, charts, and executive summaries."
              color="red"
            />
            <FeatureCard 
              icon={<Zap size={32} />}
              title="Lightning Fast" 
              desc="Process thousands of data points in milliseconds. Optimized algorithms ensure instant results."
              color="yellow"
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Simple 3-Step Process
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              From data upload to actionable insights in under 60 seconds
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StepCard 
              number="01"
              title="Upload Your Data"
              desc="Drag and drop CSV files with equipment parameters. Supports flowrate, pressure, temperature, and custom metrics."
              icon={<Cloud size={40} />}
            />
            <StepCard 
              number="02"
              title="AI Analysis"
              desc="Our Gemini AI engine analyzes your data, detects anomalies, calculates health scores, and identifies risks."
              icon={<Sparkles size={40} />}
            />
            <StepCard 
              number="03"
              title="Get Insights"
              desc="View interactive dashboards, download encrypted reports, and implement recommendations immediately."
              icon={<Award size={40} />}
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <StatItem number="10,000+" label="Analyses Performed" />
            <StatItem number="99.9%" label="Uptime Guarantee" />
            <StatItem number="<3s" label="Average Processing" />
            <StatItem number="256-bit" label="Encryption Standard" />
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="py-20 bg-white dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Built for Chemical Engineers
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Trusted by process optimization teams worldwide
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <UseCaseCard 
              title="Process Optimization"
              desc="Identify inefficiencies, optimize parameters, and reduce operational costs through data-driven insights."
              benefits={["15-30% efficiency gains", "Reduced downtime", "Predictive maintenance"]}
            />
            <UseCaseCard 
              title="Compliance & Reporting"
              desc="Generate audit-ready reports with comprehensive analysis and password protection for regulatory compliance."
              benefits={["Automated reporting", "Audit trails", "Secure data handling"]}
            />
            <UseCaseCard 
              title="Equipment Monitoring"
              desc="Real-time health scoring and anomaly detection to prevent failures before they occur."
              benefits={["Early warning system", "Health scoring", "Outlier detection"]}
            />
            <UseCaseCard 
              title="Team Collaboration"
              desc="Share encrypted reports with stakeholders and maintain complete data security across your organization."
              benefits={["Secure sharing", "Role-based access", "Version control"]}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Ready to Transform Your Operations?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-10">
            Join hundreds of chemical engineers using our platform to optimize their processes
          </p>
          <Link 
            to="/signup" 
            className="inline-flex items-center gap-2 px-10 py-5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-bold text-xl hover:from-blue-700 hover:to-purple-700 transition shadow-2xl hover:shadow-blue-500/50"
          >
            Get Started Free
            <ArrowRight size={24} />
          </Link>
          <p className="mt-6 text-sm text-gray-500 dark:text-gray-400">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="border-t border-slate-800 pt-8 text-center text-sm">
            <p>&copy; 2024 POTASH. All rights reserved.</p>
            <p className="mt-2">Built with ❤️ for Chemical Engineers</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc, color }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    red: 'from-red-500 to-red-600',
    yellow: 'from-yellow-500 to-yellow-600'
  };

  return (
    <motion.div 
      whileHover={{ y: -5 }}
      className="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-lg border border-slate-200 dark:border-slate-700 hover:shadow-xl transition-all"
    >
      <div className={`inline-flex p-4 rounded-xl bg-gradient-to-r ${colors[color]} text-white mb-6`}>
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{desc}</p>
    </motion.div>
  );
};

const StepCard = ({ number, title, desc, icon }) => (
  <div className="relative">
    <div className="text-center">
      <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white mb-6">
        {icon}
      </div>
      <div className="absolute top-10 left-1/2 -translate-x-1/2 -z-10 text-9xl font-bold text-slate-100 dark:text-slate-800">
        {number}
      </div>
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{desc}</p>
    </div>
  </div>
);

const StatItem = ({ number, label }) => (
  <div>
    <div className="text-4xl md:text-5xl font-bold mb-2">{number}</div>
    <div className="text-blue-100 text-sm md:text-base">{label}</div>
  </div>
);

const UseCaseCard = ({ title, desc, benefits }) => (
  <div className="bg-slate-50 dark:bg-slate-800 p-8 rounded-2xl border border-slate-200 dark:border-slate-700">
    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">{title}</h3>
    <p className="text-gray-600 dark:text-gray-400 mb-6">{desc}</p>
    <ul className="space-y-3">
      {benefits.map((benefit, idx) => (
        <li key={idx} className="flex items-center gap-3 text-gray-700 dark:text-gray-300">
          <CheckCircle2 size={20} className="text-green-600 flex-shrink-0" />
          <span>{benefit}</span>
        </li>
      ))}
    </ul>
  </div>
);

export default Home;
