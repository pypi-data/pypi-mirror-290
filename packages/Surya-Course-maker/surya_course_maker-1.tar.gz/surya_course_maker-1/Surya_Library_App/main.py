import os
import re
from fpdf import FPDF
from rich.console import Console
from webscout import LLAMA3, exceptions
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCursor
import fitz  # PyMuPDF


print("""
 ___                       _    _  _                       
/ __> _ _  _ _  _ _  ___  | |  <_>| |_  _ _  ___  _ _  _ _ 
\__ \| | || '_>| | |<_> | | |_ | || . \| '_><_> || '_>| | |
<___/`___||_|  `_. |<___| |___||_||___/|_|  <___||_|  `_. |
               <___'                                  <___'
""")

console = Console()

BASE_SAVE_DIR = os.getcwd()

system_prompt = """
You are an exceptionally knowledgeable and patient AI tutor, capable of teaching any subject at any level of complexity. Your role is to create comprehensive, engaging, and deeply informative courses on various topics. When generating course content:

1. Provide thorough explanations that cover both fundamental concepts and advanced ideas.
2. Use clear, accessible language while maintaining academic rigor.
3. Incorporate a variety of teaching methods to cater to different learning styles.
4. Include numerous examples, analogies, and real-world applications to illustrate concepts.
5. Address potential misconceptions and common errors in understanding.
6. Encourage critical thinking and deeper exploration of the subject matter.
7. Maintain an encouraging and supportive tone throughout your teaching.

Your goal is to ensure that learners gain a complete and nuanced understanding of the topic, equipping them with the knowledge to apply concepts in various contexts and to pursue further learning independently.
"""

LLAMA3_client_model_1 = LLAMA3(
    is_conversation=False,
    timeout=1000000,
    max_tokens=8028,
    intro=system_prompt,
    system=system_prompt,
    model='llama3-8b'
)

LLAMA3_client_model_2 = LLAMA3(
    is_conversation=False,
    timeout=1000000,
    max_tokens=8028,
    intro=system_prompt,
    system=system_prompt,
    model='llama3-8b'
)

