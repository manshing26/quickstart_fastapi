use('testdb');

// pw: test123
db.users.insertOne({
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Admin",
    "hashed_password": "$2b$12$GOoyCotCzvIa9wuxKCybBeB8IS763gHvahTbNbwM2HshNzl5Ug4vy",
    "active": true,
    "role": "admin"
})