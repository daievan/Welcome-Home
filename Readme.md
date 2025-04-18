

# Welcome Home - Fullstack Project

This is a fullstack web application built with:

- **Frontend**: Vue 3
- **Backend**: Flask (Python)

---

## ⚙️ Project Setup

### 🖥️ Frontend (Vue)

```bash
cd frontend
npm install
npm run build
```


After building, copy the generated files to the Flask backend:


- Copy everything inside `dist/static/` to `backend/static/`
- Copy `dist/index.html` to `backend/templates/index.html`

```bash
cp -r dist/static/* ../backend/static/
cp dist/index.html ../backend/templates/index.html
```



### 🔧 Backend (Flask)


```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```


Before running the app, initialize the database:


```bash
flask init-db
```


Then start the backend server:


```bash
flask run --port=5001
```


The backend will be available at `http://127.0.0.1:5001`



## 📁 Project Structure


```php
project-root/
├── frontend/         # Vue frontend
├── backend/              # Flask backend
│   ├── static/           # Static assets from Vue build
│   ├── templates/        # index.html from Vue build
├── README.md
```