def generate_course(topic: str) -> dict:
    course_prompt = f"""
    Develop a comprehensive and in-depth course outline for the topic '{topic}'. The course should cater to beginners while also covering advanced concepts. Please provide:

    1. An engaging and thorough introduction to the topic (5-6 sentences):
       - Explain the significance of the topic
       - Briefly outline its historical context
       - Mention its relevance in contemporary contexts

    2. 8-10 main lessons or subtopics, organized in a logical learning sequence:
       - Ensure a smooth progression from foundational to advanced concepts
       - Include both theoretical and practical aspects of the topic

    3. For each lesson/subtopic:
       - Provide a clear and detailed description (4-5 sentences)
       - List 5-7 key concepts to be covered
       - Include 2-3 learning objectives
       - Suggest a practical example or real-world application
       - Propose a thought-provoking question or discussion point

    4. A comprehensive conclusion (5-6 sentences):
       - Summarize the main points covered in the course
       - Explain how the knowledge gained can be applied
       - Suggest areas for further study or exploration

    Format your response as a structured outline with clear headings and subheadings. Use markdown formatting for better readability.

    Example structure:
    # Course: [Topic]

    ## Introduction
    [Thorough introduction to the topic]

    ## Lesson 1: [Subtopic 1]
    - Description: [Detailed description of the lesson]
    - Key concepts: [List of 5-7 key concepts]
    - Learning objectives: [2-3 specific learning objectives]
    - Practical example: [Real-world application or example]
    - Discussion point: [Thought-provoking question]

    [Repeat for each lesson]

    ## Conclusion
    [Comprehensive summary and future directions]
"""
    try:
        course_response = LLAMA3_client_model_1.chat(prompt=course_prompt)
        return {"course_outline": course_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate course outline: {e}"}

def generate_lesson(course_topic: str, subtopic: str) -> dict:
    lesson_prompt = f"""
    Create a comprehensive and engaging lesson for the subtopic '{subtopic}' in the course about {course_topic}. Your lesson should be thorough, leaving no stone unturned in explaining the topic. Include:

    1. Introduction (1 paragraph):
       - Explain the significance of this subtopic within the broader course
       - Outline what the learner will gain from this lesson

    2. Historical Context (1-2 paragraphs):
       - Provide a brief history of the concept or theory
       - Explain how understanding has evolved over time

    3. Learning Objectives (4-6 clear, measurable objectives for the lesson)

    4. Key Concepts (list 6-8 main ideas with detailed explanations):
       - Define each concept clearly
       - Explain how these concepts interconnect

    5. In-depth Explanation:
       - Provide a comprehensive explanation of the subtopic (4-6 paragraphs)
       - Use multiple analogies or metaphors to explain complex ideas
       - Include mathematical formulas or scientific principles where applicable
       - Address common misconceptions or challenges related to the topic
       - Explain how this subtopic relates to other areas of the main topic

    6. Real-world Examples and Applications:
       - Include at least three detailed practical examples relevant to the subtopic
       - Explain how these examples illustrate the concepts
       - Discuss potential real-world applications or technologies based on these concepts

    7. Interactive Elements:
       - Suggest 2-3 hands-on activities, thought experiments, or mini-projects related to the topic
       - Provide step-by-step instructions for at least one of these activities

    8. Case Studies (if applicable):
       - Present 1-2 relevant case studies that demonstrate the application of the concepts
       - Analyze these cases to reinforce understanding

    9. Summary (1 paragraph summarizing the main points and their significance)

    10. Further Reading:
        - Suggest 4-5 resources (books, articles, videos, research papers) for students who want to explore the topic further
        - Briefly explain what each resource offers

    11. Reflection and Critical Thinking:
        - Provide 3-4 thought-provoking questions to encourage critical thinking about the topic
        - Suggest potential areas for future research or exploration in this subtopic

    Format your response using markdown for better readability and structure. Use headings, subheadings, bullet points, and numbered lists to organize the content clearly.

"""
    try:
        lesson_response = LLAMA3_client_model_1.chat(prompt=lesson_prompt)
        return {"lesson_content": lesson_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate lesson content: {e}"}

def generate_quiz(course_topic: str, subtopic: str) -> dict:
    quiz_prompt = f"""
    Design a comprehensive and challenging quiz to evaluate deep understanding of the lesson on '{subtopic}' in the {course_topic} course. The quiz should test not only recall but also application, analysis, and synthesis of knowledge. Include:

    1. 8 Multiple-choice Questions:
       - Ensure questions cover different aspects of the subtopic
       - Include at least three questions that require application of knowledge to new situations
       - One question should involve interpreting a graph, diagram, or data set related to the topic

    2. 3 True/False Questions:
       - Make sure these questions address common misconceptions
       - Include a "justify your answer" component for each T/F question

    3. 4 Short Answer Questions:
       - Two questions should test basic understanding and recall
       - Two questions should require deeper analysis, synthesis, or application of concepts

    4. 2 Essay Questions:
       - One question should ask for an in-depth explanation of a core concept
       - One question should require the student to apply multiple concepts to analyze a complex scenario

    5. 1 Numerical Problem (if applicable to the topic):
       - Present a problem that requires quantitative reasoning and calculation
       - Provide step-by-step instructions for solving

    For each question:
    - Provide the correct answer
    - Include a detailed explanation of why the answer is correct
    - For incorrect options in multiple-choice questions, explain why they are wrong
    - Suggest further areas of study related to each question

    Format your response using markdown for better readability and structure. Use headings and subheadings to organize the content clearly.

"""
    try:
        quiz_response = LLAMA3_client_model_2.chat(prompt=quiz_prompt)
        return {"quiz_content": quiz_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate quiz content: {e}"}

def generate_pdf(content: str, file_path: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(file_path)

def create_course_structure(topic: str) -> None:
    topic_dir = os.path.join(BASE_SAVE_DIR, topic.replace(" ", "_"))

    if not os.path.exists(topic_dir):
        os.makedirs(topic_dir)

    course_data = generate_course(topic)
    if "error" in course_data:
        console.log(f"[red]Error generating course outline: {course_data['error']}[/red]")
        return

    outline_filename = os.path.join(topic_dir, "course_outline.pdf")
    generate_pdf(course_data["course_outline"], outline_filename)

    lessons = extract_subtopics(course_data["course_outline"])
    for index, subtopic in enumerate(lessons, start=1):
        lesson = generate_lesson(topic, subtopic)
        if "error" in lesson:
            console.log(f"[red]Error generating lesson for subtopic '{subtopic}': {lesson['error']}[/red]")
            continue

        lesson_filename = os.path.join(topic_dir, f"lesson{index:02d}_{subtopic.replace(' ', '_').lower()}.pdf")
        generate_pdf(lesson["lesson_content"], lesson_filename)

        quiz = generate_quiz(topic, subtopic)
        if "error" in quiz:
            console.log(f"[red]Error generating quiz for subtopic '{subtopic}': {quiz['error']}[/red]")
            continue

        quiz_filename = os.path.join(topic_dir, f"quiz{index:02d}_{subtopic.replace(' ', '_').lower()}.pdf")
        generate_pdf(quiz["quiz_content"], quiz_filename)

    console.log(f"[green]Course structure for '{topic}' created successfully in {topic_dir}![/green]")

def extract_subtopics(course_outline: str) -> list:
    subtopics = re.findall(r'^## Lesson \d+: (.+)$', course_outline, re.MULTILINE)
    return subtopics

class LibrarianApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Library")
        self.setGeometry(100, 100, 1200, 900)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QLabel, QLineEdit, QPushButton, QListWidget {
                font-size: 16px;
            }
            QLabel, QPushButton {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #888888;
            }
            QPushButton {
                background-color: #888888;
                border: none;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #aaaaaa;
            }
            QListWidget {
                background-color: #444444;
                border: 1px solid #888888;
            }
            QTextEdit {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #888888;
                font-size: 14px;
                padding: 10px;
            }
        """)

        self.header_label = QLabel("Virtual Library", self)
        self.header_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Enter Topic:", self)
        self.input = QLineEdit(self)
        self.button = QPushButton("Generate Course", self)
        self.button.clicked.connect(self.generate_course)

        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.display_pdf)

        self.pdf_viewer = QTextEdit(self)
        self.pdf_viewer.setReadOnly(True)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.pdf_viewer)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def generate_course(self):
        topic = self.input.text()
        if topic:
            create_course_structure(topic)
            self.load_pdfs(topic)

    def load_pdfs(self, topic: str):
        topic_dir = os.path.join(BASE_SAVE_DIR, topic.replace(" ", "_"))
        if os.path.exists(topic_dir):
            self.list_widget.clear()
            for file_name in os.listdir(topic_dir):
                if file_name.endswith('.pdf'):
                    item = QListWidgetItem(file_name.replace('.pdf', '').replace('_', ' ').title())
                    item.setData(Qt.UserRole, os.path.join(topic_dir, file_name))
                    self.list_widget.addItem(item)

    def display_pdf(self, item):
        pdf_path = item.data(Qt.UserRole)
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.pdf_viewer.setText(text)
        self.pdf_viewer.moveCursor(QTextCursor.Start)

def Main():
    app = QApplication([])
    window = LibrarianApp()
    window.show()
    app.exec_()
    