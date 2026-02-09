import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import toast, { Toaster } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import { uploadCSV, getHistory, downloadPDF, downloadExcel, deleteDataset, getAnalysis, compareDatasets } from '../services/api';
import Navbar from '../components/Navbar';
import { 
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, 
  BarElement, Title, Tooltip, Legend, ArcElement, RadialLinearScale 
} from 'chart.js';
import { Bar, Pie, Radar, Scatter, Line } from 'react-chartjs-2';
import { 
  Upload, FileText, Trash2, Download, Activity, Cpu, AlertTriangle, 
  Zap, Eye, TrendingUp, GitCompare, Loader, CheckCircle, XCircle 
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, 
  BarElement, Title, Tooltip, Legend, ArcElement, RadialLinearScale
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [currentFileId, setCurrentFileId] = useState(null);
  const [compareMode, setCompareMode] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const refreshHistory = useCallback(async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) { 
      console.error(err);
      if (err.response?.status === 401) {
        navigate('/login');
      }
    }
  }, [navigate]);

  // Keyboard shortcut: Ctrl+U to upload
  useEffect(() => {
    const handleKeyPress = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        fileInputRef.current?.click();
      }
    };
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  const handleUpload = useCallback(async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    setUploadProgress(0);
    const loadingToast = toast.loading('Uploading and analyzing...');
    
    try {
      const res = await uploadCSV(formData, (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percentCompleted);
      });
      
      setStats(res.data);
      setCurrentFileId(res.file_id);
      refreshHistory();
      toast.success('✅ Analysis Complete!', { id: loadingToast });
    } catch (error) {
      console.error(error);
      const errorMsg = error.response?.data?.error || 'Upload failed';
      toast.error(errorMsg, { id: loadingToast });
    }
    setLoading(false);
    setUploadProgress(0);
  }, [refreshHistory]);

  const handleHistorySelect = async (id) => {
    if (compareMode) {
      if (selectedFiles.includes(id)) {
        setSelectedFiles(selectedFiles.filter(f => f !== id));
      } else if (selectedFiles.length < 2) {
        setSelectedFiles([...selectedFiles, id]);
      } else {
        toast.error('Maximum 2 files for comparison');
      }
      return;
    }

    setLoading(true);
    const loadingToast = toast.loading('Loading analysis...');
    try {
        const res = await getAnalysis(id);
        setStats(res.data);
        setCurrentFileId(res.file_id);
        setComparisonData(null);
        toast.success('Loaded from History', { id: loadingToast });
    } catch (error) {
        console.error(error);
        toast.error('Failed to load file', { id: loadingToast });
    }
    setLoading(false);
  };

  const handleCompare = async () => {
    if (selectedFiles.length !== 2) {
      toast.error('Please select exactly 2 files');
      return;
    }

    setLoading(true);
    const loadingToast = toast.loading('Comparing datasets...');
    try {
      const data = await compareDatasets(selectedFiles[0], selectedFiles[1]);
      setComparisonData(data);
      setStats(null);
      toast.success('Comparison ready!', { id: loadingToast });
    } catch (error) {
      toast.error('Comparison failed', { id: loadingToast });
    }
    setLoading(false);
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        navigate('/login');
    } else {
        refreshHistory();
    }
  }, [navigate, refreshHistory]);

  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    if (file) handleUpload(file);
  }, [handleUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop, 
    accept: {'text/csv': ['.csv']},
    maxFiles: 1,
    disabled: loading 
  });

  const handleDownload = async (type) => {
    if (!currentFileId) {
      toast.error('No file selected');
      return;
    }
    const pw = prompt(`Enter password to encrypt ${type.toUpperCase()}:`);
    if (!pw) return;
    
    const toastId = toast.loading(`Generating ${type.toUpperCase()}...`);
    try {
      const filename = history.find(h => h.id === currentFileId)?.filename || 'report';
      if (type === 'pdf') await downloadPDF(currentFileId, filename, pw);
      else await downloadExcel(currentFileId, filename, pw);
      toast.success('✅ Downloaded successfully', { id: toastId });
    } catch (error) {
      toast.error('Download failed', { id: toastId });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-300">
      <Navbar />
      <Toaster position="bottom-right" />

      <motion.main 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-4 gap-8"
      >
        
        {/* SIDEBAR */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Upload size={20} className="text-blue-600" /> Upload Data
            </h2>
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
                isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-300 dark:border-slate-700 hover:border-blue-400'
              } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <input {...getInputProps()} ref={fileInputRef} />
              <div className="flex flex-col items-center gap-2 text-slate-500">
                {loading ? <Loader size={32} className="animate-spin" /> : <FileText size={32} />}
                <p className="text-sm font-medium">
                  {loading ? "Processing..." : "Drag & Drop CSV"}
                </p>
                <p className="text-xs text-slate-400">or click to browse</p>
              </div>
            </div>
            
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={loading}
              className="w-full mt-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2"
            >
              <Upload size={18} />
              Choose File
            </button>
            
            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="mt-4">
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-xs text-center mt-1 text-slate-500">{uploadProgress}%</p>
              </div>
            )}
          </div>

          <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold flex items-center gap-2">
                <Activity size={20} className="text-purple-600" /> History
              </h2>
              <button
                onClick={() => {
                  setCompareMode(!compareMode);
                  setSelectedFiles([]);
                  setComparisonData(null);
                }}
                className={`p-2 rounded-lg transition ${compareMode ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600'}`}
                title="Compare Mode"
              >
                <GitCompare size={16} />
              </button>
            </div>

            {compareMode && (
              <div className="mb-3">
                <button
                  onClick={handleCompare}
                  disabled={selectedFiles.length !== 2}
                  className="w-full py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                >
                  Compare Selected ({selectedFiles.length}/2)
                </button>
              </div>
            )}

            <div className="space-y-3 max-h-96 overflow-y-auto">
              {history.length === 0 && <p className="text-sm text-slate-400 italic">No history yet.</p>}
              {history.map((item) => (
                <div 
                  key={item.id} 
                  className={`group flex justify-between items-center p-3 rounded-lg transition cursor-pointer ${
                    compareMode && selectedFiles.includes(item.id) 
                      ? 'bg-blue-100 dark:bg-blue-900/30 border-2 border-blue-500' 
                      : currentFileId === item.id 
                      ? 'bg-blue-50 border-blue-200 border' 
                      : 'bg-slate-50 dark:bg-slate-800/50 hover:bg-blue-50 dark:hover:bg-blue-900/20'
                  }`}
                  onClick={() => handleHistorySelect(item.id)}
                >
                  <div className="truncate flex-1">
                    <p className="text-sm font-medium truncate">{item.filename}</p>
                    <div className="flex gap-2 text-xs text-slate-400">
                      <span>{new Date(item.uploaded_at).toLocaleDateString()}</span>
                      {item.row_count > 0 && <span>• {item.row_count} rows</span>}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {compareMode && selectedFiles.includes(item.id) && (
                      <CheckCircle size={16} className="text-blue-500" />
                    )}
                    {!compareMode && (
                      <>
                        <Eye size={16} className="text-blue-400 opacity-0 group-hover:opacity-100" />
                        <button 
                          onClick={(e) => { 
                            e.stopPropagation(); 
                            if (window.confirm('Delete this file?')) {
                              deleteDataset(item.id).then(refreshHistory);
                            }
                          }}
                          className="text-slate-400 hover:text-red-500 transition opacity-0 group-hover:opacity-100"
                        >
                          <Trash2 size={16} />
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* MAIN AREA */}
        <div className="lg:col-span-3 space-y-6">
          {comparisonData ? (
            <ComparisonView data={comparisonData} />
          ) : !stats ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl min-h-[400px]">
              <Cpu size={48} className="mb-4 opacity-50" />
              <p className="text-lg font-medium">Upload a file or select from history</p>
              <p className="text-sm mt-2">Press <kbd className="px-2 py-1 bg-slate-200 dark:bg-slate-800 rounded">Ctrl+U</kbd> to upload</p>
            </div>
          ) : (
            <AnalysisView stats={stats} onDownload={handleDownload} />
          )}
        </div>
      </motion.main>
    </div>
  );
};

// Analysis View Component
const AnalysisView = ({ stats, onDownload }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <StatCard title="Total Equipment" value={stats.total_count} icon={<Cpu />} color="blue" />
      <StatCard title="Avg Pressure" value={`${stats.averages.Pressure.toFixed(1)} bar`} icon={<Activity />} color="green" />
      <StatCard title="Avg Temp" value={`${stats.averages.Temperature.toFixed(1)} °C`} icon={<Zap />} color="orange" />
      <StatCard title="Health Score" value={`${stats.health_score_avg?.toFixed(1) || 85.2}%`} icon={<AlertTriangle />} color="purple" />
    </div>

    <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
      <div className="relative z-10">
        <h3 className="text-lg font-bold mb-2 flex items-center gap-2">✨ Gemini AI Analysis</h3>
        <div className="prose prose-invert max-w-none text-sm opacity-90 whitespace-pre-line">
          <p>{stats.ai_insights}</p>
        </div>
      </div>
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-white opacity-10 blur-3xl"></div>
    </div>

    {stats.outlier_details && stats.outlier_details.length > 0 && (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl p-6">
        <h3 className="text-lg font-bold mb-3 flex items-center gap-2 text-red-700 dark:text-red-400">
          <AlertTriangle size={20} /> Outliers Detected
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {stats.outlier_details.map((outlier, idx) => (
            <div key={idx} className="bg-white dark:bg-slate-900 p-4 rounded-lg">
              <p className="text-sm font-medium text-slate-700 dark:text-slate-300">{outlier.parameter}</p>
              <p className="text-2xl font-bold text-red-600">{outlier.count}</p>
              <p className="text-xs text-slate-500">{outlier.percentage}% of data</p>
            </div>
          ))}
        </div>
      </div>
    )}

    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <ChartCard title="Equipment Types Distribution">
        <Pie data={{
          labels: Object.keys(stats.type_distribution),
          datasets: [{
            data: Object.values(stats.type_distribution),
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'],
            borderWidth: 0
          }]
        }} options={{ maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }} />
      </ChartCard>

      <ChartCard title="Health Score Distribution">
        <Bar data={{
          labels: ['Excellent (90+)', 'Good (70-89)', 'Fair (50-69)', 'Poor (<50)'],
          datasets: [{
            label: 'Equipment Count',
            data: [
              stats.health_score_distribution?.excellent || 0,
              stats.health_score_distribution?.good || 0,
              stats.health_score_distribution?.fair || 0,
              stats.health_score_distribution?.poor || 0
            ],
            backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
            borderRadius: 8
          }]
        }} options={{ maintainAspectRatio: false }} />
      </ChartCard>

      <ChartCard title="Parameter Correlations">
        <Scatter data={{
          datasets: [{
            label: 'Pressure vs Temperature',
            data: stats.raw_data.map(row => ({
              x: parseFloat(row.Pressure || 0),
              y: parseFloat(row.Temperature || 0)
            })),
            backgroundColor: 'rgba(59, 130, 246, 0.6)',
            pointRadius: 5
          }]
        }} options={{ maintainAspectRatio: false }} />
      </ChartCard>

      <ChartCard title="Average Metrics">
        <Bar data={{
          labels: ['Flowrate', 'Pressure', 'Temperature'],
          datasets: [{
            label: 'Average Values',
            data: [stats.averages.Flowrate, stats.averages.Pressure, stats.averages.Temperature],
            backgroundColor: ['#6366f1', '#10b981', '#f59e0b'],
            borderRadius: 8
          }]
        }} options={{ maintainAspectRatio: false }} />
      </ChartCard>
    </div>

    <div className="flex justify-end gap-3">
      <button onClick={() => onDownload('pdf')} className="flex items-center gap-2 px-6 py-3 bg-slate-800 dark:bg-slate-700 text-white rounded-lg hover:bg-slate-700 transition shadow-lg">
        <Download size={16} /> Export PDF
      </button>
      <button onClick={() => onDownload('excel')} className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition shadow-lg">
        <Download size={16} /> Export Excel
      </button>
    </div>
  </div>
);

// Comparison View Component
const ComparisonView = ({ data }) => (
  <div className="space-y-6">
    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-2xl p-6">
      <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
        <GitCompare size={24} /> Dataset Comparison
      </h2>
      <p className="text-sm text-slate-600 dark:text-slate-400">
        Comparing: <span className="font-medium">{data.dataset1.name}</span> vs <span className="font-medium">{data.dataset2.name}</span>
      </p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <ComparisonCard title={data.dataset1.name} stats={data.dataset1.stats} color="blue" />
      <ComparisonCard title={data.dataset2.name} stats={data.dataset2.stats} color="purple" />
    </div>
  </div>
);

const ComparisonCard = ({ title, stats, color }) => {
  const colorClasses = {
    blue: 'border-blue-500 bg-blue-50 dark:bg-blue-900/20',
    purple: 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
  };

  return (
    <div className={`border-2 ${colorClasses[color]} rounded-2xl p-6`}>
      <h3 className="text-lg font-bold mb-4 truncate">{title}</h3>
      <div className="space-y-3">
        <MetricRow label="Total Equipment" value={stats.total_count} />
        <MetricRow label="Avg Health Score" value={`${stats.health_score_avg.toFixed(1)}%`} />
        <MetricRow label="Outliers" value={stats.outliers_count} />
        <MetricRow label="Avg Pressure" value={`${stats.averages.Pressure.toFixed(1)} bar`} />
        <MetricRow label="Avg Temperature" value={`${stats.averages.Temperature.toFixed(1)} °C`} />
      </div>
    </div>
  );
};

const MetricRow = ({ label, value }) => (
  <div className="flex justify-between items-center py-2 border-b border-slate-200 dark:border-slate-700">
    <span className="text-sm text-slate-600 dark:text-slate-400">{label}</span>
    <span className="text-sm font-bold">{value}</span>
  </div>
);

const StatCard = ({ title, value, icon, color }) => {
  const colors = {
    blue: "bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400",
    green: "bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400",
    orange: "bg-orange-50 text-orange-600 dark:bg-orange-900/20 dark:text-orange-400",
    purple: "bg-purple-50 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400",
  };
  return (
    <motion.div 
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="bg-white dark:bg-slate-900 p-5 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 flex items-center gap-4"
    >
      <div className={`p-3 rounded-xl ${colors[color]}`}>{icon}</div>
      <div>
        <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{title}</p>
        <p className="text-2xl font-bold text-slate-800 dark:text-slate-100">{value}</p>
      </div>
    </motion.div>
  );
};

const ChartCard = ({ title, children }) => (
  <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 h-80 flex flex-col">
    <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-4">{title}</h3>
    <div className="flex-1 relative w-full h-full">{children}</div>
  </div>
);

export default Dashboard;
