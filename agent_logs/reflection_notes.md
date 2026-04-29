# Reflection Notes on Agent Code Generation

### 1. Which tasks were most suitable for Gemini CLI?
The AI agent excelled at tasks that involved discrete logic implementation, localized refactoring, and writing boilerplate code given clear input/output requirements. Specifically:
- **Writing isolated functions and algorithms:** Implementing the core math for distance calculations (`is_face_enrolled`), or setting up standard OpenCV camera streams.
- **Generating Unit Tests:** Creating mock data and assertions for functions like `test_enroll_face` based on clear guidelines.
- **Formatting and Data Transformation:** Parsing date/time strings to fix the CSV schema, or stripping arrays from logs.
- **Regex and File Handling:** Creating logic to handle file naming increments (`name_1`, `name_2`) and extracting base names for the attendance system.
- **Direct Refactoring:** Moving the execution loop from `test_basic.py` into a `main()` function in `recognize.py` when explicitly instructed.

### 2. Which tasks were least suitable?
Tasks requiring holistic system awareness, environment management, and anticipating real-world edge cases were less successful. Specifically:
- **System Integration & Logical Gaps:** The AI failed to realize that newly enrolled users should immediately be logged as present for the day. This required manual intervention and a follow-up prompt.
- **Handling Destructive Edge Cases:** When enrolling a duplicate name, the AI's initial implementation silently overwrote the existing image file, destroying data. It required the user to notice this during testing and explicitly demand a prompt-and-save-as-new workflow.
- **Project Structure Consistency:** The AI initially hallucinated a relative path `../data/registered_faces` and later created redundant directories because it didn't intrinsically understand the developer's desired global folder structure.
- **Environment Setup:** Python environment errors (like missing OpenCV or `face_recognition` packages) were encountered during execution, which the AI code generation process could not natively resolve without developer environment management.

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

