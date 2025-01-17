import cv2
import pytesseract
import re
import os

# Function to extract text using Tesseract OCR

def extract_text(image_path):
     img = cv2.imread(image_path)
     
    #  cv2.imshow("Answer", img)   to open the image in another window
    #  cv2.waitKey(0)
    #  cv2.destroyAllWindows()

     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      # Additional preprocessing steps
     gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
     gray = cv2.GaussianBlur(gray, (5, 5), 0)
     gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] 
     # Configure Tesseract to use English language and adjust settings
     config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:' 
     text = pytesseract.image_to_string(gray, config=config) 
     return text
# Function to extract answers from the text using regex
def extract_answers(extracted_text):
    # Define a regex pattern for detecting answers (e.g., "Q1: C")

    answer_pattern = re.compile(r'Q(\d+).*?Ans:\s*([A-D])', re.DOTALL | re.IGNORECASE)
    answers = {}
    for match in answer_pattern.findall(extracted_text):
        question_number, answer = match
        answers[f"Q{question_number}"] = answer.upper()
    return answers

# Function to read correct answers from a ttext file
def read_correct_answers(file_path):
    correct_answers = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    question, answer = line.split(':')
                    correct_answers[question.strip()] = answer.strip().upper()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading correct answers: {e}")
    return correct_answers

# Function to evaluate the answers
def evaluate_answers(answers, correct_answers):
    score = 0
    for question, correct_answer in correct_answers.items():
        if answers.get(question) == correct_answer:
            score += 1
    return score

# Main function to drive the script
def main():
    image_path = 'images/Ravi_ans.jpg'
    

    correct_answer_path ='correct_ans/answers.txt'    

    correct_answers= read_correct_answers(correct_answer_path)

    if not correct_answers:
        print("Failed to read correct answers. Exiting...")
        return
    
    # Extract the text from the answer sheet image
    extracted_text = extract_text(image_path)
    print(f"Extracted Text:\n{extracted_text}")
    
    # Evaluate the answers based on the extracted text
    answers = extract_answers(extracted_text)
    print(f"Extracted Answers: {answers}")
    
    score = evaluate_answers(answers, correct_answers)
    
    # Output the score
    print(f"Total Score: {score}/{len(correct_answers)}")

   
    # Save the score to a file
    os.makedirs('output', exist_ok=True)   # Ensure the output directory exists
    with open('output/score.txt', 'w') as f:
        f.write(f"Total Score: {score}/{len(correct_answers)}\n")

if __name__ == "__main__":
    main()
