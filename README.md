# JetIntel Backend API

A FastAPI-based REST API for the JetIntel private jet intelligence platform. This backend provides role-based access control with admin and user roles, JWT authentication, and comprehensive jet management capabilities.

## 🚀 Features

- **Role-Based Access Control (RBAC)**: Admin and User roles with different permissions
- **JWT Authentication**: Secure token-based authentication with email/password
- **Jet Management**: Full CRUD operations for private jet data (Admin only)
- **Public Endpoints**: Open access to view jets and get recommendations
- **AI-Powered Recommendations**: Route-based jet recommendations using Haversine distance calculations
- **MongoDB Integration**: NoSQL database for flexible data management
- **Interactive API Docs**: Auto-generated Swagger UI and ReDoc

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation using Python type hints
- **JWT (python-jose)** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
JetIntel-DB/
├── main.py                     # FastAPI app entry point
├── config.py                   # Configuration (JWT, MongoDB)
├── database.py                 # MongoDB connection setup
├── requirements.txt            # Python dependencies
├── seed.py                     # Seed jets and airports data
├── seed_admin.py              # Create initial admin user
├── .env                        # Environment variables
├── models/
│   ├── user.py                # User Pydantic schemas
│   └── jet.py                 # Jet Pydantic schemas
├── routes/
│   ├── auth.py                # Authentication endpoints
│   ├── jets.py                # Jet CRUD endpoints
│   └── recommend.py           # Recommendation logic
├── middleware/
│   └── auth.py                # JWT validation & role checking
├── utils/
│   └── helpers.py             # Helper functions (Haversine)
├── data/
│   ├── jets.json              # Jet seed data
│   └── airports.json          # Airport seed data
└── static/
    └── images/                # Jet images
```

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.9+
- MongoDB Atlas account (or local MongoDB)
- Git

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   cd JetIntel-DB
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Update the `.env` file with your MongoDB connection string:
   ```env
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
   JWT_SECRET=your-super-secret-jwt-key-change-in-production
   ```

5. **Seed the database**
   
   First, seed jets and airports data:
   ```bash
   python seed.py
   ```

   Then create the admin user:
   ```bash
   python seed_admin.py
   ```

6. **Run the server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔐 Authentication

### Default Admin Credentials

After running `seed_admin.py`, use these credentials:

- **Email**: `admin@jetintel.com`
- **Password**: `admin123`

> ⚠️ **Important**: Change the default password after first login in production!

### How Authentication Works

1. **Register/Login** at `/auth/register` or `/auth/login`
2. Receive a JWT `access_token` in the response
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```
4. For Swagger UI: Click the **Authorize** button (🔒) and enter: `Bearer <token>`

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | None | Register a new user account |
| POST | `/auth/login` | None | Login and receive JWT token |
| GET | `/auth/me` | Required | Get current user information |

### Jets (Public Access)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/jets` | None | Get all jets |
| GET | `/jets/{jet_id}` | None | Get a specific jet by ID |

### Recommendations

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/recommend` | None | Get jet recommendation based on route |

**Query Parameters:**
- `departure`: IATA airport code (e.g., JFK)
- `arrival`: IATA airport code (e.g., LAX)
- `passengers`: Number of passengers
- `budget`: Budget in millions (e.g., 50 = $50M)

### Admin Routes (Admin Role Only)

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| POST | `/admin/jets` | Required | Admin | Create a new jet |
| PUT | `/admin/jets/{jet_id}` | Required | Admin | Update an existing jet |
| DELETE | `/admin/jets/{jet_id}` | Required | Admin | Delete a jet |

## 📝 Example Requests

### Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@jetintel.com",
    "password": "admin123"
  }'
```

### Get all jets

```bash
curl "http://localhost:8000/jets"
```

### Create a new jet (Admin only)

