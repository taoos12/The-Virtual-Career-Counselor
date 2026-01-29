from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import hashlib
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# In-memory databases using dictionaries
users_db = {}
admins_db = {}
conversations_db = {}

# Initialize with default admin
admins_db['admin'] = {
    'password': hashlib.sha256('admin123'.encode()).hexdigest(),
    'email': 'admin@careercounselor.com',
    'created_at': datetime.now().isoformat()
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_career_guidance(user_query, scenario_type="general"):
    """
    Enhanced AI response system with specific scenarios
    In production, this would integrate with Groq/Amazon Bedrock
    """
    
    query_lower = user_query.lower()
    
    # Scenario 1: Career Path Exploration
    career_paths = {
        'software developer': {
            'skills': ['Python', 'JavaScript', 'Git', 'Problem-solving', 'Database management'],
            'courses': ['Computer Science Fundamentals', 'Web Development Bootcamp', 'Data Structures & Algorithms', 'Software Engineering Principles'],
            'job_roles': ['Frontend Developer', 'Backend Developer', 'Full-Stack Developer', 'Software Engineer', 'DevOps Engineer'],
            'description': 'Software development is a rapidly growing field with excellent career prospects.'
        },
        'data scientist': {
            'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
            'courses': ['Data Science Fundamentals', 'Machine Learning Specialization', 'Statistics for Data Science', 'Big Data Analytics'],
            'job_roles': ['Data Analyst', 'Machine Learning Engineer', 'Business Intelligence Analyst', 'Research Scientist'],
            'description': 'Data science combines statistics, programming, and domain expertise to extract insights from data.'
        },
        'digital marketer': {
            'skills': ['SEO', 'Social Media Marketing', 'Content Creation', 'Analytics', 'PPC Advertising'],
            'courses': ['Digital Marketing Fundamentals', 'Google Ads Certification', 'Social Media Strategy', 'Content Marketing'],
            'job_roles': ['SEO Specialist', 'Social Media Manager', 'Content Marketer', 'PPC Specialist', 'Marketing Analyst'],
            'description': 'Digital marketing focuses on promoting products and services through digital channels.'
        },
        'ux designer': {
            'skills': ['User Research', 'Wireframing', 'Prototyping', 'Figma', 'Adobe Creative Suite', 'Usability Testing'],
            'courses': ['UX Design Fundamentals', 'User Research Methods', 'Interaction Design', 'Design Thinking'],
            'job_roles': ['UX Designer', 'UI Designer', 'Product Designer', 'User Researcher', 'Design Lead'],
            'description': 'UX design focuses on creating meaningful and relevant experiences for users.'
        }
    }
    
    # Check for career path exploration
    for career, info in career_paths.items():
        if career.replace(' ', '') in query_lower.replace(' ', '') or any(word in query_lower for word in career.split()):
            response = f"**Career Path: {career.title()}**\n\n"
            response += f"{info['description']}\n\n"
            response += f"**Required Skills:**\n"
            for skill in info['skills']:
                response += f"• {skill}\n"
            response += f"\n**Recommended Courses:**\n"
            for course in info['courses']:
                response += f"• {course}\n"
            response += f"\n**Potential Job Roles:**\n"
            for role in info['job_roles']:
                response += f"• {role}\n"
            return response
    
    # Scenario 2: Course Recommendations
    if any(word in query_lower for word in ['course', 'learn', 'study', 'education', 'training']):
        if 'programming' in query_lower or 'coding' in query_lower:
            return """**Personalized Course Recommendations - Programming:**

Based on current market demand, here are my top recommendations:

**Beginner Level:**
• Python for Beginners - Learn syntax, data structures, and basic programming concepts
• Introduction to Web Development - HTML, CSS, and JavaScript fundamentals
• Git & Version Control - Essential for any developer

**Intermediate Level:**
• Full-Stack Web Development - React, Node.js, and database integration
• Data Structures & Algorithms - Critical for technical interviews
• Cloud Computing Basics - AWS or Azure fundamentals

**Advanced Level:**
• Machine Learning with Python - scikit-learn, TensorFlow
• DevOps & CI/CD - Docker, Kubernetes, Jenkins
• System Design - Scalable architecture patterns

Each course includes hands-on projects and industry-relevant skills!"""
        
        elif 'business' in query_lower or 'management' in query_lower:
            return """**Personalized Course Recommendations - Business:**

Tailored for your business career goals:

**Foundation Courses:**
• Business Analytics Fundamentals - Data-driven decision making
• Project Management Professional (PMP) - Industry-standard certification
• Financial Analysis & Modeling - Excel and financial planning

**Specialization Tracks:**
• Digital Marketing Strategy - SEO, SEM, social media marketing
• Supply Chain Management - Operations and logistics optimization
• Leadership & Team Management - Soft skills for career advancement

**Advanced Certifications:**
• MBA Essentials - Strategy, finance, and operations
• Six Sigma Green Belt - Process improvement methodologies
• Agile & Scrum Master - Modern project management approaches

These courses are selected based on high job market demand and salary potential!"""
    
    # Scenario 3: Job Market Insights
    if any(word in query_lower for word in ['job market', 'salary', 'demand', 'trends', 'hiring', 'employment']):
        return """**Job Market Insights - Current Trends:**

** High-Demand Skills (2025-2026):**
• Artificial Intelligence & Machine Learning - 40% job growth
• Cloud Computing (AWS, Azure, GCP) - 35% job growth  
• Cybersecurity - 32% job growth
• Data Science & Analytics - 28% job growth
• Full-Stack Development - 25% job growth

**Salary Trends by Role:**
• AI/ML Engineer: $120,000 - $180,000
• Cloud Architect: $130,000 - $200,000
• Cybersecurity Specialist: $90,000 - $150,000
• Data Scientist: $95,000 - $160,000
• Full-Stack Developer: $75,000 - $130,000

**Top Hiring Regions:**
• San Francisco Bay Area - Tech hub with highest salaries
• Seattle - Strong demand for cloud and AI roles
• Austin - Growing tech scene with lower cost of living
• New York - Finance and fintech opportunities
• Remote Work - 60% of tech jobs now offer remote options

**Emerging Opportunities:**
• Prompt Engineering for AI systems
• Sustainability Technology roles
• Web3 and Blockchain development
• IoT and Edge Computing specialists

The job market is particularly strong for candidates with AI, cloud, and security skills!"""
    
    # General career guidance
    general_responses = {
        'skills': "Focus on developing both technical and soft skills. Technical skills get you the interview, but soft skills get you the job and help you advance.",
        'interview': "Prepare for interviews by practicing coding problems, researching the company, and preparing STAR method examples for behavioral questions.",
        'networking': "Build your professional network through LinkedIn, industry events, and informational interviews. Many jobs are filled through referrals.",
        'portfolio': "Create a strong portfolio showcasing your best work. For developers, use GitHub. For designers, use Behance or personal websites.",
        'career change': "Career changes are common! Focus on transferable skills, consider bootcamps or certifications, and start building experience through projects or volunteering."
    }
    
    for key, response in general_responses.items():
        if key in query_lower:
            return response
    
    return """Welcome to your Virtual Career Counselor! I can help you with:

** Career Path Exploration** - Ask about specific careers like "software developer" or "data scientist"
** Course Recommendations** - Tell me what you want to learn
** Job Market Insights** - Ask about salary trends, job demand, or market analysis
** General Guidance** - Career advice, interview tips, networking strategies

What would you like to explore today?"""

@app.route('/')
def index():
    # Redirect to login page first
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type', 'user')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    # Check if user already exists
    if user_type == 'admin':
        if username in admins_db:
            return jsonify({'success': False, 'message': 'Admin already exists'})
        admins_db[username] = {
            'password': hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat()
        }
    else:
        if username in users_db:
            return jsonify({'success': False, 'message': 'User already exists'})
        users_db[username] = {
            'password': hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'conversations': []
        }
    
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', 'user')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'})
    
    hashed_password = hash_password(password)
    
    if user_type == 'admin':
        if username in admins_db and admins_db[username]['password'] == hashed_password:
            session['admin_id'] = username
            session['user_type'] = 'admin'
            return jsonify({'success': True, 'redirect': '/admin-dashboard'})
    else:
        if username in users_db and users_db[username]['password'] == hashed_password:
            session['user_id'] = username
            session['user_type'] = 'user'
            return jsonify({'success': True, 'redirect': '/dashboard'})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user_id'])

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', admin=session['admin_id'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    data = request.get_json()
    user_query = data.get('message', '').strip()
    
    if not user_query:
        return jsonify({'success': False, 'message': 'Please enter a message'})
    
    # Generate AI response
    ai_response = generate_career_guidance(user_query)
    
    # Store conversation
    conversation_id = str(uuid.uuid4())
    conversation = {
        'id': conversation_id,
        'user_id': session['user_id'],
        'user_message': user_query,
        'ai_response': ai_response,
        'timestamp': datetime.now().isoformat()
    }
    
    conversations_db[conversation_id] = conversation
    users_db[session['user_id']]['conversations'].append(conversation_id)
    
    return jsonify({
        'success': True,
        'response': ai_response,
        'timestamp': conversation['timestamp']
    })

@app.route('/api/admin/stats')
def api_admin_stats():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    stats = {
        'total_users': len(users_db),
        'total_conversations': len(conversations_db),
        'total_admins': len(admins_db)
    }
    
    return jsonify({'success': True, 'stats': stats})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)