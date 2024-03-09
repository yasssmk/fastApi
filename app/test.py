from dotenv import load_dotenv
load_dotenv()

import os  # Add this import

# Try printing an environment variable to see if it's loaded correctly
print(os.getenv("ALGORITHM"))
