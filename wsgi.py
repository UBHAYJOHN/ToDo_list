from app import app, create_table

if __name__ == "__main__":
    create_table()
    app.run()

# For WSGI servers to pick up the application
application = app
