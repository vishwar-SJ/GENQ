import { useState, useRef, useEffect } from 'react';
import api from '../api/axios';

export default function ChatBot({ reportId }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hi! I'm your GENQ Health Advisor. How can I help you understand your report and lifestyle changes?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  // Handle Speech Synthesis
  const speakText = (text) => {
    if (!voiceEnabled || !window.speechSynthesis) return;
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    // Find a good voice if possible (Google UK English Female or similar)
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.name.includes('Female') || v.name.includes('Google'));
    if (preferredVoice) utterance.voice = preferredVoice;
    
    utterance.rate = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  // Ensure voices are loaded
  useEffect(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.getVoices();
    }
  }, []);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        report_id: reportId,
        message: userText
      });

      const data = res.data;
      const botText = data.response;
      
      setMessages(prev => [
        ...prev, 
        { role: 'bot', text: botText, sections: data.sections }
      ]);
      
      // Speak the bot's response
      speakText(botText);

    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'bot', text: "I'm sorry, I encountered an error connecting to the server." }]);
    } finally {
      setLoading(false);
    }
  };

  const toggleVoice = () => {
    setVoiceEnabled(!voiceEnabled);
    if (voiceEnabled && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  };

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-teal-700 text-white shadow-lg flex items-center justify-center hover:bg-teal-800 transition-all z-50 slide-up"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden slide-up border border-gray-200" style={{ height: '500px', maxHeight: '80vh' }}>
      {/* Header */}
      <div className="bg-teal-700 text-white p-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a7 7 0 017 7c0 2.5-1.5 4.5-3 6l-1 1.5V20a2 2 0 01-2 2h-2a2 2 0 01-2-2v-3.5L8 15c-1.5-1.5-3-3.5-3-6a7 7 0 017-7z" />
          </svg>
          <span className="font-bold">Health Advisor</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={toggleVoice} className="p-1 hover:bg-teal-600 rounded" title={voiceEnabled ? "Mute Voice" : "Enable Voice"}>
            {voiceEnabled ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>
            )}
          </button>
          <button onClick={() => setIsOpen(false)} className="p-1 hover:bg-teal-600 rounded">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl px-4 py-2 ${msg.role === 'user' ? 'bg-teal-600 text-white rounded-br-none' : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'}`}>
              <p className="text-sm leading-relaxed">{msg.text}</p>
              
              {/* Render sections if bot provided them */}
              {msg.sections && msg.sections.map((sec, j) => (
                <div key={j} className="mt-3 pt-3 border-t border-gray-100">
                  <h4 className="text-xs font-bold text-teal-800 mb-1">{sec.title}</h4>
                  <ul className="list-disc pl-4 space-y-1">
                    {sec.items.map((item, k) => (
                      <li key={k} className="text-xs text-gray-600">{item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm">
              <div className="flex gap-1.5">
                <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style={{ animationDelay: '0.2s' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 bg-white border-t border-gray-200">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about diet, exercise, lifestyle..."
            className="flex-1 text-sm rounded-full bg-gray-100 border-transparent focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-200 px-4 py-2 outline-none transition-all"
          />
          <button 
            type="submit"
            disabled={!input.trim() || loading}
            className="w-10 h-10 rounded-full bg-teal-600 text-white flex items-center justify-center disabled:opacity-50 disabled:bg-gray-400 hover:bg-teal-700 transition-colors"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}
