import streamlit as st
import os
from optimizer import ResumeOptimizer
from document_processor import DocumentProcessor, validate_extracted_text
from dotenv import load_dotenv

# Load environment variables from .env file into the current environment
load_dotenv()

# Configure the Streamlit page settings and metadata
st.set_page_config(
    page_title="AI Resume Optimizer", 
    page_icon="📄", 
    layout="wide"
)

# Check if OpenAI API key is available in environment variables
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found! Please set your OPENAI_API_KEY environment variable.")
    # Stop execution of the app if no API key is found
    st.stop()

# Initialize the ResumeOptimizer class instance for use throughout the app
optimizer = ResumeOptimizer()
# Initialize the DocumentProcessor for handling file uploads
doc_processor = DocumentProcessor()

# Display the main title of the web application
st.title("AI Resume Optimizer")
# Display descriptive text about the application's functionality
st.markdown("""
This tool uses AI to optimize your resume for specific job descriptions.
It analyzes both documents and provides tailored recommendations to increase your chances of getting an interview.

**Supported resume formats:** PDF, DOCX, TXT
""")

# Create two columns for side-by-side input layout
col1, col2 = st.columns(2)

# Configure the left column for job description input
with col1:
    # Display subheader for the job description section
    st.subheader("Job Description")
    # Create a text area widget for job description input
    job_description = st.text_area(
        "Paste the job description here",  # Label for the text area
        height=300,  # Set height of text area in pixels
        placeholder="Copy and paste the job description you're applying for...",  # Placeholder text
        key="job_description_input"  # Unique key for this widget
    )

