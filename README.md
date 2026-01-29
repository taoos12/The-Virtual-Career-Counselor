# Virtual Career Counselor

A Generative AI-powered career counseling platform built with Flask, providing personalized career guidance and pathways.

## Features

- **AI-Powered Career Guidance**: Get personalized career advice using generative AI
- **User Authentication**: Separate login systems for users and administrators
- **Real-time Chat Interface**: Interactive chat with the AI career counselor
- **Admin Dashboard**: Monitor platform statistics and user activity
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Python dictionaries (in-memory storage)
- **AI Integration**: Ready for Amazon Bedrock integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd virtual-career-counselor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

### For Users
1. Register for a new account or login with existing credentials
2. Access the dashboard to start chatting with the AI career counselor
3. Ask questions about career paths, skills development, job opportunities, etc.
4. Receive personalized guidance and recommendations

### For Administrators
1. Login with admin credentials (default: username: `admin`, password: `admin123`)
2. Access the admin dashboard to view platform statistics
3. Monitor user activity and system performance

## Project Structure

```
virtual-career-counselor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── login.html        # User login
│   ├── register.html     # User registration
│   ├── admin_login.html  # Admin login
│   ├── dashboard.html    # User dashboard
│   └── admin_dashboard.html # Admin dashboard
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── main.js       # JavaScript functionality
```

## API Endpoints

- `POST /api/register` - User/Admin registration
- `POST /api/login` - User/Admin authentication
- `POST /api/chat` - Send message to AI counselor
- `GET /api/admin/stats` - Get platform statistics (admin only)

## Future Enhancements

- Integration with Amazon Bedrock for advanced AI capabilities
- Persistent database storage (PostgreSQL/MongoDB)
- User profile management
- Career assessment tools
- Job market analytics
- Email notifications
- Advanced admin features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.