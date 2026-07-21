def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #6C5DD3;
        --secondary: #FF754C;
        --bg-color: #F8F9FD;
        --card-bg: rgba(255, 255, 255, 0.85);
        --text-color: #1E202C;
        --glass-border: rgba(108, 93, 211, 0.12);
        --card-shadow: 0 8px 30px rgba(108, 93, 211, 0.05);
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Outfit', sans-serif;
        color: var(--text-color);
        background-color: var(--bg-color);
    }
    
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #F8F9FD 0%, #E8ECF8 100%);
        background-attachment: fixed;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1E202C !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--card-shadow);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(108, 93, 211, 0.09);
        border-color: rgba(108, 93, 211, 0.25);
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
        margin-top: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .result-pos {
        background: linear-gradient(135deg, #E2F6EA 0%, #C3F0D4 100%);
        box-shadow: 0 8px 24px rgba(40, 167, 69, 0.1);
        border-left: 6px solid #28A745;
        color: #155724 !important;
    }
    
    .result-pos h2 {
        color: #155724 !important;
    }
    
    .result-neg {
        background: linear-gradient(135deg, #FDF2F4 0%, #FAD7DD 100%);
        box-shadow: 0 8px 24px rgba(220, 53, 69, 0.1);
        border-left: 6px solid #DC3545;
        color: #721C24 !important;
    }
    
    .result-neg h2 {
        color: #721C24 !important;
    }
    
    .result-neu {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFF0C2 100%);
        box-shadow: 0 8px 24px rgba(255, 193, 7, 0.1);
        border-left: 6px solid #FFC107;
        color: #856404 !important;
    }
    
    .result-neu h2 {
        color: #856404 !important;
    }
    
    .result-card h2 {
        margin-top: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid var(--glass-border);
    }
    
    /* Inputs */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid var(--glass-border) !important;
        color: #1E202C !important;
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
        box-shadow: 0 4px 15px rgba(108, 93, 211, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(108, 93, 211, 0.35);
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #5E6278;
        padding: 8px 16px;
        border: 1px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(108, 93, 211, 0.08) !important;
        color: var(--primary) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* History Items */
    .history-item {
        background: #FFFFFF;
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        transition: background 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px rgba(108, 93, 211, 0.03);
    }
    
    .history-item:hover {
        background: #F9FAFC;
        box-shadow: 0 4px 12px rgba(108, 93, 211, 0.06);
    }
    
    .hist-label-pos { color: #28A745; font-weight: bold; }
    .hist-label-neg { color: #DC3545; font-weight: bold; }
    .hist-label-neu { color: #D39E00; font-weight: bold; }
    
    /* Metric styling for high contrast */
    [data-testid="stMetricLabel"] {
        color: #5E6278 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #1E202C !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    
    </style>
    """
