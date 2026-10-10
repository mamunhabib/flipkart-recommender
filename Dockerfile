# 1. Base Image: Start with a very small, lightweight version of Linux that has Python 3.11 pre-installed.
FROM python:3.11-slim

# Automatically link this Docker image to the GitHub repository so it appears on the sidebar
LABEL org.opencontainers.image.source="https://github.com/mamunhabib/flipkart-recommender"

# 2. Working Directory: Create a folder called /app inside the container and move into it.
WORKDIR /app

# 3. Cache Dependencies: Copy ONLY the requirements file first. 
# This is a massive optimization trick! It ensures Docker doesn't re-download LangChain every time you change a line of HTML.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Source Code: Copy all the files from your Mac (app, core, run.py) into the /app folder in the container.
COPY . .

# 5. Expose Port: Tell the container to open port 5000 so the outside world can see the web interface.
EXPOSE 5000

# 6. Run Command: The exact terminal command the container should run the second it boots up.
CMD ["python", "run.py"]
