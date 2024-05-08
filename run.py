from app import create_app
from dotenv import load_dotenv

if __name__ == "__main__":
    # load env variables
    load_dotenv()

    create_app().run(host="0.0.0.0", port=int('3000'), debug=True)