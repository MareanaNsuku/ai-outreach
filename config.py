import os
from urllib.parse import urlparse

OUTPUT_DIR = "/Users/nsukumareana/Library/CloudStorage/GoogleDrive-mareanansuku@gmail.com/My Drive/AI Outreach/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOMAIN_BLACKLIST = {
    "briefly.co.za","news24.com","sapeople.com","timeslive.co.za",
    "iol.co.za","enca.com","ewn.co.za","thesouthafrican.com",
    "dailymaverick.co.za","bbc.com","cnn.com","reuters.com",
    "apnews.com","aljazeera.com","theguardian.com","nytimes.com",
    "washingtonpost.com","forbes.com","businessinsider.com","techcrunch.com",
    "mashable.com","theverge.com","engadget.com","gizmodo.com",
}
def is_blacklisted(link):
    domain = urlparse(link).netloc.lower()
    return domain in DOMAIN_BLACKLIST or any(d in domain for d in DOMAIN_BLACKLIST)

AI_KEYWORD_WEIGHTS = {
    "ai":1,"artificial intelligence":3,"machine learning":3,
    "deep learning":3,"neural network":3,"nlp":2,
    "natural language":1,"computer vision":3,
    "prompt engineer":3,"generative ai":4,"llm":3,
    "gpt":3,"chatbot":2,"ai trainer":3,
    "ai evaluator":3,"data annotation":2,"ai engineer":4,
    "ml engineer":4,"ai developer":4,"machine learning engineer":4,
    "deep learning engineer":4,"ai researcher":4,"ai ethics":2,
    "prompt writer":3,"ai moderation":2,"ai chat":2,
    "ai solutions":2,"artificial intelligence engineer":4,
    "ai data scientist":4,"tensorflow":5,"pytorch":5,
    "keras":4,"scikit-learn":3,"mlops":3,
    "transformer model":4,"hugging face":4,"stable diffusion":4,
    "langchain":4,"llama":3,"ai agent":4,"autonomous ai":4,
    "ai safety":3,"retrieval augmented generation":5,"rag":2,
    "computer vision engineer":4,"nlp engineer":4,"ai startups":1,
}

REMOTE_KEYWORDS = [
    "remote","work from home","online job","virtual assistant","data entry",
    "transcription","customer service","customer support","call center",
    "social media evaluator","online tutor","english teacher","freelance",
    "micro job","micro task","side hustle","gig","telecommute",
    "content writer","copywriter","graphic designer","web developer",
    "software developer","app tester","game tester","translator",
    "proofreader","video editor","voice over","online moderator",
    "learnership","internship","intern","stipend",
]
TECH_KEYWORDS = [
    "programming","coding","python","javascript","java","c++","c#","ruby","go","rust",
    "swift","kotlin","web development","frontend","backend","full stack","react","angular",
    "vue","node","django","flask","machine learning","deep learning","neural network",
    "data science","artificial intelligence","ai","ml","nlp","computer vision",
    "tensorflow","pytorch","keras","scikit-learn","software engineering","devops",
    "cloud computing","aws","azure","gcp","docker","kubernetes","linux","git","sql",
    "database","algorithms","data structures","computer science","cs50","it","cybersecurity",
    "mobile app","android","ios","flutter","blockchain","game development","unity","unreal",
    "ethical hacking","penetration testing"
]
NON_TECH_KEYWORDS = [
    "soft skill","personal development","self help","self improvement",
    "leadership","communication skill","public speaking","mindfulness",
    "meditation","yoga","life coach","emotional intelligence",
    "time management","productivity hack","goal setting",
    "cooking","photography","music production","drawing","painting",
    "writing fiction","poetry","creative writing",
    "gardening","fitness","nutrition","health coach",
    "personal finance","investing","stock market","real estate",
    "language learning (not programming)","spanish","french","german",
    "marketing (non-tech)","sales (non-tech)","hr","recruiting",
    "business strategy","entrepreneurship (non-tech)","startup idea",
    "personal branding","network marketing",
]
FREE_INDICATORS = ["free","no cost","open course","open access","no payment","free pdf","free download","free ebook","zero cost","no subscription"]

