import json
from optimizer import ResumeOptimizer  # import your class

# Dummy sample inputs — replace with real job/resume or load from file
job_description = """
We are looking for a Python developer with experience in backend systems, REST APIs, and PostgreSQL.
Must have at least 2 years of experience in software development.
"""

resume = """
Lance is a software developer with skills in Python, Flask, and database design. 
Worked on various projects involving APIs and data storage.
"""

# Create an optimizer instance
optimizer = ResumeOptimizer()

# Call the optimize_resume method and get raw response
raw_response = optimizer.optimize_resume(job_description, resume)

# Print raw GPT response
print("\n📦 RAW GPT RESPONSE FROM GPT-4o:")
print(raw_response)

# Try to parse the JSON response
try:
    result = json.loads(raw_response)
    print("\n✅ Parsed Result:")
    print(json.dumps(result, indent=2))  # Pretty-print the parsed JSON
except json.JSONDecodeError as e:
    print("\n❌ Failed to parse JSON. Here's the error:")
    print(e)
