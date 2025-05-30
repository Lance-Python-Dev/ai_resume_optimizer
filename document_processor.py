"""
Document processing utilities for extracting text from various file formats.
Supports PDF, DOCX, and TXT files for resume upload functionality.
"""

import io
import PyPDF2 
import docx  
import pdfplumber 
import streamlit as st  

class DocumentProcessor:
    """
    A class to handle document processing and text extraction from various file formats.
    Supports PDF, DOCX, and plain text files.
    """
    
    def __init__(self):
        """Initialize the DocumentProcessor class."""
        # Define supported file types and their extensions
        self.supported_types = {
            'pdf': ['.pdf'],
            'docx': ['.docx', '.doc'],
            'txt': ['.txt']
        }
    
    def get_file_type(self, filename):
        """
        Determine the file type based on the filename extension.
        
        Args:
            filename (str): Name of the uploaded file
            
        Returns:
            str: File type ('pdf', 'docx', 'txt', or 'unsupported')
        """
        # Convert filename to lowercase for case-insensitive comparison
        filename_lower = filename.lower()
        
        # Check each supported file type
        for file_type, extensions in self.supported_types.items():
            # Check if filename ends with any of the extensions for this type
            for ext in extensions:
                if filename_lower.endswith(ext):
                    return file_type
        
        # Return 'unsupported' if no matching extension found
        return 'unsupported'
    
    def extract_text_from_pdf_pypdf2(self, pdf_file):
        """
        Extract text from PDF using PyPDF2 library.
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Create a PDF reader object from the uploaded file
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Initialize empty string to store extracted text
            text = ""
            
            # Iterate through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the current page
                page = pdf_reader.pages[page_num]
                # Extract text from the page and add to our text string
                text += page.extract_text() + "\n"
            
            # Return the extracted text
            return text.strip()
            
        except Exception as e:
            # Raise exception with descriptive error message
            raise Exception(f"Error extracting text from PDF with PyPDF2: {str(e)}")
    
    def extract_text_from_pdf_pdfplumber(self, pdf_file):
        """
        Extract text from PDF using pdfplumber library (more robust).
        
        Args:
            pdf_file: Uploaded PDF file object
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Reset file pointer to beginning
            pdf_file.seek(0)
            # Initialize empty string to store extracted text
            text = ""
            
            # Open PDF with pdfplumber
            with pdfplumber.open(pdf_file) as pdf:
                # Iterate through each page
                for page in pdf.pages:
                    # Extract text from current page
                    page_text = page.extract_text()
                    # Add page text if it exists
                    if page_text:
                        text += page_text + "\n"
            
            # Return the extracted text
            return text.strip()
            
        except Exception as e:
            # Raise exception with descriptive error message
            raise Exception(f"Error extracting text from PDF with pdfplumber: {str(e)}")
    
    def extract_text_from_docx(self, docx_file):
        """
        Extract text from Word document (.docx) files.
        
        Args:
            docx_file: Uploaded DOCX file object
            
        Returns:
            str: Extracted text from the document
        """
        try:
            # Create a Document object from the uploaded file
            doc = docx.Document(docx_file)
            # Initialize empty list to store paragraph text
            text_parts = []
            
            # Iterate through each paragraph in the document
            for paragraph in doc.paragraphs:
                # Add paragraph text to our list
                text_parts.append(paragraph.text)
            
            # Join all paragraphs with newlines and return
            return "\n".join(text_parts).strip()
            
        except Exception as e:
            # Raise exception with descriptive error message
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_text_from_txt(self, txt_file):
        """
        Extract text from plain text files.
        
        Args:
            txt_file: Uploaded TXT file object
            
        Returns:
            str: Content of the text file
        """
        try:
            # Read the file content and decode as UTF-8
            content = txt_file.read().decode('utf-8')
            # Return the content stripped of leading/trailing whitespace
            return content.strip()
            
        except UnicodeDecodeError:
            # Try alternative encoding if UTF-8 fails
            try:
                # Reset file pointer and try latin-1 encoding
                txt_file.seek(0)
                content = txt_file.read().decode('latin-1')
                return content.strip()
            except Exception as e:
                # Raise exception if both encodings fail
                raise Exception(f"Error reading text file with multiple encodings: {str(e)}")
        except Exception as e:
            # Raise exception for other errors
            raise Exception(f"Error extracting text from TXT: {str(e)}")
    
    def process_uploaded_file(self, uploaded_file):
        """
        Main method to process an uploaded file and extract text.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text from the file
        """
        # Check if a file was actually uploaded
        if uploaded_file is None:
            raise Exception("No file uploaded")
        
        # Get the file type based on filename
        file_type = self.get_file_type(uploaded_file.name)
        
        # Process based on file type
        if file_type == 'pdf':
            # Try pdfplumber first (more robust), fall back to PyPDF2
            try:
                return self.extract_text_from_pdf_pdfplumber(uploaded_file)
            except Exception:
                # Reset file pointer for second attempt
                uploaded_file.seek(0)
                return self.extract_text_from_pdf_pypdf2(uploaded_file)
                
        elif file_type == 'docx':
            # Process Word document
            return self.extract_text_from_docx(uploaded_file)
            
        elif file_type == 'txt':
            # Process plain text file
            return self.extract_text_from_txt(uploaded_file)
            
        else:
            # Raise exception for unsupported file types
            raise Exception(f"Unsupported file type. Supported formats: PDF, DOCX, TXT")
    
    def get_supported_formats_string(self):
        """
        Get a formatted string of supported file formats for display.
        
        Returns:
            str: Comma-separated list of supported formats
        """
        # Flatten all extensions into a single list
        all_extensions = []
        for extensions in self.supported_types.values():
            all_extensions.extend(extensions)
        
        # Convert to uppercase and join with commas
        return ", ".join([ext.upper() for ext in all_extensions])

def validate_extracted_text(text):
    """
    Validate that extracted text is suitable for resume processing.
    
    Args:
        text (str): Extracted text from document
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if text is empty or too short
    if not text or len(text.strip()) < 50:
        return False, "The extracted text is too short. Please ensure your resume has sufficient content."
    
    # Check if text contains common resume keywords (basic validation)
    resume_keywords = [
        'experience', 'education', 'skills', 'work', 'employment', 
        'university', 'college', 'degree', 'certification', 'project'
    ]
    
    # Convert text to lowercase for keyword checking
    text_lower = text.lower()
    
    # Check if at least one resume keyword is present
    has_resume_content = any(keyword in text_lower for keyword in resume_keywords)
    
    if not has_resume_content:
        return False, "The document doesn't appear to contain typical resume content. Please verify you uploaded the correct file."
    
    # If all checks pass, return valid
    return True, ""