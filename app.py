from app import create_app
import config as config

isDebug = config.DEBUG
app = create_app()

if __name__ == "__main__":
    app.run(debug=isDebug)