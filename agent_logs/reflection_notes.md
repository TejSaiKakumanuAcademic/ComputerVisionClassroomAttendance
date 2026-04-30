# Reflection Notes on Agent Code Generation

### 1. Which tasks were most suitable for Gemini CLI?

The AI was most useful in writing code snippets that had a clearly defined input, output and goal, as well as in performing refactoring work and handling the implementation of discrete logic. For instance:

- **Implementing specific functions:** The AI successfully implemented the `enroll_face()` function in the `enroll.py` script with little human interaction besides the initial prompt.

- **Generating unit tests:** A single prompt was utilized to instruct the agent to implement unit tests for the `load_enrolled_faces()`, `recognize_faces_in_image()`, `is_face_enrolled()`, and `log_attendance()` functions, which it did easily.

- **Handling specific logic:** The agent handled creating logic to handle incremental file naming, as well as the regex to extract people's names from their file names.

- **Refactoring:** The agent was able to move the main code from the `test_basic.py` file into the `recognize.py` function when instructed to better match the desired project design.

### 2. Which tasks were least suitable?

The AI agent was less effective in tasks that required knowledge of the system as a whole, as well as situations that involved edge cases and managing the project environment. These tasks included:

- **System-wide logic:** The AI did not automatically make the connection that when a new user is enrolled, they should be logged as in attendance.

- **Handling edge cases:** Initially, the AI implemented code that would override an already existing user, which was not the desired output. Human input was necessary using further prompting to fix this issue.

- **Project structuring:** The AI tried using the relative path `../data/registered_faces`, which caused data to be stored in the wrong location as it did not have a full understanding of the ideal project structure.

- **Environment setup:** During development, there were issues with developers not having the required packages and the AI was unable to resolve these on its own, requiring human intervention.

### 3. How did you refine your prompts over time?
Prompts were at first very conversational and human-like, asking Gemini CLI to perform tasks as one would a coworker. As more prompts were generated, they took on a more managerial tone—treating Gemini CLI as a junior developer for whom we outlined code, which it then executed.
Techniques Used:
- **Management Prompts**
Instead of being conversational with Gemini, we provided strict instructions for generation, outlining expectations for how the scripts should interact. This gave Gemini prompts more structure. 
Example: *"This script should use a passed in array of results from recognize.py to append to the attendance_log.csv with an entry. An entry should be in this format: face_encoding, face_name, timestamp."*

- **Negative Prompts** 
As the project grew, Gemini required more guidance on what not to do; we utilized **Negative Prompts** to refine Gemini's scope.
Example: *"make sure you don't delete the unit test... nor mess with enroll, or attendence files at any point... make sure you don't create any new files."*

- **Referencing Project Files:** 
Once the project contained existing files, Gemini could read them directly instead of requiring descriptions of finished scripts.
Example: *"read the attendance csv to understand the format: date,time,Name"*.

### 4. Did using an AI Agent change how you approached software development?
Yes. In earlier classes, the focus was on syntax and how to write code. When working with Gemini CLI, it is more effective to act as an architect, leaving the syntax to Gemini while the developer handles the program's design.

Normally, to use a library, a developer must read documentation to find relevant function calls. Gemini can parse documentation and identify the most relevant functions quickly. This allows the developer more time to plan the program. In this project, we used OpenCV; rather than spending hours learning the library, Gemini was able to write the implementation almost instantly.

### 5. What risks do you see in over-reliance on AI Agents?

Throughout our project, we realised that AI is still not perfect with a lot of things. If we don't pay attention to what is being implemented by AI, it is highly likely that AI would cause some disastrous mistakes like file overwriting which could lead to loss of critical data in production phase. We also observed that AI is really not very robust regarding analysing the whole project's context before implementing a new file. For example, when we asked the AI to implement the enroll function, it just focused on implementing the enroll function rather than understand the project structure and creating a logic to also mark the student in attendance. This indicates that majority of the agent's context window is filled with the details included in the prompt. Which means it is crucial for developers to append strict rules into their prompts that guide the agent appropriately.

