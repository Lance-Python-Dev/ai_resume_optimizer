import os
import openai 
import json
from dotenv import load_dotenv



#loading environment variables from .env file into the current environment
load_dotenv()



#handles optimization using openai's GPT-4o model
class ResumeOptimizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def optimize_resume(self, job_description, resume):
        try: 
            response = self.client.chat.completions.create(
    model="gpt-4o",
    response_format="json",

    messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume optimizer and career coach. "
                    "Analyze the provided job description and resume, "
                    "then optimize the resume to better match the job requirements."
                )
            },
            {
                "role": "user",
                "content": f"""
    Job Description:
    {job_description}

    Current Resume:
    {resume}

    Please:
    1. Rewrite the resume to better align with the job description
    2. Include relevant keywords from the job description naturally
    3. Highlight transferable skills and experiences
    4. Improve formatting and structure
    5. Provide specific suggestions for improvement
    6. Calculate a match score (0-100) based on how well the optimized resume aligns with the job
    7. List the key keywords that match between the job description and resume

    Focus on:
    - Using action verbs and quantifiable achievements
    - Matching the tone and language of the job description
    - Emphasizing relevant skills and experiences
    - Removing or de-emphasizing irrelevant information
    - Ensuring ATS (Applicant Tracking System) compatibility

    Return the optimized resume in a clean, professional format.
    """
        }
    ]
)

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"Error Optimizing Resume: {e}")
            return None
        

def main(): 
    print("\n" + "=" * 50)
    print(("🚀 RESUME OPTIMIZER - POWERED BY AI 🚀".center(50)))
    print("=" * 50 + "\n")

    #Check if the OpenAI API key is available in environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OpenAI API key was not found!")
        print("Please set your OPEN_API_KEY environment variable.")
        return
    
    # Display welcome message explaining the tool's purpose
    print("This tool will optimize your resume based on a specific job description. \n")

    # Get job description input from user
    print("📝 JOB DESCRIPTION")
    print("Paste the job description below (press Enter twice when done):")

    job_description_lines = []
    while True:
        line = input()
        
        if line.strip() == "":
            break

        job_description_lines.append(line)
    job_description = "\n".join(job_description_lines)

    print("\n📄 YOUR CURRENT RESUME")
    print("Paste your current resume below (press Enter twice when done):")

    resume_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        resume_lines.append(line)
    resume = "\n".join(resume_lines)
    
    # Validate that both inputs were provided by the user
    if not job_description or not resume:
        print("❌ Error: Both job description and resume are required!")
        return
    
    print("\n⏳ Optimizing your resume... (this may take a minute)")
    
    # Create an instance of the ResumeOptimizer class
    optimizer = ResumeOptimizer()
    result = optimizer.optimize_resume(job_description, resume)
    
    # Check if optimization was successful
    if not result:
        print("❌ Error: Failed to optimize resume. Please try again.")
        return
    
    print("\n" + "="*50)
    print("✅ OPTIMIZATION COMPLETE".center(50))
    print("="*50 + "\n")
    
    # Display the match score from the optimization result
    print(f"🎯 Match Score: {result['score']}%\n")
    
    # Display keyword matches section
    print("📊 KEYWORD MATCHES:")
    for keyword in result['keyword_matches']:
        print(f"• {keyword}")
    print()
    
    # Display improvement suggestions section
    print("💡 SUGGESTIONS FOR IMPROVEMENT:")
    for suggestion in result['suggestions']:
        print(f"• {suggestion}")
    print()
    
    # Display the optimized resume section
    print("📝 OPTIMIZED RESUME:")
    print("-"*50)
    print(result['optimized_resume'])
    print("-"*50)
    
    # Display detailed analysis section
    print("\n📊 DETAILED ANALYSIS:")
    print(result['analysis'])
    
    # Ask user if they want to save the optimized resume to a file
    save = input("\nWould you like to save the optimized resume to a file? (y/n): ")
    # Check if user wants to save (case-insensitive)
    if save.lower() == 'y':
        filename = input("Enter filename (default: optimized_resume.txt): ") or "optimized_resume.txt"
        with open(filename, 'w') as f:
            f.write(result['optimized_resume'])
        print(f"✅ Optimized resume saved to {filename}")
    
    print("\nThank you for using Resume Optimizer!")

# Check if this script is being run directly (not imported)
if __name__ == "__main__":
    main()
    