NEWS_INDICATORS = [
    "breaking","news","court","police","school","grade","teacher suspended",
    "student","anc","eff","ramaphosa","zuma","malema","political","government says",
    "weather","traffic","accident","murder","robbery","stabbing","died",
    "watch:","video:","pic:","picture:","photo:","photos:","pictures:",
    "tiktok video","viral video","shocking","disturbing","exclusive",
    "editorial","opinion","analysis","explainer","what to know",
    "watch: ","south african","zimdollar","bafana","springboks","proteas",
    "rwc","world cup","soccer","rugby","cricket","olympics",
    "load shedding","eskom","anc","da","eff","mk party","ifp",
    "gauteng","mpumalanga","kwazulu","natal","limpopo","freestate","north west",
]

JOB_CATEGORIES = {
    "AI/ML Engineer": ["ai engineer","ml engineer","machine learning engineer","deep learning engineer","nlp engineer","computer vision engineer","ai developer"],
    "AI Researcher": ["ai researcher","research scientist","machine learning researcher","deep learning researcher"],
    "AI Agent Developer": ["ai agent","autonomous ai","langchain","agent developer"],
    "Prompt Writer / AI Trainer": ["prompt writer","prompt engineer","ai trainer","ai evaluator","ai tutor"],
    "Data Annotation / Labelling": ["data annotation","data labelling","data labeling","image annotation","video annotation"],
    "Chatbot Evaluator": ["chatbot evaluator","chat moderator","ai moderator","content moderator"],
    "AI Data Scientist": ["data scientist","data analyst","data analytics","business intelligence","data science"],
    "AI Safety & Ethics": ["ai safety","ai ethics","responsible ai"],
    "Other AI/Remote Work": []
}
COURSE_CATEGORIES = {
    "Machine Learning / AI": ["machine learning","deep learning","neural network","artificial intelligence","nlp","computer vision","generative ai","llm","prompt engineering"],
    "AI Agents & Automation": ["ai agent","autonomous ai","langchain","agent development"],
    "AI Ethics & Safety": ["ai ethics","ai safety","responsible ai"],
    "Data Science": ["data science","data analytics","pandas","numpy","matplotlib","seaborn","tableau","power bi"],
    "Python for AI": ["python"],
    "AI Research Papers": ["research paper","arxiv","conference","journal"],
    "Other AI Courses": []
}

