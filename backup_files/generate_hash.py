from werkzeug.security import generate_password_hash

hashed = generate_password_hash("admin123")
print(hashed)
