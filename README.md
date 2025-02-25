# Health Insurance System

## Overview
The Health Insurance System is a web application built using Django for the backend and React for the frontend. It allows users to view and manage insurance plans, provide feedback, and get personalized recommendations based on their profiles.

## Features
- User registration and authentication
- View available insurance plans
- Provide feedback on insurance plans
- Get personalized insurance plan recommendations
- Responsive frontend built with React

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Frontend**: React, Vite
- **Database**: SQLite (for development)
- **Containerization**: Docker (previously used, now removed)

## Getting Started

### Prerequisites
- Python 3.x
- Node.js
- npm

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd HealthInsurance
   ```

2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Start the frontend server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:8000/api](http://localhost:8000/api)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