RSS_FEEDS = [
    "https://remoteok.com/remote-ai-jobs.rss",
    "https://weworkremotely.com/categories/remote-ai-jobs.rss",
    "https://ai-jobs.net/feed/",
]
JOB_SCRAPE_PAGES = [
    ("https://fullyscholarships.com/5-ai-websites-paying-30-60-hour/", "FullyScholarships AI"),
    ("https://remoteok.com", "Remote OK"),
    ("https://remotive.com", "Remotive"),
    ("https://www.makoyajobs.co.za", "MakoyaJobs SA"),
    ("https://www.nasi-ispani.co.za", "Nasi Ispani SA"),
    ("https://ai-jobs.net", "AI-Jobs.net"),
]
REDDIT_RSS = [
    "https://www.reddit.com/r/RemoteJobs/.rss",
    "https://www.reddit.com/r/WorkOnline/.rss",
    "https://www.reddit.com/r/freelance/.rss",
    "https://www.reddit.com/r/SlaveLabour/.rss",
    "https://www.reddit.com/r/HireaWriter/.rss",
    "https://www.reddit.com/r/VirtualAssistant/.rss",
    "https://www.reddit.com/r/ArtificialIntelligence/.rss",
    "https://www.reddit.com/r/MachineLearning/.rss",
]
JOB_SEARCH_QUERIES = [
    "ai remote jobs no experience","machine learning engineer remote job","ai trainer remote job hiring",
    "data annotation ai remote","prompt writer ai remote","ai chatbot evaluator remote",
    "artificial intelligence learnership South Africa 2026 stipend","ai training jobs $30 hour",
    "remote ai side hustle","ai agent developer remote","autonomous ai engineer remote",
    "langchain developer remote","ai safety researcher remote","computer vision engineer remote",
    "nlp engineer remote","generative ai engineer remote","ai ethics consultant remote",
]
COURSE_SCRAPE_PAGES = [
    ("https://www.classcentral.com/subject/ai", "Class Central AI"),
    ("https://www.classcentral.com/subject/deep-learning", "Class Central Deep Learning"),
    ("https://ocw.mit.edu/search/?q=artificial+intelligence", "MIT OCW AI"),
    ("https://www.edx.org/search?tab=course&subject=Artificial+Intelligence&availability=Free", "edX Free AI"),
    ("https://www.coursera.org/courses?query=free&skills=Artificial+Intelligence", "Coursera AI"),
    ("https://www.freecodecamp.org/learn/", "freeCodeCamp"),
    ("https://www.kaggle.com/learn", "Kaggle Learn"),
    ("https://developers.google.com/machine-learning/crash-course", "Google ML Crash"),
    ("https://ai.google/education/", "Google AI Education"),
    ("https://www.udemy.com/courses/search/?price=price-free&q=ai", "Udemy AI"),
    ("https://www.udemy.com/courses/search/?price=price-free&q=machine+learning", "Udemy ML"),
    ("https://www.deeplearning.ai/courses/", "DeepLearning.AI"),
    ("https://course.fast.ai/", "Fast.ai"),
]
COURSE_SEARCH_QUERIES = [
    "free ai course online 2026","free machine learning course","free deep learning course",
    "free nlp course","free computer vision course","free generative ai course",
    "free prompt engineering course","free ai ethics course","free python for ai course",
    "free ai agent development course","free langchain tutorial","free autonomous ai course",
    "free retrieval augmented generation course","free ai safety course","free ai research paper course",
]
PDF_SEARCH_QUERIES = [
    "filetype:pdf free python programming book","filetype:pdf free machine learning book",
    "filetype:pdf free deep learning with pytorch","filetype:pdf free artificial intelligence notes",
    "filetype:pdf free nlp with python","filetype:pdf free computer vision notes",
    "filetype:pdf free generative ai guide","filetype:pdf free prompt engineering book",
    "filetype:pdf free langchain tutorial","filetype:pdf free ai agent development",
    "filetype:pdf free retrieval augmented generation","filetype:pdf free ai safety textbook",
    "site:github.com free programming books pdf","site:arxiv.org ai pdf",
    "filetype:pdf machine learning research paper 2025",
]

def is_remote(txt, extra=None):
    kw = REMOTE_KEYWORDS + (extra or [])
    return any(k in txt.lower() for k in kw)
def is_free(txt): return any(k in txt.lower() for k in FREE_INDICATORS)
def is_tech(txt): return any(k in txt.lower() for k in TECH_KEYWORDS)
def is_non_tech(txt): return any(k in txt.lower() for k in NON_TECH_KEYWORDS)
def is_news(txt):
    txt = txt.lower()
    return any(k in txt for k in NEWS_INDICATORS)
def is_ai_related(txt, threshold=4):
    txt = txt.lower()
    score = sum(weight for kw, weight in AI_KEYWORD_WEIGHTS.items() if kw in txt)
    return score >= threshold
def categorize_job(title, desc):
    text = (title + " " + desc).lower()
    for cat, keys in JOB_CATEGORIES.items():
        if cat == "Other AI/Remote Work": continue
        if any(k in text for k in keys): return cat
    return "Other AI/Remote Work"
def categorize_course(title, desc):
    text = (title + " " + desc).lower()
    for cat, keys in COURSE_CATEGORIES.items():
        if cat == "Other AI Courses": continue
        if any(k in text for k in keys): return cat
    return "Other AI Courses"
def entry(title, link, desc="", src="", category=""):
    return {"title":title.strip()[:150],"link":link.strip(),"description":desc.strip()[:300],"source":src,"category":category}
