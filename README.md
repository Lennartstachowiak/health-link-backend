# HealthLink Backend

Backend for **HealthLink** that handles **authorization**, **patient data retrieval**, and **chat requests**.

---

## 🚀 Getting Started

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/healthlink-backend.git
cd healthlink-backend
```

### 2. **Set Up a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

Or, if `requirements.txt` is not yet created:

```bash
pip install fastapi uvicorn python-dotenv
```

### 4. **Configure Environment Variables**

Create a `.env` file in the project root:

```bash
touch .env
```

Create a `.env` with the `.env.example` file

### 5. **Run the Application**

```bash
uvicorn app.main:app --reload
```

- The API will be available at: **`http://127.0.0.1:8000`**

---

## 📖 API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📂 Project Structure

```
healthlink-backend/
├── app/
│   ├── main.py          # FastAPI app initialization
│   ├── routes.py        # API routes
│   └── auth.py          # Authentication logic
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── venv/                # Virtual environment
```

---

## 🛠️ Available Commands

- **Run the server (dev mode):**

  ```bash
  uvicorn app.main:app --reload
  ```

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

---

## ✅ Features

- **User Authorization** via OTP and JWT.
- **Patient Data Retrieval** API.
- **Secure Chat Requests.**
- Auto-generated **OpenAPI docs**.

---

## 🤝 Contribution

1. Fork the repo.
2. Create your feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
