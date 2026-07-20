def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #6C5DD3;
        --secondary: #FF754C;
        --bg-color: #0F111A;
        --card-bg: rgba(255, 255, 255, 0.05);
        --text-color: #E0E0E0;
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: var(--text-color);
        background-color: var(--bg-color);
    }
    
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0F111A 0%, #1A1C29 100%);
        background-attachment: fixed;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Result Cards with Animation */
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .result-card {
        animation: slideUp 0.5s ease-out;
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-top: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .result-pos {
        background: linear-gradient(135deg, #00C853 0%, #69F0AE 100%);
        box-shadow: 0 8px 20px rgba(0, 200, 83, 0.3);
        border-left: 6px solid #B9F6CA;
    }
    
    .result-neg {
        background: linear-gradient(135deg, #FF1744 0%, #FF5252 100%);
        box-shadow: 0 8px 20px rgba(255, 23, 68, 0.3);
        border-left: 6px solid #FF8A80;
    }
    
    .result-neu {
        background: linear-gradient(135deg, #FF9100 0%, #FFD180 100%);
        box-shadow: 0 8px 20px rgba(255, 145, 0, 0.3);
        border-left: 6px solid #FFE57F;
    }
    
    .result-card h2 {
        margin-top: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 17, 26, 0.95);
        border-right: 1px solid var(--glass-border);
    }
    
    /* Inputs */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        background: linear-gradient(90deg, var(--primary) 0%, #8F7CFF 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 93, 211, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(108, 93, 211, 0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #888;
        padding: 8px 16px;
        border: 1px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(108, 93, 211, 0.1) !important;
        color: var(--primary) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* History Items */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        transition: background 0.2s;
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.07);
    }
    
    .hist-label-pos { color: #00E676; font-weight: bold; }
    .hist-label-neg { color: #FF5252; font-weight: bold; }
    .hist-label-neu { color: #FFAB40; font-weight: bold; }
    
    </style>
    """
