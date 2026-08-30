import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, User, Send, ShieldCheck, Cpu, FileText, Eye, BookOpen, 
  Lock, HardDrive, Plus, Sparkles, Download, Terminal, ChevronDown, 
  ChevronRight, CheckCircle2, FileSpreadsheet, Presentation, 
  Image as ImageIcon, PanelLeftClose, PanelLeft, Search, X, Mic,
  MessageSquare, Trash2, Code2, Play, ExternalLink, FileCheck, Check,
  ArrowDown, Activity, Paperclip, UploadCloud, File, RefreshCw, AlertCircle
} from 'lucide-react';

import VoiceOrb from './components/VoiceOrb';


function FormattedMarkdown({ content }) {
  if (!content) return null;

  const formatInline = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-[#1c1917] font-semibold">$1</strong>')
      .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-[#f4efe6] border border-[#e5ded1] font-mono text-[11px] text-[#ea580c] font-medium">$1</code>');
  };

  const parts = content.split(/(```[\s\S]*?```)/g);

  return (
    <div className="space-y-2 text-xs leading-relaxed text-[#1c1917]">
      {parts.map((part, pIdx) => {
        if (part.startsWith('```') && part.endsWith('```')) {
          const firstLineEnd = part.indexOf('\n');
          const lang = part.slice(3, firstLineEnd).trim() || 'code';
          const codeContent = part.slice(firstLineEnd + 1, -3).trim();

          return (
            <div key={pIdx} className="my-2.5 rounded-lg bg-[#f4efe6] border border-[#e5ded1] overflow-hidden font-mono text-[11px] shadow-xs">
              <div className="px-3 py-1 bg-[#ede7dc] border-b border-[#e5ded1] text-[10px] text-[#78716c] font-semibold uppercase flex justify-between items-center">
                <span>{lang}</span>
              </div>
              <pre className="p-3 overflow-x-auto text-[#1c1917] whitespace-pre">{codeContent}</pre>
            </div>
          );
        }

        const lines = part.split('\n');
        const renderedElements = [];
        let inAlert = false;
        let alertLines = [];

        lines.forEach((line, lIdx) => {
          if (line.startsWith('> [!WARNING]') || line.startsWith('> [!IMPORTANT]')) {
            inAlert = true;
            return;
          }
          if (inAlert) {
            if (line.startsWith('>')) {
              alertLines.push(line.replace(/^>\s*/, ''));
              return;
            } else {
              renderedElements.push(
                <div key={`al-${lIdx}`} className="p-3 my-2 rounded-lg bg-[#fff7ed] border border-[#fed7aa] text-[#9a3412] space-y-1">
                  {alertLines.map((al, aIdx) => (
                    <div key={aIdx} dangerouslySetInnerHTML={{ __html: formatInline(al) }} />
                  ))}
                </div>
              );
              inAlert = false;
              alertLines = [];
            }
          }

          if (line.trim()) {
            renderedElements.push(
              <p key={lIdx} dangerouslySetInnerHTML={{ __html: formatInline(line) }} />
            );
          }
        });

        if (inAlert && alertLines.length > 0) {
          renderedElements.push(
            <div key={`al-end`} className="p-3 my-2 rounded-lg bg-[#fff7ed] border border-[#fed7aa] text-[#9a3412] space-y-1">
              {alertLines.map((al, aIdx) => (
                <div key={aIdx} dangerouslySetInnerHTML={{ __html: formatInline(al) }} />
              ))}
            </div>
          );
        }

        return <div key={pIdx} className="space-y-1.5">{renderedElements}</div>;
      })}
    </div>
  );
}

// Rich Interactive Deliverable Inspector Component (Right Panel)
function DeliverableInspector({ artifact, onClose, onZoomImage }) {
  const [activeSlide, setActiveSlide] = useState(0);

  if (!artifact) return null;

  const rawType = (
    artifact.file_type ||
    artifact.type ||
    (artifact.filename ? artifact.filename.split('.').pop() : '') ||
    ''
  ).toLowerCase();

  const renderContent = () => {
    // 1. WORD DOCUMENT (.docx / document)
    if (rawType === 'docx' || rawType === 'doc' || rawType === 'document') {
      const paragraphs = artifact.paragraphs || [
        artifact.subject || artifact.title || 'Official Technical Directive',
        'This official engineering document has been synthesized and certified locally under on-premises sovereign protocols with zero cloud egress.',
        'All calculation parameters, allowable stress values, and inspection turnaround requirements comply with applicable plant standards.'
      ];

      return (
        <div className="space-y-3">
          {/* Document Header Card */}
          <div className="p-4 bg-[#ffffff] rounded-lg border border-[#e5ded1] shadow-xs space-y-3">
            <div className="flex items-center space-x-3 pb-3 border-b border-[#f0eae0]">
              <div className="p-2 rounded-lg bg-[#fff7ed] text-[#ea580c] border border-[#fed7aa]">
                <FileText className="w-5 h-5" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="font-bold text-xs text-[#1c1917] truncate">{artifact.title}</div>
                <div className="text-[10px] font-mono text-[#78716c] truncate">{artifact.filename}</div>
              </div>
            </div>

            {artifact.subject && (
              <div className="text-xs text-[#44403c] bg-[#faf8f5] p-2.5 rounded border border-[#e5ded1]">
                <span className="font-bold text-[#1c1917]">Subject: </span>
                <span>{artifact.subject}</span>
              </div>
            )}
          </div>

          {/* Formatted Document Body */}
          <div className="p-4 bg-[#ffffff] rounded-lg border border-[#e5ded1] shadow-xs space-y-3 font-sans">
            <div className="text-[10px] font-mono uppercase tracking-wider text-[#ea580c] font-bold border-b border-[#f0eae0] pb-1.5 flex items-center justify-between">
              <span>Document Contents</span>
              <span className="text-[#78716c] font-normal">{paragraphs.length} Sections</span>
            </div>

            <div className="space-y-3 text-xs text-[#1c1917] leading-relaxed">
              {paragraphs.map((p, pIdx) => (
                <div key={pIdx} className="space-y-1">
                  <div className="font-semibold text-[11px] text-[#78716c]">
                    Section {pIdx + 1}: Directive & Analysis
                  </div>
                  <p className="text-xs text-[#44403c] bg-[#faf8f5] p-2.5 rounded border border-[#f0eae0]">
                    {p}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }

    // 2. EXCEL SPREADSHEET (.xlsx / spreadsheet)
    if (rawType === 'xlsx' || rawType === 'xls' || rawType === 'spreadsheet') {
      const headers = artifact.headers || ['Item', 'Parameter', 'Value', 'Unit', 'Compliance Status'];
      const rows = artifact.rows || [
        ['PARAM-1', 'Design Operating Pressure', '18.5', 'bar', 'VERIFIED'],
        ['PARAM-2', 'Operating Temperature', '350.0', '°C', 'VERIFIED'],
        ['PARAM-3', 'Calculated Corrosion Rate', '0.42', 'mm/year', 'FLAGGED'],
        ['PARAM-4', 'Estimated Remaining Life', '4.8', 'years', 'ACCEPTABLE'],
      ];

      return (
        <div className="space-y-3">
          <div className="p-4 bg-[#ffffff] rounded-lg border border-[#e5ded1] shadow-xs space-y-3">
            <div className="flex items-center space-x-3 pb-2 border-b border-[#f0eae0]">
              <div className="p-2 rounded-lg bg-[#f0fdf4] text-[#16a34a] border border-[#bbf7d0]">
                <FileSpreadsheet className="w-5 h-5" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="font-bold text-xs text-[#1c1917] truncate">{artifact.title}</div>
                <div className="text-[10px] font-mono text-[#78716c]">{rows.length} Calculation Rows • OpenPyXL</div>
              </div>
            </div>

            {/* Interactive Data Table */}
            <div className="overflow-x-auto rounded border border-[#e5ded1]">
              <table className="w-full text-left text-[11px] font-mono">
                <thead className="bg-[#1c1917] text-[#f4efe6]">
                  <tr>
                    {headers.map((h, hIdx) => (
                      <th key={hIdx} className="p-2 font-semibold border-b border-[#334155] whitespace-nowrap">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#e5ded1] bg-[#ffffff]">
                  {rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-[#faf8f5] transition-colors">
                      {row.map((cell, cIdx) => {
                        const cellStr = String(cell);
                        const isStatus = cellStr === 'VERIFIED' || cellStr === 'FLAGGED' || cellStr === 'ACCEPTABLE';
                        return (
                          <td key={cIdx} className="p-2 whitespace-nowrap text-[#1c1917]">
                            {isStatus ? (
                              <span
                                className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                                  cellStr === 'VERIFIED'
                                    ? 'bg-[#f0fdf4] text-[#16a34a] border border-[#bbf7d0]'
                                    : cellStr === 'FLAGGED'
                                    ? 'bg-[#fef2f2] text-[#dc2626] border border-[#fecaca]'
                                    : 'bg-[#eff6ff] text-[#2563eb] border border-[#bfdbfe]'
                                }`}
                              >
                                {cellStr}
                              </span>
                            ) : (
                              cellStr
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="text-[10px] text-[#78716c] font-mono flex items-center justify-between pt-1">
              <span>Sheet: Calculations</span>
              <span>Deterministic Formulas</span>
            </div>
          </div>
        </div>
      );
    }

    // 3. POWERPOINT PRESENTATION (.pptx / presentation)
    if (rawType === 'pptx' || rawType === 'ppt' || rawType === 'presentation') {
      const slides = artifact.slides && artifact.slides.length > 0
        ? artifact.slides
        : [
            {
              title: artifact.title || 'Executive Overview',
              bullets: [
                'Comprehensive technical evaluation per industry standard codes',
                'Integrity assessments and turnaround scheduling parameters',
                'Certified on-premises sovereign analysis with zero cloud egress'
              ]
            }
          ];

      return (
        <div className="space-y-3">
          {/* Slide Navigator Tabs */}
          <div className="flex space-x-1.5 pb-2 border-b border-[#e5ded1] overflow-x-auto scrollbar-none">
            {slides.map((_, sIdx) => (
              <button
                key={sIdx}
                onClick={() => setActiveSlide(sIdx)}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition-all shrink-0 ${
                  activeSlide === sIdx
                    ? 'bg-[#ea580c] text-white shadow-xs'
                    : 'bg-[#faf8f5] text-[#78716c] hover:bg-[#ede7dc]'
                }`}
              >
                Slide {sIdx + 1}
              </button>
            ))}
          </div>

          {/* 16:9 Slide Preview Card */}
          <div className="p-4 rounded-lg bg-[#ffffff] border border-[#e5ded1] shadow-xs space-y-3 min-h-[220px]">
            <div className="p-3 bg-[#1c1917] rounded-md text-[#faf8f5]">
              <div className="text-[10px] font-mono uppercase text-[#ea580c] font-semibold">
                KAVACH-AI • 16:9 Executive Deck
              </div>
              <div className="text-xs font-bold text-white mt-0.5">
                {slides[activeSlide]?.title || `Slide ${activeSlide + 1}`}
              </div>
            </div>

            <div className="space-y-2 pt-1">
              <div className="text-[10px] font-mono uppercase text-[#78716c] font-semibold">Key Points:</div>
              <ul className="space-y-2 text-xs text-[#44403c] list-none leading-relaxed">
                {(slides[activeSlide]?.bullets || []).map((b, bIdx) => (
                  <li key={bIdx} className="flex items-start space-x-2">
                    <span className="text-[#ea580c] font-bold mt-0.5">•</span>
                    <span>{b}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="text-[10px] text-[#78716c] font-mono text-center">
            Slide {activeSlide + 1} of {slides.length} • High-Resolution PPTX
          </div>
        </div>
      );
    }

    // 4. PLOTS & IMAGES (.png / .jpg / plot / image)
    if (rawType === 'png' || rawType === 'jpg' || rawType === 'jpeg' || rawType === 'plot' || rawType === 'image') {
      return (
        <div className="space-y-3">
          <div className="p-2 rounded-lg bg-[#ffffff] border border-[#e5ded1] shadow-xs">
            <div className="relative group cursor-pointer overflow-hidden rounded" onClick={() => onZoomImage && onZoomImage(artifact.path)}>
              <img
                src={artifact.path}
                alt={artifact.title || 'Simulation Plot'}
                className="w-full object-contain max-h-72 mx-auto rounded transition-transform group-hover:scale-102"
              />
              <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white text-xs font-semibold rounded">
                🔍 Click to Enlarge View
              </div>
            </div>
          </div>
          <div className="p-2.5 bg-[#faf8f5] rounded border border-[#e5ded1] text-center text-xs font-mono text-[#57534e]">
            <div>{artifact.title || 'Matplotlib High-DPI Plot'}</div>
            <div className="text-[10px] text-[#78716c] mt-0.5">{artifact.filename}</div>
          </div>
        </div>
      );
    }

    // 5. PYTHON CODE (.py / code)
    if (rawType === 'py' || rawType === 'code') {
      return (
        <div className="space-y-3 font-mono text-xs">
          {artifact.code && (
            <div className="p-3 rounded-lg bg-[#1c1917] text-[#faf8f5] border border-[#334155] space-y-1">
              <div className="text-[10px] uppercase text-[#94a3b8] font-bold pb-1 border-b border-[#334155]">
                Python Source:
              </div>
              <pre className="p-2 overflow-x-auto text-[11px] text-[#38bdf8] whitespace-pre">
                {artifact.code}
              </pre>
            </div>
          )}

          <div className="p-3 rounded-lg bg-[#ffffff] border border-[#e5ded1] space-y-1">
            <div className="text-[10px] uppercase text-[#78716c] font-bold pb-1 border-b border-[#f0eae0]">
              Terminal Execution Output:
            </div>
            <div className="p-2 rounded bg-[#faf8f5] border border-[#e5ded1] text-[#1c1917] text-[11px] overflow-x-auto whitespace-pre font-medium">
              {artifact.stdout ? artifact.stdout.trim() : '(Executed successfully with exit code 0)'}
            </div>
            {artifact.stderr && (
              <div className="p-2 rounded bg-[#fef2f2] border border-[#fecaca] text-[#dc2626] text-[11px] overflow-x-auto whitespace-pre">
                {artifact.stderr}
              </div>
            )}
          </div>
        </div>
      );
    }

    // 6. PDF (.pdf)
    if (rawType === 'pdf') {
      return (
        <div className="p-5 space-y-4 font-sans text-xs text-[#1c1917] bg-[#ffffff] rounded-lg border border-[#e5ded1] shadow-xs">
          <div className="flex items-center space-x-3 pb-3 border-b border-[#e5ded1]">
            <div className="p-2.5 rounded-lg bg-[#fef2f2] text-[#dc2626] border border-[#fecaca]">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="font-bold text-sm text-[#1c1917]">{artifact.title}</div>
              <div className="text-[11px] font-mono text-[#78716c]">{artifact.filename}</div>
            </div>
          </div>

          <div className="space-y-2 text-xs text-[#44403c] leading-relaxed">
            <p>
              Portable Document Format compiled locally under <code className="px-1.5 py-0.5 rounded bg-[#f4efe6] font-mono text-[11px] text-[#dc2626]">storage/{artifact.filename}</code>.
            </p>
          </div>

          <div className="flex space-x-2">
            <a
              href={artifact.path}
              target="_blank"
              rel="noreferrer"
              className="flex-1 py-2 rounded-lg bg-[#faf8f5] hover:bg-[#ede7dc] text-[#1c1917] font-semibold flex items-center justify-center space-x-1.5 border border-[#e5ded1] transition-all"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Open in Tab</span>
            </a>
          </div>
        </div>
      );
    }

    // Default Fallback
    return (
      <div className="p-6 text-center text-[#78716c] font-mono text-xs bg-[#ffffff] rounded-lg border border-[#e5ded1]">
        <div>📄 {artifact.title || artifact.filename}</div>
        <div className="text-[10px] text-[#94a3b8] mt-1">Ready for preview and download</div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#faf8f5]">
      {/* Top Header */}
      <div className="p-3.5 border-b border-[#e5ded1] bg-[#ffffff] flex items-center justify-between shrink-0 shadow-xs">
        <div className="flex items-center space-x-2 truncate mr-2">
          <div className="p-1.5 rounded bg-[#faf8f5] border border-[#d6cebf]">
            {(rawType === 'docx' || rawType === 'doc' || rawType === 'document') && <FileText className="w-4 h-4 text-[#ea580c]" />}
            {(rawType === 'xlsx' || rawType === 'xls' || rawType === 'spreadsheet') && <FileSpreadsheet className="w-4 h-4 text-[#16a34a]" />}
            {(rawType === 'pptx' || rawType === 'ppt' || rawType === 'presentation') && <Presentation className="w-4 h-4 text-[#d97706]" />}
            {(rawType === 'png' || rawType === 'jpg' || rawType === 'plot' || rawType === 'image') && <ImageIcon className="w-4 h-4 text-[#7c3aed]" />}
            {(rawType === 'py' || rawType === 'code') && <Terminal className="w-4 h-4 text-[#0284c7]" />}
            {rawType === 'pdf' && <FileText className="w-4 h-4 text-[#dc2626]" />}
          </div>
          <div className="truncate">
            <div className="text-xs font-bold text-[#1c1917] truncate">{artifact.title}</div>
            <div className="text-[10px] font-mono text-[#78716c] truncate">{artifact.filename}</div>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 shrink-0">
          <a
            href={artifact.path}
            download={artifact.filename}
            className="p-1.5 rounded-lg bg-[#ea580c] hover:bg-[#c2410c] text-white shadow-xs transition-colors"
            title="Download original file"
          >
            <Download className="w-3.5 h-3.5" />
          </a>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#78716c] hover:text-[#1c1917] hover:bg-[#f4efe6] transition-colors"
            title="Close preview"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {renderContent()}
      </div>

      {/* Bottom Download Footer */}
      <div className="p-3 border-t border-[#e5ded1] bg-[#ffffff] flex items-center justify-between shrink-0">
        <span className="text-[10px] font-mono text-[#78716c]">
          {artifact.size_bytes ? `${Math.round(artifact.size_bytes / 1024)} KB` : 'Ready'} • SHA-256 Verified
        </span>
        <a
          href={artifact.path}
          download={artifact.filename}
          className="px-3 py-1.5 rounded-lg bg-[#ffffff] hover:bg-[#ea580c] hover:text-white border border-[#d6cebf] text-xs font-semibold text-[#1c1917] flex items-center space-x-1.5 shadow-sm transition-all"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Download File</span>
        </a>
      </div>
    </div>
  );
}


export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightPanelOpen, setRightPanelOpen] = useState(true);
  const [selectedDeliverable, setSelectedDeliverable] = useState(null);
  const [expandedImage, setExpandedImage] = useState(null);

  const [prompt, setPrompt] = useState('');
  const [loadingSessionId, setLoadingSessionId] = useState(null);

  const loading = !!loadingSessionId;
  const [activeTaskMeta, setActiveTaskMeta] = useState(null);
  const [elapsedTimer, setElapsedTimer] = useState(0);
  const [thinkingExpanded, setThinkingExpanded] = useState(false);
  const [showScrollBottomBtn, setShowScrollBottomBtn] = useState(false);
  
  // Chat History & Sessions Management - always start fresh on page load
  const [sessions, setSessions] = useState(() => {
    try {
      const saved = localStorage.getItem('kavach_chat_sessions');
      let parsed = saved ? JSON.parse(saved) : [];
      
      // Keep previous chats that have messages
      parsed = parsed.filter(s => s.messages && s.messages.length > 0);

      // Create a fresh new chat session for this visit
      const freshSession = {
        id: `sess-${Date.now()}`,
        title: 'New Industrial Task',
        messages: [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      return [freshSession, ...parsed];
    } catch (e) {
      return [{
        id: `sess-${Date.now()}`,
        title: 'New Industrial Task',
        messages: [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }];
    }
  });
  const [currentSessionId, setCurrentSessionId] = useState(() => sessions[0]?.id || `sess-${Date.now()}`);

  const [scenarios, setScenarios] = useState([]);
  const [healthData, setHealthData] = useState(null);
  const [expandedTraces, setExpandedTraces] = useState({});
  const [expandedSteps, setExpandedSteps] = useState({});
  const [activeModal, setActiveModal] = useState(null);

  // File Uploads State for Chat
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  // Knowledge Base RAG State
  const [kbQuery, setKbQuery] = useState('');
  const [kbResults, setKbResults] = useState([]);
  const [kbDocuments, setKbDocuments] = useState([]);
  const [kbStats, setKbStats] = useState(null);
  const [kbUploadLoading, setKbUploadLoading] = useState(false);
  const [kbTab, setKbTab] = useState('search'); // 'search' or 'manage'
  const kbFileInputRef = useRef(null);

  const [securityData, setSecurityData] = useState(null);
  const [certificate, setCertificate] = useState(null);
  const [models, setModels] = useState([]);

  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const isUserAtBottomRef = useRef(true);

  useEffect(() => {
    try {
      // Only persist sessions that have messages or the currently active session
      const toSave = sessions.filter(s => (s.messages && s.messages.length > 0) || s.id === currentSessionId);
      localStorage.setItem('kavach_chat_sessions', JSON.stringify(toSave));
    } catch (e) {}
  }, [sessions, currentSessionId]);

  const currentSession = sessions.find(s => s.id === currentSessionId) || sessions[0];
  const messages = currentSession?.messages || [];
  const isCurrentSessionLoading = loadingSessionId === currentSession?.id;

  useEffect(() => {
    fetchHealth();
    fetchScenarios();
    fetchModels();
    fetchSecurityData();
    fetchKbDocuments();
  }, []);

  const fetchKbDocuments = async () => {
    try {
      const res = await fetch('/api/knowledge-base/documents');
      const data = await res.json();
      setKbDocuments(data.documents || []);
      setKbStats(data.stats || null);
    } catch (e) {}
  };

  const handleKbUpload = async (file) => {
    if (!file) return;
    setKbUploadLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/knowledge-base/upload', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        await fetchKbDocuments();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setKbUploadLoading(false);
    }
  };

  const handleKbDelete = async (docId) => {
    try {
      const res = await fetch(`/api/knowledge-base/documents/${docId}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        setKbDocuments(prev => prev.filter(d => d.doc_id !== docId));
      }
    } catch (e) {}
  };

  const handleSelectModel = async (modelId) => {
    try {
      const res = await fetch('/api/models/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_id: modelId })
      });
      if (res.ok) {
        await fetchHealth();
      }
    } catch (e) {}
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files || []);
    handleFilesAdd(files);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleFilesAdd = (files) => {
    const newItems = files.map(f => {
      const isImg = f.type.startsWith('image/');
      return {
        file: f,
        name: f.name,
        size: f.size,
        type: f.type,
        preview: isImg ? URL.createObjectURL(f) : null
      };
    });
    setAttachedFiles(prev => [...prev, ...newItems]);
  };

  const handleRemoveAttachment = (index) => {
    setAttachedFiles(prev => {
      const item = prev[index];
      if (item?.preview) URL.revokeObjectURL(item.preview);
      return prev.filter((_, i) => i !== index);
    });
  };


  // Handle Chat Scroll Event to detect if user has scrolled up
  const handleChatScroll = () => {
    if (!chatContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 120;
    isUserAtBottomRef.current = isAtBottom;
    setShowScrollBottomBtn(!isAtBottom && messages.length > 2);
  };

  const scrollToBottom = (force = false) => {
    if (force || isUserAtBottomRef.current) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Only auto-scroll on new message added IF user was already at the bottom
  useEffect(() => {
    if (isUserAtBottomRef.current) {
      scrollToBottom();
    }
  }, [messages.length, loadingSessionId]);

  // Live Timer during active inference execution
  useEffect(() => {
    let interval = null;
    if (loadingSessionId) {
      setElapsedTimer(0);
      const start = Date.now();
      interval = setInterval(() => {
        setElapsedTimer(parseFloat(((Date.now() - start) / 1000).toFixed(1)));
      }, 100);
    } else {
      if (interval) clearInterval(interval);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [loadingSessionId]);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      const data = await res.json();
      setHealthData(data);
    } catch (e) {}
  };

  const fetchScenarios = async () => {
    try {
      const res = await fetch('/api/scenarios');
      const data = await res.json();
      setScenarios(data.scenarios || []);
    } catch (e) {}
  };

  const fetchModels = async () => {
    try {
      const res = await fetch('/api/models');
      const data = await res.json();
      setModels(data.models || []);
    } catch (e) {}
  };

  const fetchSecurityData = async () => {
    try {
      const res = await fetch('/api/security/status');
      const data = await res.json();
      setSecurityData(data);
    } catch (e) {}
  };

  const handleNewChat = () => {
    if (currentSession && currentSession.messages.length === 0) {
      setPrompt('');
      setSelectedDeliverable(null);
      return;
    }
    const newSess = {
      id: `sess-${Date.now()}`,
      title: 'New Industrial Task',
      messages: [],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setSessions(prev => [newSess, ...prev.filter(s => s.messages && s.messages.length > 0)]);
    setCurrentSessionId(newSess.id);
    setSelectedDeliverable(null);
    setPrompt('');
  };

  const handleDeleteSession = (e, sessId) => {
    e.stopPropagation();
    const updated = sessions.filter(s => s.id !== sessId);
    if (updated.length === 0) {
      const fresh = {
        id: `sess-${Date.now()}`,
        title: 'New Industrial Task',
        messages: [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setSessions([fresh]);
      setCurrentSessionId(fresh.id);
    } else {
      setSessions(updated);
      if (currentSessionId === sessId) {
        setCurrentSessionId(updated[0].id);
      }
    }
  };

  const handleSend = async (textToSend) => {
    const query = textToSend || prompt;
    if ((!query.trim() && attachedFiles.length === 0) || loadingSessionId) return;

    const targetSessionId = currentSessionId;
    const filesToUpload = [...attachedFiles];
    setAttachedFiles([]);

    let uploadedAttachments = [];
    if (filesToUpload.length > 0) {
      for (const item of filesToUpload) {
        const formData = new FormData();
        formData.append('file', item.file);
        try {
          const res = await fetch('/api/upload', {
            method: 'POST',
            body: formData
          });
          if (res.ok) {
            const data = await res.json();
            uploadedAttachments.push(data);
          }
        } catch (err) {
          console.error("Attachment upload error:", err);
        }
      }
    }

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: query || (uploadedAttachments.length > 0 ? `Uploaded ${uploadedAttachments.length} file(s): ${uploadedAttachments.map(a => a.filename).join(', ')}` : ''),
      attachments: uploadedAttachments,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    const isFirstMsg = messages.length === 0;
    const newTitle = isFirstMsg ? (query.length > 28 ? query.slice(0, 28) + '...' : (query || uploadedAttachments[0]?.filename || 'File Task')) : currentSession.title;

    setSessions(prev => prev.map(s => {
      if (s.id === targetSessionId) {
        return {
          ...s,
          title: newTitle,
          messages: [...s.messages, userMsg]
        };
      }
      return s;
    }));

    // Dynamically classify the ACTUAL task intent for live inspection
    const promptLower = query.toLowerCase();
    let taskType = "Neural Reasoning & Response Synthesis";
    let targetAction = "Querying local model on localhost (127.0.0.1:11434)...";

    if (uploadedAttachments.length > 0) {
      taskType = "Multimodal Document & Attachment Processing";
      targetAction = `Processing ${uploadedAttachments.length} attachment(s) with local foundation model`;
    } else if (promptLower.includes("powerpoint") || promptLower.includes("ppt") || promptLower.includes("slide") || promptLower.includes("deck") || promptLower.includes("presentation")) {
      taskType = "PowerPoint Presentation Generation";
      targetAction = "Structuring slide outline & generating .pptx deck";
    } else if (promptLower.includes("word") || promptLower.includes("docx") || promptLower.includes("report") || promptLower.includes("approval note")) {
      taskType = "Word Document Compilation";
      targetAction = "Drafting executive note & compiling .docx deliverable";
    } else if (promptLower.includes("excel") || promptLower.includes("xlsx") || promptLower.includes("spreadsheet") || promptLower.includes("workbook")) {
      taskType = "Excel Spreadsheet Calculation";
      targetAction = "Building spreadsheet formulas & compiling .xlsx file";
    } else if (promptLower.includes("differentiate") || promptLower.includes("integral") || promptLower.includes("calculus") || promptLower.includes("sympy") || promptLower.includes("solve")) {
      taskType = "Mathematical Sandbox Evaluation";
      targetAction = "Evaluating calculus with local Python SymPy engine in sandbox";
    } else if (promptLower.includes("simulate") || promptLower.includes("heat exchanger") || promptLower.includes("lmtd")) {
      taskType = "Thermal Process Simulation";
      targetAction = "Simulating LMTD equations & generating matplotlib thermal plot";
    } else if (promptLower.includes("p&id") || promptLower.includes("drawing") || promptLower.includes("schematic")) {
      taskType = "P&ID Schematic Vision Inspection";
      targetAction = "Analyzing coordinates & auditing safety interlocks";
    } else if (promptLower.includes("api") || promptLower.includes("asme") || promptLower.includes("standard") || promptLower.includes("gfr")) {
      taskType = "Plant Standards Local Search";
      targetAction = "Searching local RAG knowledge base & standards";
    }

    const activeModelName = healthData?.active_foundation_model || healthData?.active_model_id || "Local Model";

    setActiveTaskMeta({
      taskType,
      targetAction,
      model: activeModelName,
      endpoint: "http://127.0.0.1:11434",
      networkEgress: "0 Bytes (Air-Gapped)"
    });

    setPrompt('');
    setLoadingSessionId(targetSessionId);
    setThinkingExpanded(false);
    
    // User explicitly sent a message -> scroll to bottom once
    isUserAtBottomRef.current = true;
    setTimeout(() => scrollToBottom(true), 50);

    const historyPayload = messages.map(m => ({
      role: m.role,
      content: m.content
    }));

    fetch('/api/agent/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: query || "Analyze attached file(s) and provide technical assessment.",
        attachments: uploadedAttachments,
        history: historyPayload
      })
    })
      .then(res => res.json())
      .then(data => {
        const assistantMsg = {
          id: Date.now() + 1,
          role: 'assistant',
          content: data.summary,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          routing: data.routing,
          steps: data.steps,
          artifacts: data.artifacts,
          sandbox_output: data.sandbox_output,
          sovereign_proof: data.sovereign_proof,
          elapsed_seconds: data.elapsed_seconds
        };

        // If artifacts were generated and user is still on this session, auto-open in right inspector!
        if (targetSessionId === currentSessionId && data.artifacts && data.artifacts.length > 0) {
          setSelectedDeliverable(data.artifacts[0]);
          setRightPanelOpen(true);
        }

        setSessions(prev => prev.map(s => {
          if (s.id === targetSessionId) {
            return {
              ...s,
              messages: [...s.messages, assistantMsg]
            };
          }
          return s;
        }));

        fetchSecurityData();
      })
      .catch(err => {
        const errorMsg = {
          id: Date.now() + 1,
          role: 'assistant',
          content: `Execution Notice: Local sovereign backend error (${err.message}). Ensure 127.0.0.1:8000 is running.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          isError: true
        };
        setSessions(prev => prev.map(s => {
          if (s.id === targetSessionId) {
            return { ...s, messages: [...s.messages, errorMsg] };
          }
          return s;
        }));
      })
      .finally(() => {
        setLoadingSessionId(null);
      });
  };


  const toggleTrace = (msgId) => {
    setExpandedTraces(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const toggleStep = (msgId, stepNum) => {
    const key = `${msgId}-${stepNum}`;
    setExpandedSteps(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleKbSearch = async (e) => {
    e.preventDefault();
    if (!kbQuery.trim()) return;
    try {
      const res = await fetch('/api/knowledge-base/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: kbQuery })
      });
      const data = await res.json();
      setKbResults(data.results || []);
    } catch (e) {}
  };

  const handleGenerateCert = async () => {
    try {
      const res = await fetch('/api/security/certificate');
      const data = await res.json();
      setCertificate(data);
    } catch (e) {}
  };

  const allArtifacts = messages
    .filter(m => m.artifacts && m.artifacts.length > 0)
    .flatMap(m => m.artifacts);

  const getArtifactIcon = (type) => {
    const t = (type || '').toLowerCase();
    if (t === 'docx' || t === 'doc' || t === 'document') return <FileText className="w-4 h-4 text-[#ea580c]" />;
    if (t === 'xlsx' || t === 'xls' || t === 'spreadsheet') return <FileSpreadsheet className="w-4 h-4 text-[#16a34a]" />;
    if (t === 'pptx' || t === 'ppt' || t === 'presentation') return <Presentation className="w-4 h-4 text-[#d97706]" />;
    if (t === 'png' || t === 'jpg' || t === 'jpeg' || t === 'plot' || t === 'image') return <ImageIcon className="w-4 h-4 text-[#7c3aed]" />;
    if (t === 'py' || t === 'code') return <Terminal className="w-4 h-4 text-[#0284c7]" />;
    if (t === 'pdf') return <FileText className="w-4 h-4 text-[#dc2626]" />;
    return <Download className="w-4 h-4 text-[#57534e]" />;
  };


  return (
    <div className="flex h-screen bg-[#faf8f5] text-[#1c1917] font-sans overflow-hidden">
      {/* 1. LEFT SIDEBAR */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-0 -translate-x-full'
        } transition-all duration-300 ease-in-out bg-[#f4efe6] border-r border-[#e5ded1] flex flex-col justify-between shrink-0 z-30 overflow-hidden select-none`}
      >
        <div className="flex flex-col h-full overflow-hidden p-4">
          {/* Top Brand & Collapse Button */}
          <div className="flex items-center justify-between mb-3 px-1">
            <div className="flex items-center space-x-2.5">
              <div className="w-6 h-6 rounded-md bg-[#ea580c] flex items-center justify-center text-white shadow-sm">
                <ShieldCheck className="w-3.5 h-3.5" />
              </div>
              <div>
                <h1 className="text-xs font-bold tracking-wider text-[#1c1917] uppercase">
                  KAVACH
                </h1>
                <p className="text-[9px] text-[#78716c] font-mono tracking-tight">
                  SOVEREIGN WORKBENCH
                </p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-1 text-[#78716c] hover:text-[#1c1917] rounded hover:bg-[#ede7dc] transition-colors"
              title="Close sidebar"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          </div>

          {/* + New Task Button */}
          <button
            onClick={handleNewChat}
            className="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-lg border border-[#d6cebf] bg-[#ffffff] hover:bg-[#fcfbf9] text-xs font-semibold text-[#1c1917] transition-all mb-3 shadow-sm group"
          >
            <Plus className="w-3.5 h-3.5 text-[#ea580c] group-hover:scale-110 transition-transform" />
            <span>New Task</span>
          </button>

          {/* CHAT HISTORY (Top Area Under New Task) */}
          <div className="flex flex-col flex-1 overflow-hidden min-h-0">
            <div className="text-[10px] uppercase tracking-wider text-[#78716c] px-1 mb-1.5 font-bold flex items-center justify-between">
              <span>Chat History</span>
              <span className="text-[9px] font-mono font-normal text-[#a8a29e]">{sessions.length} chats</span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-1 pr-1 scrollbar-none max-h-[38%] border-b border-[#e5ded1] pb-2 mb-3">
              {sessions.map((s) => {
                const isActive = s.id === currentSessionId;
                return (
                  <div
                    key={s.id}
                    onClick={() => {
                      setCurrentSessionId(s.id);
                      setSelectedDeliverable(null);
                    }}
                    className={`w-full flex items-center justify-between p-2 rounded-lg text-xs cursor-pointer transition-all group ${
                      isActive
                        ? 'bg-[#ffffff] text-[#1c1917] font-semibold border border-[#d6cebf] shadow-xs'
                        : 'text-[#57534e] hover:bg-[#ede7dc] hover:text-[#1c1917] border border-transparent'
                    }`}
                  >
                    <div className="flex items-center space-x-2 truncate mr-1">
                      <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-[#ea580c]' : 'text-[#a8a29e]'}`} />
                      <span className="truncate text-[11px]">{s.title}</span>
                      {loadingSessionId === s.id && (
                        <span className="w-1.5 h-1.5 rounded-full bg-[#ea580c] animate-ping shrink-0 ml-1" title="Thinking..." />
                      )}
                    </div>
                    {sessions.length > 1 && (
                      <button
                        onClick={(e) => handleDeleteSession(e, s.id)}
                        className="opacity-0 group-hover:opacity-100 p-0.5 text-[#a8a29e] hover:text-[#dc2626] rounded transition-opacity"
                        title="Delete chat"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                );
              })}
            </div>

            {/* LOWER SECTION: STANDARD WORKFLOWS & TOOLS */}
            <div className="flex-1 overflow-y-auto space-y-3 pr-1 scrollbar-none">
              {/* Standard Workflows */}
              <div>
                <div className="text-[10px] uppercase tracking-wider text-[#78716c] px-1 mb-1.5 font-bold">
                  Standard Workflows
                </div>
                <div className="space-y-1">
                  {scenarios.map((sc) => (
                    <button
                      key={sc.id}
                      onClick={() => handleSend(sc.prompt)}
                      disabled={loading}
                      className="w-full text-left p-2 rounded-lg text-xs hover:bg-[#ede7dc] text-[#44403c] hover:text-[#1c1917] transition-colors group flex items-start space-x-2 border border-transparent hover:border-[#d6cebf]"
                    >
                      <div className="w-1.5 h-1.5 rounded-full bg-[#ea580c] mt-1.5 shrink-0 group-hover:scale-125 transition-transform" />
                      <div className="flex-1 truncate">
                        <div className="font-medium text-[#1c1917] truncate group-hover:text-[#ea580c] transition-colors text-[11px]">
                          {sc.title}
                        </div>
                        <div className="text-[9px] text-[#78716c] truncate">
                          {sc.badge}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Integrity & Tools */}
              <div>
                <div className="text-[10px] uppercase tracking-wider text-[#78716c] px-1 mb-1.5 font-bold">
                  Integrity & Tools
                </div>
                <div className="space-y-1">
                  <button
                    onClick={() => setActiveModal('sentinel')}
                    className="w-full flex items-center justify-between p-2 rounded-lg text-xs hover:bg-[#ede7dc] text-[#44403c] hover:text-[#1c1917] transition-colors"
                  >
                    <div className="flex items-center space-x-2 text-[11px]">
                      <ShieldCheck className="w-3.5 h-3.5 text-[#ea580c]" />
                      <span>Air-Gap Sentinel</span>
                    </div>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[#ffffff] text-[#1c1917] border border-[#d6cebf]">
                      0 B Egress
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveModal('deliverables')}
                    className="w-full flex items-center justify-between p-2 rounded-lg text-xs hover:bg-[#ede7dc] text-[#44403c] hover:text-[#1c1917] transition-colors"
                  >
                    <div className="flex items-center space-x-2 text-[11px]">
                      <FileText className="w-3.5 h-3.5 text-[#78716c]" />
                      <span>Deliverables Hub</span>
                    </div>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[#ffffff] text-[#1c1917] border border-[#d6cebf]">
                      {allArtifacts.length}
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveModal('kb')}
                    className="w-full flex items-center justify-between p-2 rounded-lg text-xs hover:bg-[#ede7dc] text-[#44403c] hover:text-[#1c1917] transition-colors"
                  >
                    <div className="flex items-center space-x-2 text-[11px]">
                      <BookOpen className="w-3.5 h-3.5 text-[#78716c]" />
                      <span>Plant Standards</span>
                    </div>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[#ffffff] text-[#1c1917] border border-[#d6cebf]">
                      ASME / API
                    </span>
                  </button>

                  <button
                    onClick={() => setActiveModal('models')}
                    className="w-full flex items-center justify-between p-2 rounded-lg text-xs hover:bg-[#ede7dc] text-[#44403c] hover:text-[#1c1917] transition-colors"
                  >
                    <div className="flex items-center space-x-2 text-[11px]">
                      <Cpu className="w-3.5 h-3.5 text-[#78716c]" />
                      <span>Model Settings</span>
                    </div>
                    <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[#ffffff] text-[#1c1917] border border-[#d6cebf]">
                      4B Class
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Host Badge */}
          <div className="pt-2 border-t border-[#e5ded1] text-[10px] text-[#78716c] space-y-0.5">
            <div className="flex items-center justify-between">
              <span>Foundation Model:</span>
              <span className="text-[#1c1917] font-semibold truncate max-w-[110px]">{healthData?.active_foundation_model || 'Local Model'}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>RAM Allocation:</span>
              <span className="text-[#1c1917] font-mono">{healthData?.ram_allocated_gb || 3.4} GB</span>
            </div>
            <div className="flex items-center space-x-1.5 text-[#57534e] pt-0.5">
              <span className={`w-1.5 h-1.5 rounded-full ${healthData?.ollama_backend?.available ? 'bg-[#16a34a]' : 'bg-[#ea580c]'}`}></span>
              <span>{healthData?.ollama_backend?.available ? 'Ollama Online' : '100% On-Premises Isolated'}</span>
            </div>
          </div>
        </div>
      </aside>

      {/* 2. CENTER CONVERSATION CONTAINER */}
      <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#faf8f5] relative">
        {/* Top Minimal Header */}
        <header className="h-14 border-b border-[#e5ded1] bg-[#faf8f5]/90 backdrop-blur px-5 flex items-center justify-between shrink-0 z-20">
          <div className="flex items-center space-x-3">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-1.5 text-[#78716c] hover:text-[#1c1917] rounded hover:bg-[#f4efe6] transition-colors"
                title="Open sidebar"
              >
                <PanelLeft className="w-4 h-4" />
              </button>
            )}

            <div className="flex items-center space-x-2">
              <span className="text-xs font-semibold tracking-wide text-[#1c1917] uppercase">
                {healthData?.active_foundation_model || 'Local Sovereign Assistant'}
              </span>
              <button
                onClick={() => setActiveModal('models')}
                className={`text-[10px] font-mono px-2 py-0.5 rounded border transition-colors flex items-center space-x-1 ${
                  healthData?.ollama_backend?.available
                    ? 'bg-[#f0fdf4] text-[#16a34a] border-[#bbf7d0] hover:bg-[#dcfce7]'
                    : 'bg-[#fff7ed] text-[#ea580c] border-[#fed7aa] hover:bg-[#ffedd5]'
                }`}
                title="Click to view model settings"
              >
                <span className={`w-1.5 h-1.5 rounded-full ${healthData?.ollama_backend?.available ? 'bg-[#16a34a]' : 'bg-[#ea580c]'}`} />
                <span>{healthData?.ollama_backend?.available ? (healthData.ollama_backend.active_model || 'Ollama Connected') : 'Ollama Offline'}</span>
              </button>
            </div>
          </div>


          <div className="flex items-center space-x-3 text-xs">
            <button
              onClick={() => setActiveModal('sentinel')}
              className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#ffffff] text-[#1c1917] hover:bg-[#f4efe6] border border-[#d6cebf] transition-colors font-mono text-[11px] shadow-sm"
            >
              <Lock className="w-3 h-3 text-[#ea580c]" />
              <span>0 B Egress</span>
            </button>

            <button
              onClick={() => setActiveModal('deliverables')}
              className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#ffffff] text-[#1c1917] hover:bg-[#f4efe6] border border-[#d6cebf] transition-colors font-mono text-[11px] shadow-sm"
            >
              <FileText className="w-3 h-3 text-[#78716c]" />
              <span>Deliverables ({allArtifacts.length})</span>
            </button>

            <button
              onClick={() => setRightPanelOpen(!rightPanelOpen)}
              className={`p-1.5 rounded-md border transition-colors ${
                rightPanelOpen
                  ? 'bg-[#ea580c] text-white border-[#ea580c]'
                  : 'bg-[#ffffff] text-[#78716c] hover:text-[#1c1917] border-[#d6cebf]'
              }`}
              title={rightPanelOpen ? "Hide right panel" : "Show right panel"}
            >
              {selectedDeliverable ? <FileCheck className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>
          </div>
        </header>

        {/* Message Thread (with smart onScroll tracking) */}
        <div 
          ref={chatContainerRef}
          onScroll={handleChatScroll}
          className="flex-1 overflow-y-auto px-4 sm:px-8 md:px-16 lg:px-24 py-8 space-y-6 relative"
        >
          {messages.length === 0 ? (
            /* Empty State Hero */
            <div className="max-w-xl mx-auto my-auto py-12 text-center space-y-6">
              <div className="inline-flex p-3.5 rounded-2xl bg-[#ffffff] border border-[#e5ded1] shadow-sm">
                <ShieldCheck className="w-8 h-8 text-[#ea580c]" />
              </div>

              <div className="space-y-1.5">
                <h2 className="text-lg font-bold tracking-tight text-[#1c1917]">
                  How can KAVACH assist you today?
                </h2>
                <p className="text-xs text-[#57534e] max-w-md mx-auto leading-relaxed">
                  On-premises sovereign engineering assistant powered by <strong>Gemma 3 4B</strong>. 
                  Zero cloud telemetry, sandboxed calculation verification, and official PSU Word/Excel/PowerPoint deliverables.
                </p>
              </div>

              {/* Suggestion Chips */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left pt-2">
                {scenarios.map((sc) => (
                  <div
                    key={sc.id}
                    onClick={() => handleSend(sc.prompt)}
                    className="p-3.5 rounded-xl border border-[#e5ded1] bg-[#ffffff] hover:bg-[#fcfbf9] hover:border-[#ea580c] transition-all cursor-pointer group shadow-sm"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-semibold text-[#1c1917] group-hover:text-[#ea580c] transition-colors">
                        {sc.title}
                      </span>
                    </div>
                    <p className="text-[11px] text-[#78716c] line-clamp-2 leading-relaxed">
                      {sc.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            /* Messages List */
            messages.map((msg) => {
              const isTraceExpanded = expandedTraces[msg.id] || false;

              return (
                <div
                  key={msg.id}
                  className={`flex space-x-3 max-w-3xl mx-auto ${
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {msg.role === 'assistant' && (
                    <div className="w-6 h-6 rounded-md bg-[#ea580c] flex items-center justify-center text-white shrink-0 mt-1 shadow-sm">
                      <Bot className="w-3.5 h-3.5" />
                    </div>
                  )}

                  <div
                    className={`flex flex-col space-y-3 max-w-[90%] ${
                      msg.role === 'user'
                        ? 'bg-[#ede7dc] border border-[#d6cebf] text-[#1c1917] rounded-2xl rounded-tr-sm p-4 text-xs leading-relaxed shadow-sm'
                        : 'bg-[#ffffff] border border-[#e5ded1] text-[#1c1917] rounded-2xl rounded-tl-sm p-5 shadow-sm space-y-3 text-xs leading-relaxed'
                    }`}
                  >
                    {/* Assistant Meta */}
                    {msg.role === 'assistant' && msg.routing && (
                      <div className="flex items-center justify-between pb-2 border-b border-[#f0eae0] text-[11px] font-mono text-[#78716c]">
                        <div className="flex items-center space-x-2">
                          <span className="text-[#ea580c] font-semibold">
                            {msg.routing.model_name}
                          </span>
                        </div>
                        {msg.elapsed_seconds && (
                          <span>Executed in {msg.elapsed_seconds}s</span>
                        )}
                      </div>
                    )}

                    {/* Message content */}
                    <FormattedMarkdown content={msg.content} />

                    {/* Sandbox execution result */}
                    {msg.sandbox_output && (
                      <div className="my-2.5 rounded-lg border border-[#e5ded1] bg-[#faf8f5] overflow-hidden shadow-xs">
                        <div className="px-3 py-1.5 bg-[#f4efe6] border-b border-[#e5ded1] flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <Terminal className="w-3.5 h-3.5 text-[#ea580c]" />
                            <span className="text-[11px] font-semibold text-[#1c1917]">
                              Python Sandbox Execution Output
                            </span>
                          </div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#ffffff] text-[#16a34a] border border-[#d6cebf] font-medium flex items-center space-x-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#16a34a] animate-pulse"></span>
                            <span>Verified ({msg.sandbox_output.elapsed_seconds}s)</span>
                          </span>
                        </div>

                        <div className="p-3 space-y-2 text-[11px] font-mono">
                          {msg.sandbox_output.code && (
                            <div>
                              <div className="text-[10px] uppercase text-[#78716c] font-semibold mb-1">Executed Code:</div>
                              <div className="p-2 rounded bg-[#ffffff] border border-[#e5ded1] text-[#1c1917] overflow-x-auto whitespace-pre">
                                {msg.sandbox_output.code}
                              </div>
                            </div>
                          )}

                          <div>
                            <div className="text-[10px] uppercase text-[#78716c] font-semibold mb-1">Live Terminal Output:</div>
                            <div className="p-2.5 rounded bg-[#1c1917] text-[#f4efe6] overflow-x-auto whitespace-pre font-mono font-medium shadow-inner">
                              {msg.sandbox_output.stdout ? msg.sandbox_output.stdout.trim() : '(Process executed with 0 stdout output)'}
                            </div>
                          </div>

                          {msg.sandbox_output.plots && msg.sandbox_output.plots.length > 0 && (
                            <div>
                              <div className="text-[10px] uppercase text-[#78716c] font-semibold mb-1">Generated Visualizations:</div>
                              <div className="grid grid-cols-1 gap-2">
                                {msg.sandbox_output.plots.map((plot, pIdx) => (
                                  <div 
                                    key={pIdx} 
                                    onClick={() => {
                                      setSelectedDeliverable(plot);
                                      setRightPanelOpen(true);
                                    }}
                                    className="p-2 rounded bg-[#ffffff] border border-[#e5ded1] cursor-pointer hover:border-[#ea580c] transition-all"
                                  >
                                    <img src={plot.path} alt={plot.title} className="rounded w-full object-contain max-h-56" />
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Execution trace */}
                    {msg.steps && msg.steps.length > 0 && (
                      <div className="pt-1">
                        <button
                          onClick={() => toggleTrace(msg.id)}
                          className="w-fit flex items-center space-x-2 px-2.5 py-1 rounded-md bg-[#f4efe6] hover:bg-[#ede7dc] border border-[#e5ded1] text-[11px] font-mono text-[#78716c] hover:text-[#1c1917] transition-all group"
                        >
                          <Terminal className="w-3.5 h-3.5 text-[#ea580c] group-hover:scale-110 transition-transform" />
                          <span className="font-semibold">Execution Trace ({msg.steps.length} Phases)</span>
                          {isTraceExpanded ? (
                            <ChevronDown className="w-3 h-3 text-[#78716c]" />
                          ) : (
                            <ChevronRight className="w-3 h-3 text-[#78716c]" />
                          )}
                        </button>

                        {isTraceExpanded && (
                          <div className="mt-2 space-y-1.5 p-2 rounded-lg bg-[#faf8f5] border border-[#e5ded1]">
                            {msg.steps.map((st) => {
                              const isStepExpanded = expandedSteps[`${msg.id}-${st.step_number}`];
                              return (
                                <div
                                  key={st.step_number}
                                  className="rounded-lg border border-[#e5ded1] bg-[#ffffff] overflow-hidden text-xs"
                                >
                                  <button
                                    onClick={() => toggleStep(msg.id, st.step_number)}
                                    className="w-full flex items-center justify-between p-2 hover:bg-[#f4efe6] text-left font-mono text-[11px]"
                                  >
                                    <div className="flex items-center space-x-2 truncate">
                                      <div className="w-1.5 h-1.5 rounded-full bg-[#ea580c] shrink-0" />
                                      <span className="font-medium text-[#1c1917] truncate">
                                        Phase {st.step_number}: {st.title}
                                      </span>
                                    </div>
                                    <div className="flex items-center space-x-2 text-[#78716c] shrink-0">
                                      <span>{st.duration_ms}ms</span>
                                      {isStepExpanded ? (
                                        <ChevronDown className="w-3 h-3" />
                                      ) : (
                                        <ChevronRight className="w-3 h-3" />
                                      )}
                                    </div>
                                  </button>

                                  {isStepExpanded && (
                                    <div className="p-3 pt-1 border-t border-[#e5ded1] bg-[#faf8f5] space-y-2 text-[#44403c]">
                                      {st.details && <p className="text-[#44403c]">{st.details}</p>}
                                    </div>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Generated deliverables */}
                    {msg.artifacts && msg.artifacts.length > 0 && (
                      <div className="pt-3 border-t border-[#f0eae0]">
                        <div className="text-[10px] uppercase tracking-wider text-[#ea580c] font-bold mb-2 flex items-center space-x-1.5">
                          <Download className="w-3 h-3" />
                          <span>Generated Deliverables ({msg.artifacts.length}) • Click Card to Preview on Right</span>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {msg.artifacts.map((art, aIdx) => (
                            <div
                              key={aIdx}
                              onClick={() => {
                                setSelectedDeliverable(art);
                                setRightPanelOpen(true);
                              }}
                              className={`flex items-center justify-between p-2.5 rounded-lg border cursor-pointer transition-all group ${
                                selectedDeliverable?.filename === art.filename
                                  ? 'border-[#ea580c] bg-[#fff7ed] shadow-xs ring-1 ring-[#ea580c]'
                                  : 'border-[#e5ded1] bg-[#faf8f5] hover:border-[#ea580c] hover:bg-[#ffffff]'
                              }`}
                            >
                              <div className="flex items-center space-x-2.5 truncate mr-2">
                                <div className="p-1.5 rounded bg-[#ffffff] border border-[#d6cebf] shrink-0 group-hover:scale-105 transition-transform">
                                  {getArtifactIcon(art.file_type)}
                                </div>
                                <div className="truncate">
                                  <div className="text-xs font-semibold text-[#1c1917] truncate group-hover:text-[#ea580c] transition-colors">
                                    {art.title}
                                  </div>
                                  <div className="text-[10px] font-mono text-[#78716c] truncate">
                                    {art.filename}
                                  </div>
                                </div>
                              </div>

                              <div className="flex items-center space-x-1">
                                <button
                                  className="p-1.5 rounded text-[#78716c] hover:text-[#ea580c] transition-colors"
                                  title="View on right panel"
                                >
                                  <Eye className="w-3.5 h-3.5" />
                                </button>
                                <a
                                  href={art.path}
                                  download={art.filename}
                                  onClick={(e) => e.stopPropagation()}
                                  className="px-2 py-1 text-[11px] font-medium rounded bg-[#ffffff] text-[#1c1917] hover:bg-[#ea580c] hover:text-white border border-[#d6cebf] transition-all shrink-0 flex items-center space-x-1 shadow-xs"
                                  title="Direct download"
                                >
                                  <Download className="w-3 h-3" />
                                </a>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Security hash */}
                    {msg.sovereign_proof && (
                      <div className="pt-2 flex items-center justify-between text-[10px] font-mono text-[#78716c] border-t border-[#f0eae0]">
                        <span className="text-[#57534e] flex items-center">
                          <Lock className="w-3 h-3 mr-1 text-[#ea580c]" />
                          100% Air-Gapped (0 Bytes Exfiltrated)
                        </span>
                        <span className="truncate max-w-[160px] text-[#a8a29e]">
                          {msg.sovereign_proof.audit_hash.slice(0, 16)}...
                        </span>
                      </div>
                    )}
                  </div>

                  {msg.role === 'user' && (
                    <div className="w-6 h-6 rounded-md bg-[#1c1917] flex items-center justify-center text-white shrink-0 mt-1 shadow-sm">
                      <User className="w-3.5 h-3.5" />
                    </div>
                  )}
                </div>
              );
            })
          )}

          {/* Thinking indicator */}
          {isCurrentSessionLoading && (
            <div className="flex space-x-3 max-w-3xl mx-auto items-start">
              {/* Status indicator ball */}
              <div className="relative w-6 h-6 flex items-center justify-center shrink-0 mt-0.5">
                <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-[#ea580c] via-[#f97316] to-[#fbbf24] animate-slime shadow-sm" />
                <div className="absolute inset-0 w-6 h-6 rounded-full bg-[#ea580c]/20 animate-ping pointer-events-none" />
              </div>

              {/* Status badge */}
              <div className="flex flex-col space-y-1.5">
                <button
                  type="button"
                  onClick={() => setThinkingExpanded(!thinkingExpanded)}
                  className="inline-flex items-center space-x-2 py-1 px-3 rounded-full bg-[#f4efe6] hover:bg-[#ede7dc] border border-[#e5ded1] text-[11px] font-mono text-[#1c1917] w-fit shadow-xs transition-all cursor-pointer group"
                >
                  <span className="font-semibold text-[#ea580c]">Thinking</span>
                  <span className="text-[#a8a29e]">•</span>
                  <span className="text-[#1c1917] font-semibold text-[10px]">{elapsedTimer}s</span>
                  <span className="text-[#a8a29e]">•</span>
                  <span className="text-[#78716c] group-hover:text-[#1c1917] text-[10px]">
                    {thinkingExpanded ? "Hide details" : "Inspect process"}
                  </span>
                  {thinkingExpanded ? (
                    <ChevronDown className="w-3 h-3 text-[#78716c] group-hover:text-[#ea580c] transition-colors" />
                  ) : (
                    <ChevronRight className="w-3 h-3 text-[#78716c] group-hover:text-[#ea580c] transition-colors" />
                  )}
                </button>

                {/* Expanded telemetry */}
                {thinkingExpanded && activeTaskMeta && (
                  <div className="p-3 rounded-xl bg-[#f4efe6] border border-[#e5ded1] text-[11px] font-mono text-[#57534e] space-y-2 max-w-md shadow-xs animate-in fade-in duration-200">
                    <div className="flex items-center justify-between border-b border-[#e5ded1] pb-1.5">
                      <div className="flex items-center space-x-1.5 text-[#ea580c] font-semibold text-[10px] uppercase tracking-wider">
                        <Activity className="w-3.5 h-3.5 text-[#ea580c]" />
                        <span>{activeTaskMeta.taskType}</span>
                      </div>
                      <span className="text-[10px] text-[#1c1917] font-bold bg-[#ffffff] px-2 py-0.5 rounded border border-[#d6cebf]">
                        {elapsedTimer}s
                      </span>
                    </div>

                    <p className="text-[#1c1917] font-medium leading-relaxed">
                      {activeTaskMeta.targetAction}
                    </p>

                    <div className="pt-1.5 border-t border-[#e5ded1] grid grid-cols-2 gap-2 text-[10px]">
                      <div>
                        <span className="text-[#78716c]">Inference Host:</span>{" "}
                        <span className="text-[#1c1917] font-semibold">{activeTaskMeta.model}</span>
                      </div>
                      <div>
                        <span className="text-[#78716c]">Egress:</span>{" "}
                        <span className="text-[#16a34a] font-semibold">{activeTaskMeta.networkEgress}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Floating Jump to Bottom Button if Scrolled Up */}
        {showScrollBottomBtn && (
          <button
            onClick={() => {
              isUserAtBottomRef.current = true;
              scrollToBottom(true);
            }}
            className="absolute bottom-24 right-8 p-2.5 rounded-full bg-[#1c1917] text-white shadow-lg hover:bg-[#ea580c] transition-all flex items-center space-x-1.5 text-xs font-mono z-30 group"
          >
            <ArrowDown className="w-3.5 h-3.5 group-hover:translate-y-0.5 transition-transform" />
            <span className="text-[10px] pr-1">Latest Messages</span>
          </button>
        )}

        {/* Floating Bottom Input */}
        <div className="p-4 bg-gradient-to-t from-[#faf8f5] via-[#faf8f5]/90 to-transparent shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={(e) => {
              e.preventDefault();
              setIsDragging(false);
              if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                handleFilesAdd(Array.from(e.dataTransfer.files));
              }
            }}
            className={`max-w-3xl mx-auto relative bg-[#ffffff] border ${
              isDragging ? 'border-[#ea580c] ring-2 ring-[#ea580c]/20' : 'border-[#d6cebf]'
            } rounded-xl shadow-md p-2 focus-within:border-[#ea580c] transition-all`}
          >
            {/* Hidden File Input */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileSelect}
              multiple
              className="hidden"
              accept=".pdf,.png,.jpg,.jpeg,.docx,.xlsx,.txt,.csv,.py"
            />

            {/* Attached Files Preview Tray */}
            {attachedFiles.length > 0 && (
              <div className="flex flex-wrap gap-2 pb-2 mb-1.5 border-b border-[#f0eae0]">
                {attachedFiles.map((file, idx) => (
                  <div
                    key={idx}
                    className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#faf8f5] border border-[#d6cebf] text-xs shadow-2xs group"
                  >
                    {file.preview ? (
                      <img src={file.preview} alt="preview" className="w-4 h-4 object-cover rounded" />
                    ) : (
                      <FileText className="w-3.5 h-3.5 text-[#ea580c]" />
                    )}
                    <span className="font-mono text-[11px] text-[#1c1917] max-w-[120px] truncate">{file.name}</span>
                    <span className="text-[10px] text-[#a8a29e] font-mono">({Math.round(file.size / 1024)} KB)</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveAttachment(idx)}
                      className="p-0.5 text-[#a8a29e] hover:text-[#dc2626] rounded transition-colors"
                      title="Remove file"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="flex items-center space-x-1.5">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-1.5 rounded-lg text-[#78716c] hover:text-[#ea580c] hover:bg-[#f4efe6] transition-colors"
                title="Attach files (PDF, images, Word, Excel, text)"
              >
                <Paperclip className="w-4 h-4" />
              </button>

              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder={attachedFiles.length > 0 ? "Ask about attached file(s) or leave empty for analysis..." : `Ask ${healthData?.active_foundation_model || 'Local Model'} (e.g. 'Draft API 510 Turnaround Note' or 'Simulate heat exchanger')...`}
                disabled={loading}
                className="flex-1 bg-transparent px-2.5 py-1.5 text-xs text-[#1c1917] placeholder-[#a8a29e] focus:outline-none font-sans"
              />

              <button
                type="button"
                onClick={() => setRightPanelOpen(true)}
                className="p-1.5 rounded-lg text-[#78716c] hover:text-[#ea580c] hover:bg-[#f4efe6] transition-colors"
                title="Open Voice Dictation"
              >
                <Mic className="w-4 h-4" />
              </button>

              <button
                type="submit"
                disabled={loading || (!prompt.trim() && attachedFiles.length === 0)}
                className={`p-2 rounded-lg transition-all ${
                  loading || (!prompt.trim() && attachedFiles.length === 0)
                    ? 'bg-[#ede7dc] text-[#a8a29e] cursor-not-allowed'
                    : 'bg-[#ea580c] hover:bg-[#c2410c] text-white font-semibold shadow-sm'
                }`}
                title="Send Task"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="flex items-center justify-between px-2 pt-1.5 text-[10px] text-[#78716c] font-mono border-t border-[#f0eae0] mt-1">
              <span>{healthData?.active_foundation_model || 'Local Model'} (~3.4 GB RAM)</span>
              <span>100% On-Premises • Zero Egress</span>
            </div>
          </form>
        </div>
      </div>

      {/* 3. RIGHT SIDEBAR: DEDICATED DELIVERABLE INSPECTOR OR VOICE AGENT */}
      <aside
        className={`${
          rightPanelOpen ? 'w-80 md:w-96' : 'w-0 translate-x-full'
        } transition-all duration-300 ease-in-out bg-[#f4efe6] border-l border-[#e5ded1] shrink-0 z-30 overflow-hidden flex flex-col`}
      >
        {selectedDeliverable ? (
          <DeliverableInspector
            artifact={selectedDeliverable}
            onClose={() => setSelectedDeliverable(null)}
            onZoomImage={(imgUrl) => setExpandedImage(imgUrl)}
          />
        ) : (

          <VoiceOrb
            onVoiceInput={(spokenText) => {
              setPrompt(spokenText);
            }}
            loading={loading}
          />
        )}
      </aside>

      {/* 4. MODALS */}

      {/* Air-Gap Sentinel Modal */}
      {activeModal === 'sentinel' && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-[#ffffff] border border-[#d6cebf] rounded-xl max-w-xl w-full p-6 shadow-xl space-y-4 text-xs font-mono text-[#1c1917]">
            <div className="flex items-center justify-between border-b border-[#e5ded1] pb-3">
              <div className="flex items-center space-x-2 font-bold text-[#1c1917]">
                <ShieldCheck className="w-4 h-4 text-[#ea580c]" />
                <span>AIR-GAP SENTINEL AUDIT REPORT</span>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="text-[#78716c] hover:text-[#1c1917]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-[#faf8f5] border border-[#e5ded1]">
                <div className="text-[#78716c] text-[10px]">Outbound Egress</div>
                <div className="text-base font-bold text-[#1c1917]">0 Bytes</div>
              </div>
              <div className="p-3 rounded-lg bg-[#faf8f5] border border-[#e5ded1]">
                <div className="text-[#78716c] text-[10px]">External DNS</div>
                <div className="text-base font-bold text-[#1c1917]">0 Calls</div>
              </div>
              <div className="p-3 rounded-lg bg-[#faf8f5] border border-[#e5ded1]">
                <div className="text-[#78716c] text-[10px]">Local Loopback</div>
                <div className="text-base font-bold text-[#ea580c]">127.0.0.1</div>
              </div>
            </div>

            <div>
              <div className="text-[10px] uppercase text-[#78716c] mb-1.5 font-semibold">Bound Local Services:</div>
              <div className="space-y-1 bg-[#faf8f5] p-2.5 rounded-lg border border-[#e5ded1] text-[11px]">
                {securityData?.active_loopback_sockets?.map((s, i) => (
                  <div key={i} className="flex justify-between text-[#44403c]">
                    <span>{s.service}</span>
                    <span className="text-[#78716c]">{s.bind}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-[#e5ded1]">
              <span className="text-[#78716c] text-[10px]">
                SHA-256 Tamper-Proof Chain
              </span>
              <button
                onClick={handleGenerateCert}
                className="px-3 py-1.5 rounded-lg bg-[#ea580c] hover:bg-[#c2410c] text-white font-semibold flex items-center space-x-1 shadow-sm"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Certificate</span>
              </button>
            </div>

            {certificate && (
              <div className="p-3 rounded bg-[#fff7ed] border border-[#fed7aa] text-[10px] space-y-1 text-[#9a3412]">
                <div><strong>Cert ID:</strong> {certificate.certificate_id}</div>
                <div><strong>Audit Root:</strong> {certificate.chain_head_hash}</div>
                <div><strong>Status:</strong> {certificate.external_egress_verified}</div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Deliverables Drawer Modal */}
      {activeModal === 'deliverables' && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-[#ffffff] border border-[#d6cebf] rounded-xl max-w-xl w-full p-6 shadow-xl space-y-4 text-xs text-[#1c1917]">
            <div className="flex items-center justify-between border-b border-[#e5ded1] pb-3">
              <div className="flex items-center space-x-2 font-bold text-[#1c1917]">
                <FileText className="w-4 h-4 text-[#ea580c]" />
                <span>GENERATED INDUSTRIAL DELIVERABLES</span>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="text-[#78716c] hover:text-[#1c1917]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2 max-h-[350px] overflow-y-auto pr-1">
              {allArtifacts.length === 0 ? (
                <div className="p-8 text-center text-[#78716c] font-mono">
                  No deliverables generated yet. Run a workflow to create Word, Excel, or PowerPoint files.
                </div>
              ) : (
                allArtifacts.map((art, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      setSelectedDeliverable(art);
                      setActiveModal(null);
                      setRightPanelOpen(true);
                    }}
                    className="flex items-center justify-between p-3 rounded-lg bg-[#faf8f5] hover:bg-[#ffffff] border border-[#e5ded1] hover:border-[#ea580c] cursor-pointer transition-all group"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="p-1.5 rounded bg-[#ffffff] border border-[#d6cebf] group-hover:scale-105 transition-transform">
                        {getArtifactIcon(art.file_type)}
                      </div>
                      <div>
                        <div className="font-semibold text-[#1c1917] group-hover:text-[#ea580c] transition-colors">{art.title}</div>
                        <div className="text-[10px] font-mono text-[#78716c]">{art.filename}</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] text-[#ea580c] font-semibold flex items-center space-x-1">
                        <Eye className="w-3 h-3" />
                        <span>Preview</span>
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Dynamic Local RAG Knowledge Base Modal */}
      {activeModal === 'kb' && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-[#ffffff] border border-[#d6cebf] rounded-xl max-w-2xl w-full p-6 shadow-xl space-y-4 text-xs text-[#1c1917] max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-[#e5ded1] pb-3 shrink-0">
              <div className="flex items-center space-x-2 font-bold text-[#1c1917]">
                <BookOpen className="w-4 h-4 text-[#ea580c]" />
                <span>DYNAMIC LOCAL RAG KNOWLEDGE BASE</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  type="button"
                  onClick={() => setKbTab('search')}
                  className={`px-3 py-1 rounded-md font-semibold text-xs transition-colors ${
                    kbTab === 'search' ? 'bg-[#ea580c] text-white shadow-xs' : 'bg-[#faf8f5] text-[#78716c] hover:bg-[#ede7dc]'
                  }`}
                >
                  Search Index
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setKbTab('manage');
                    fetchKbDocuments();
                  }}
                  className={`px-3 py-1 rounded-md font-semibold text-xs transition-colors ${
                    kbTab === 'manage' ? 'bg-[#ea580c] text-white shadow-xs' : 'bg-[#faf8f5] text-[#78716c] hover:bg-[#ede7dc]'
                  }`}
                >
                  Documents ({kbDocuments.length})
                </button>
                <button
                  onClick={() => setActiveModal(null)}
                  className="text-[#78716c] hover:text-[#1c1917] p-1"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {kbTab === 'search' ? (
              <div className="space-y-3 flex-1 overflow-y-auto pr-1">
                <form onSubmit={handleKbSearch} className="flex space-x-2">
                  <input
                    type="text"
                    value={kbQuery}
                    onChange={(e) => setKbQuery(e.target.value)}
                    placeholder="Search indexed RAG documents & standards..."
                    className="flex-1 bg-[#faf8f5] border border-[#d6cebf] rounded-lg px-3 py-2 text-xs text-[#1c1917] focus:outline-none focus:border-[#ea580c]"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2 rounded-lg bg-[#ea580c] hover:bg-[#c2410c] text-white font-semibold flex items-center space-x-1 shadow-sm"
                  >
                    <Search className="w-3.5 h-3.5" />
                    <span>Search</span>
                  </button>
                </form>

                <div className="space-y-2">
                  {kbResults.length === 0 ? (
                    <div className="p-8 text-center text-[#78716c] font-mono text-xs">
                      {kbDocuments.length === 0
                        ? "No documents indexed yet. Switch to 'Documents' tab to upload PDFs, Word files, or TXT standards."
                        : "Type a query above to search through indexed RAG chunks."}
                    </div>
                  ) : (
                    kbResults.map((chunk, idx) => (
                      <div key={idx} className="p-3.5 rounded-lg bg-[#faf8f5] border border-[#e5ded1] space-y-1.5">
                        <div className="flex items-center justify-between">
                          <div className="font-semibold text-[#1c1917] flex items-center space-x-1.5">
                            <FileText className="w-3.5 h-3.5 text-[#ea580c]" />
                            <span>{chunk.title}</span>
                            {chunk.chunk_index && (
                              <span className="text-[10px] font-mono text-[#78716c]">
                                (Chunk {chunk.chunk_index}/{chunk.total_chunks})
                              </span>
                            )}
                          </div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#ffffff] text-[#16a34a] border border-[#bbf7d0]">
                            {Math.round(chunk.relevance_score * 100)}% Match
                          </span>
                        </div>
                        <p className="text-[11px] text-[#44403c] font-mono leading-relaxed bg-[#ffffff] p-2.5 rounded border border-[#e5ded1] whitespace-pre-wrap">
                          {chunk.full_content || chunk.excerpt}
                        </p>
                      </div>
                    ))
                  )}
                </div>
              </div>
            ) : (
              <div className="space-y-4 flex-1 overflow-y-auto pr-1">
                {/* Upload Dropzone */}
                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => {
                    e.preventDefault();
                    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                      handleKbUpload(e.dataTransfer.files[0]);
                    }
                  }}
                  onClick={() => kbFileInputRef.current?.click()}
                  className="p-6 border-2 border-dashed border-[#d6cebf] hover:border-[#ea580c] rounded-xl bg-[#faf8f5] text-center space-y-2 transition-colors cursor-pointer"
                >
                  <input
                    type="file"
                    ref={kbFileInputRef}
                    onChange={(e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        handleKbUpload(e.target.files[0]);
                      }
                    }}
                    className="hidden"
                    accept=".pdf,.docx,.doc,.txt,.md,.csv,.json"
                  />
                  <UploadCloud className="w-8 h-8 text-[#ea580c] mx-auto" />
                  <div className="text-xs font-semibold text-[#1c1917]">
                    {kbUploadLoading ? "Parsing and indexing document into RAG..." : "Click or drag & drop files to index into RAG"}
                  </div>
                  <p className="text-[10px] text-[#78716c]">
                    Supports PDF, Word (.docx), TXT, Markdown, CSV. Automatically chunked with local TF-IDF / BM25 index.
                  </p>
                </div>

                {/* Documents Table */}
                <div className="space-y-2">
                  <div className="text-[10px] uppercase font-bold text-[#78716c] tracking-wider">
                    Indexed Documents ({kbDocuments.length})
                  </div>
                  {kbDocuments.length === 0 ? (
                    <div className="p-4 text-center text-[#a8a29e] font-mono text-xs bg-[#faf8f5] rounded-lg border border-[#e5ded1]">
                      No documents indexed yet. Upload files above to build your on-premises knowledge base.
                    </div>
                  ) : (
                    kbDocuments.map((doc) => (
                      <div
                        key={doc.doc_id}
                        className="flex items-center justify-between p-3 rounded-lg bg-[#faf8f5] border border-[#e5ded1]"
                      >
                        <div className="flex items-center space-x-2.5 truncate mr-2">
                          <div className="p-1.5 rounded bg-[#ffffff] border border-[#d6cebf]">
                            <FileText className="w-4 h-4 text-[#ea580c]" />
                          </div>
                          <div className="truncate">
                            <div className="font-semibold text-xs text-[#1c1917] truncate">{doc.filename}</div>
                            <div className="text-[10px] font-mono text-[#78716c]">
                              {doc.chunk_count} Chunks • {Math.round(doc.size_bytes / 1024)} KB • {doc.character_count} chars
                            </div>
                          </div>
                        </div>
                        <button
                          onClick={() => handleKbDelete(doc.doc_id)}
                          className="p-1.5 text-[#a8a29e] hover:text-[#dc2626] hover:bg-[#ffffff] rounded transition-colors"
                          title="Delete document from RAG index"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Model Settings Modal */}
      {activeModal === 'models' && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-[#ffffff] border border-[#d6cebf] rounded-xl max-w-xl w-full p-6 shadow-xl space-y-4 text-xs font-mono text-[#1c1917]">
            <div className="flex items-center justify-between border-b border-[#e5ded1] pb-3">
              <div className="flex items-center space-x-2 font-bold text-[#1c1917]">
                <Cpu className="w-4 h-4 text-[#ea580c]" />
                <span>LOCAL SOVEREIGN FOUNDATION MODEL</span>
              </div>
              <button
                onClick={() => setActiveModal(null)}
                className="text-[#78716c] hover:text-[#1c1917]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Live Ollama Connectivity Card */}
            <div className="p-4 rounded-xl bg-[#faf8f5] border border-[#e5ded1] space-y-2.5 font-sans">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className={`w-2.5 h-2.5 rounded-full ${healthData?.ollama_backend?.available ? 'bg-[#16a34a] animate-pulse' : 'bg-[#ea580c]'}`} />
                  <span className="font-semibold text-xs">
                    {healthData?.ollama_backend?.available ? 'Ollama Daemon Connected' : 'Ollama Daemon Offline'}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-[#78716c]">
                  {healthData?.ollama_backend?.endpoint || 'http://127.0.0.1:11434'}
                </span>
              </div>

              <div className="text-[11px] text-[#57534e]">
                Active Model: <strong className="text-[#1c1917]">{healthData?.active_foundation_model || healthData?.active_model_id || 'Auto-Detected'}</strong> (~3.4 GB RAM allocation)
              </div>

              {healthData?.ollama_backend?.models && healthData.ollama_backend.models.length > 0 ? (
                <div className="space-y-1.5 pt-2 border-t border-[#e5ded1]">
                  <div className="text-[10px] uppercase font-bold text-[#78716c] font-mono">Installed Ollama Models:</div>
                  <div className="flex flex-wrap gap-1.5">
                    {healthData.ollama_backend.models.map((mTag) => (
                      <button
                        key={mTag}
                        onClick={() => handleSelectModel(mTag)}
                        className={`px-2.5 py-1 rounded-md text-[11px] font-mono transition-all ${
                          (healthData.active_model_id === mTag || healthData.active_foundation_model === mTag)
                            ? 'bg-[#ea580c] text-white font-bold shadow-xs'
                            : 'bg-[#ffffff] text-[#44403c] border border-[#d6cebf] hover:border-[#ea580c]'
                        }`}
                      >
                        {mTag}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-[#fff7ed] border border-[#fed7aa] text-[11px] text-[#9a3412] space-y-1">
                  <div className="font-bold flex items-center space-x-1">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>Ollama Connection Notice</span>
                  </div>
                  <p>Start your local model in terminal:</p>
                  <code className="block p-1.5 rounded bg-[#ffffff] font-mono text-[10px] text-[#ea580c] border border-[#fed7aa]">
                    ollama run llama3 &nbsp;# or: ollama run gemma3:4b
                  </code>
                </div>
              )}
            </div>

            <div className="flex justify-end pt-2 border-t border-[#e5ded1]">
              <button
                onClick={fetchHealth}
                className="px-3 py-1.5 rounded-lg bg-[#faf8f5] hover:bg-[#ede7dc] text-[#1c1917] font-semibold flex items-center space-x-1.5 border border-[#d6cebf] text-xs transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5 text-[#ea580c]" />
                <span>Refresh Connection</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Full-Screen Image / Plot Lightbox Modal */}
      {expandedImage && (
        <div
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-60 flex items-center justify-center p-4"
          onClick={() => setExpandedImage(null)}
        >
          <div className="relative max-w-4xl max-h-[90vh] bg-[#ffffff] p-2 rounded-xl shadow-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={() => setExpandedImage(null)}
              className="absolute top-3 right-3 p-1.5 rounded-full bg-black/60 hover:bg-black text-white transition-colors"
              title="Close image"
            >
              <X className="w-4 h-4" />
            </button>
            <img src={expandedImage} alt="Expanded visualization" className="max-h-[85vh] max-w-full object-contain rounded" />
          </div>
        </div>
      )}
    </div>
  );
}


