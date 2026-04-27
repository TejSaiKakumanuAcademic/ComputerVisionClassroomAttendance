# Reflection Notes on Agent Code Generation

Based on the analysis of `code_generation.md`, here are the answers to the reflection questions:

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
Prompts evolved from broad, goal-oriented requests into highly specific, constraint-driven instructions based on observed failures:
- **Adding Strict Constraints:** As the project grew, prompts started including defensive rules like: *"make sure you don't delete the unit test... nor mess with enroll, or attendence files at any point... make sure you don't create any new files."*
- **Describing Exact Formats:** Instead of saying "fix the csv," the prompt became specific: *"read the attendance csv to understand the format: date,time,Name"*.
- **Detailing the Logic Flow:** For complex edge cases, the prompts broke down the exact state machine required. For example, detailing the 3-step logic for handling duplicate names (alert user, ask to save/overwrite, implement specific naming convention while abstracting it from the logs).

### 4. Did using an AI Agent change how you approached software development?
Yes, the approach fundamentally shifted from **writing code** to **system architecture and QA testing**. 
Instead of spending time figuring out the syntax for OpenCV bounding boxes or CSV writing, the developer acted as a director and tester. The workflow became: define requirements -> AI generates code -> developer rigorously tests edge cases -> developer observes outputs (e.g., checking if the image was actually saved, or if the CSV had arrays instead of strings) -> developer writes a highly specific corrective prompt. The developer's primary job became maintaining the "big picture" state and closing logical loopholes that the AI didn't anticipate.

### 5. What risks do you see in over-reliance on AI Agents?
- **Silent Logic Failures and Data Loss:** As seen with the file-overwrite issue, AI will often implement the "happy path" without defensive programming. If developers don't thoroughly test edge cases, critical data could be lost or corrupted in production.
- **Integration Blind Spots:** The AI is context-bound to the prompt. It might create two perfectly functioning modules (Enrollment and Attendance) but fail to link them logically (enrolling doesn't mark attendance) unless explicitly told to do so.
- **Technical Debt via Formatting:** AI can generate "working" code that produces terrible artifacts. For instance, dumping massive numerical encoding arrays into the attendance CSV worked programmatically but was unreadable. Over-reliance without manual inspection can lead to heavily degraded data schemas.
- **Architectural Drift:** Without strict rules (like the ones added later in the prompts), AI may start creating redundant folders, hallucinating paths, or duplicating logic, which slowly degrades the project's structural integrity.