# Configure the right column for resume input
with col2:
    # Display subheader for the resume section
    st.subheader("Your Current Resume")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Upload File", "Paste Text"])
    
    # Initialize resume variable
    resume = ""
    
    # Tab 1: File Upload
    with tab1:
        # Create file uploader widget
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=['pdf', 'docx', 'txt'],
            help=f"Supported formats: {doc_processor.get_supported_formats_string()}"
        )
        
        # Process uploaded file if one is selected
        if uploaded_file is not None:
            st.info(f"📎 Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            # Show processing spinner while extracting text
            with st.spinner("Extracting text from your resume..."):
                try:
                    extracted_text = doc_processor.process_uploaded_file(uploaded_file)
                    
                    # Validate the extracted text
                    is_valid, error_message = validate_extracted_text(extracted_text)
                    
                    if is_valid:
                        # Set resume variable to extracted text
                        resume = extracted_text
                        st.success("Text extracted successfully!")
                        
                        # Show preview of extracted text
                        with st.expander("Preview extracted text"):
                            # Display first 500 characters of extracted text
                            preview_text = extracted_text[:500]
                            if len(extracted_text) > 500:
                                preview_text += extracted_text
                            st.text_area("Extracted content preview:", preview_text, height=150, disabled=True)
                    else:
                        # Show validation error
                        st.error(f" {error_message}")
                        
                except Exception as e:
                    # Show error message if text extraction fails
                    st.error(f" Error processing file: {str(e)}")
                    st.info("Try converting your file to PDF or paste the text manually in the 'Paste Text' tab.")
    
    # Tab 2: Manual Text Input
    with tab2:
        manual_resume = st.text_area(
            "Paste your resume content here",
            height=250,
            placeholder="Copy and paste your current resume text...",
            key="manual_resume_input" 
        )
        
        # Use manual input if no file was uploaded or if manual input is provided
        if manual_resume and not resume:
            resume = manual_resume

# Display current input status
if resume:
    char_count = len(resume)
    input_method = "File upload" if uploaded_file else "Manual input"
    st.info(f"Resume loaded ({char_count} characters) via {input_method}")

# Create the main action button for optimization
if st.button("Optimize Resume", type="primary", disabled=not (job_description and resume)):
    # Check if both required inputs are provided
    if not job_description or not resume:
        st.error("Both job description and resume are required!")
    else:
        with st.spinner("Optimizing your resume... This may take a while."):
            try:
                # Call the optimize_resume method with user inputs
                result = optimizer.optimize_resume(job_description, resume)
                
                # Check if optimization was successful
                if not result:
                    st.error("Failed to optimize resume. Please try again.")
                else:
                    st.session_state.optimization_result = result
                    
            except Exception as e:
                st.error(f" An error occurred: {str(e)}")

# Display results if available (either from current run or session state)
if 'optimization_result' in st.session_state:
    result = st.session_state.optimization_result
    
    # Create tabs for organizing the results display
    tab1, tab2, tab3 = st.tabs(["Optimized Resume", "Analysis", "Recommendations"])
    
    # Configure the first tab for displaying the optimized resume
    with tab1:
        st.subheader("Optimized Resume")
        
        # Create two columns for the optimized resume display
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Create a text area to display the optimized resume (read-only)
            st.text_area(
                "Your optimized resume:",  
                result['optimized_resume'],
                height=400,
                disabled=True
            )
        
        with col2:
            # Create download buttons for different formats
            st.markdown("### Download Options")
            
            # Download as TXT
            st.download_button(
                label="Download as TXT",
                data=result['optimized_resume'],
                file_name="optimized_resume.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Download as formatted text (with better formatting)
            formatted_resume = f"""OPTIMIZED RESUME
{'='*50}

{result['optimized_resume']}

{'='*50}
Generated by AI Resume Optimizer
Match Score: {result['score']}%
"""
            
            st.download_button(
                label="Download Formatted",
                data=formatted_resume,
                file_name="optimized_resume_formatted.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Configure the second tab for analysis and metrics
    with tab2:
        col1, col2 = st.columns([1, 2])
        
        # Configure the left column for metrics and keywords
        with col1:
            st.subheader("Match Score")
            st.metric("Score", f"{result['score']}%")
            st.progress(result['score'] / 100)
            
            # Display score interpretation
            if result['score'] >= 80:
                st.success("Excellent match!")
            elif result['score'] >= 60:
                st.info("Good match!")
            elif result['score'] >= 40:
                st.warning("Moderate match")
            else:
                st.error("Low match - needs improvement")
            
            # Display keyword matches
            st.subheader("🔑 Keyword Matches")
            if result['keyword_matches']:
                for keyword in result['keyword_matches']:
                    st.markdown(f"`{keyword}`")
            else:
                st.info("No specific keyword matches found")
        
        # Configure the right column for detailed analysis
        with col2:
            st.subheader("Detailed Analysis")
            # Display the detailed analysis text in an expandable container
            with st.container():
                st.write(result['analysis'])
    

    # Configure the third tab for improvement recommendations
    with tab3:
        st.subheader("Improvement Suggestions")
        
        # Check if there are suggestions available
        if result['suggestions']:
            for i, suggestion in enumerate(result['suggestions'], 1):
                # Create an expandable section for each suggestion
                with st.expander(f"Suggestion {i}", expanded=True):
                    # Display each suggestion with formatting
                    st.markdown(f"**{suggestion}**")
        else:
            st.info("No specific suggestions available.")
        
        # Add a section for general tips
        st.subheader("General Resume Tips")
        st.markdown("""
        - **Use action verbs**: Start bullet points with strong action verbs
        - **Quantify achievements**: Include numbers, percentages, and metrics
        - **Tailor keywords**: Match the language used in the job description
        - **Keep it concise**: Aim for 1-2 pages maximum
        - **Use consistent formatting**: Maintain uniform fonts, spacing, and style
        - **Proofread carefully**: Check for spelling and grammar errors
        """)

# Add footer with additional information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Powered by OpenAI GPT-4o | Built with Streamlit</p>
    <p>Tip: For best results, ensure your resume includes specific achievements and metrics</p>
</div>
""", unsafe_allow_html=True)

# Configure the sidebar with additional information and controls
st.sidebar.title("About App")
# Display informational text about the application
st.sidebar.info(
    "This app uses OpenAI's GPT-4o model to optimize resumes "
    "for specific job descriptions. It analyzes the content, "
    "identifies keywords, and suggests improvements to increase "
    "your chances of getting past ATS systems and impressing recruiters."
)

# Add sidebar section for supported formats
st.sidebar.markdown("### Supported Formats")
st.sidebar.markdown(f"**{doc_processor.get_supported_formats_string()}**")

# Add sidebar section for tips
st.sidebar.markdown("### Tips for Best Results")
st.sidebar.markdown("""
- Upload high-quality PDF files
- Ensure your resume has clear structure
- Include complete job descriptions
- Review AI suggestions before applying
""")

# Add clear results button in sidebar
if st.sidebar.button("Clear Results"):
    # Clear the optimization results from session state
    if 'optimization_result' in st.session_state:
        del st.session_state.optimization_result
    # Rerun the app to refresh the display
    st.rerun()