```bash
curl -X POST "http://localhost:8000/admin/jets" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "cessna-citation-x",
    "manufacturer": "Cessna",
    "model": "Citation X",
    "category": "Super Midsize",
    "range_nm": 3460,
    "cruise_knots": 527,
    "cruise_mach": 0.92,
    "max_passengers": 12,
    "price_new_million": 23.5,
    "price_used_million": 12.8,
    "fuel_efficiency_lph": 350,
    "cost_per_hour": 3200,
    "annual_cost_total": 2100000,
    "annual_cost_fuel": 980000,
    "annual_cost_maintenance": 650000,
    "annual_cost_crew": 470000,
    "runway_required_ft": 5250,
    "year_introduced": 1996,
    "description": "One of the fastest civilian aircraft",
    "tags": ["Super Midsize", "High Speed", "Corporate"],
    "image_url": "https://example.com/citation-x.jpg"
  }'
```

### Get recommendations

```bash
curl "http://localhost:8000/recommend?departure=LAX&arrival=JFK&passengers=8&budget=50"
```

## 🗃️ Data Models

### Jet Schema

```json
{
  "id": "gulfstream-g650er",
  "manufacturer": "Gulfstream",
  "model": "G650ER",
  "category": "Ultra Long Range",
  "range_nm": 7500,
  "cruise_knots": 516,
  "cruise_mach": 0.9,
  "max_passengers": 19,
  "price_new_million": 71.5,
  "price_used_million": 42,
  "fuel_efficiency_lph": 460,
  "cost_per_hour": 5200,
  "annual_cost_total": 3800000,
  "annual_cost_fuel": 1520000,
  "annual_cost_maintenance": 980000,
  "annual_cost_crew": 850000,
  "runway_required_ft": 6000,
  "year_introduced": 2014,
  "description": "The flagship of the Gulfstream fleet...",
  "tags": ["Ultra Long Range", "Flagship", "Transatlantic"],
  "image_url": "/images/G650.jpg"
}
```

### User Schema

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"  // or "admin"
}
```

## 🔒 Security Notes

1. **Change default credentials** after first deployment
2. **Use strong JWT_SECRET** - generate with: `openssl rand -hex 32`
3. **Enable HTTPS** in production
4. **Restrict CORS** origins in production (currently set to `*`)
5. **Rate limiting** - consider adding rate limiting middleware
6. **Environment variables** - never commit `.env` to version control

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### MongoDB connection issues
- Verify your `MONGO_URL` in `.env`
- Check MongoDB Atlas IP whitelist (allow `0.0.0.0/0` for development)
- Ensure database user has read/write permissions

### Module not found errors
```bash
pip install -r requirements.txt
```

### Virtual environment not activated
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 📦 Dependencies

Core dependencies (see `requirements.txt` for complete list):
- `fastapi>=0.135.1`
- `uvicorn>=0.41.0`
- `motor>=3.7.1` (async MongoDB)
- `pydantic>=2.12.5` (with email validation)
- `python-jose[cryptography]>=3.5.0` (JWT)  
  ⚠️ **Do not install the unrelated `jose` package**; it’s a Python 2 library that will raise syntax errors.
- `bcrypt>=4.2.1` (password hashing)
- `python-dotenv>=1.2.2`

## 🚢 Deployment

### Production Checklist

- [ ] Update `JWT_SECRET` to a strong random value
- [ ] Change admin password from default
- [ ] Restrict CORS origins to your frontend domain
- [ ] Enable HTTPS
- [ ] Set up proper MongoDB user with minimal permissions
- [ ] Configure firewall rules
- [ ] Add rate limiting
- [ ] Set up logging and monitoring
- [ ] Use environment-specific `.env` files
- [ ] Consider using Docker for containerization

### Example Production Command

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📄 License

This project is part of the JetIntel platform.

## 👨‍💻 Developer Notes

- The API uses **async/await** throughout for better performance
- MongoDB ObjectIds are automatically converted to strings in responses
- Jet IDs use slug format (e.g., `gulfstream-g650er`) for clean URLs
- Distance calculations use the **Haversine formula** for accuracy
- All timestamps are stored in UTC

## 🤝 Contributing

1. Ensure all endpoints are properly documented
2. Follow FastAPI best practices
3. Write clear commit messages
4. Test authentication flows before committing
5. Update this README for any significant changes

---

**Built with FastAPI** 🚀 | **Database: MongoDB** 🍃 | **JetIntel Platform** ✈️
