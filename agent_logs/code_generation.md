# Agent Code Generation Logs

## Task: Generate Recognise Function

Prompt:
"Implement src/recognise.py to accept a face and check if the face is already enrolled or not."

Result:

- Created the functions `load_enrolled_faces()` and `is_face_enrolled()` within `src/recognize.py`.
- `load_enrolled_faces()` iterates through the `data/registered_faces` directory and caches the face encodings and names from loaded images.
- `is_face_enrolled()` calculates the facial distance between an input image and the pre-loaded known encodings to find the closest match.

Human Action:

- Read through the generated code to ensure it matched the design specifications.
- Verified that the distance calculation logic uses a correct tolerance threshold to determine if a face matches.

---

## Task: Real-time Camera Testing

Prompt:
"can you also implement testbasic.py where I can run recognise and get an output on whether or not the face is recognised. make it use my camera for real time tetsing"

Result:

- Implemented the `main()` function in `tests/test_basic.py` to initialize an OpenCV `cv2.VideoCapture(0)` stream.
- Modified `is_face_enrolled()` to optionally accept cached `known_encodings` and `known_names`, preventing severe I/O bottleneck operations on every video frame.

Human Action:

- Attempted to execute `tests/test_basic.py` using my local Python environment to view the webcam output.
- Discovered that the required Python packages (`opencv-python`, `face_recognition`) were throwing import errors and not correctly installed or linked to the workspace environment.

---

## Task: UI Boxes, Frame Extraction, and FPS Boost

Prompt:
"if it is not recognised, can you make a code to cut the specific frame out and send the encoding of that face as a return value batch? I also want you to show the frame that you are cutting on the video screen with the appropriate color instead of saying unknown on the top. Also the video has very few frames, can you try making it 60frames per second? is it too much to ask?"

Result:

- Integrated frame resizing (`fx=0.25, fy=0.25`) in `tests/test_basic.py` prior to passing frames to the recognition model, greatly increasing the frames-per-second (FPS) output.
- Added `cv2.rectangle` and `cv2.putText` logic to draw dynamic green bounding boxes around recognized faces, and red boxes for unrecognized individuals.

Human Action:

- Tested the live video feed and observed the FPS was significantly smoother.
- Confirmed that bounding boxes correctly tracked my face and correctly labeled me as 'Unknown' with a red box since I was not enrolled.

---

## Task: Identity Clustering (Short-Term Memory)

Prompt:
"I just ran it and I was the only person in front of the camera and it said Collected data for 669 unknown face frames.
Returning batch of 669 unknown encodings/frames.

I am wondering if it will know it was only one person or it will think each face is different? does it matter?"

Result:

- Refactored `src/recognize.py` by introducing a new function `recognize_faces_in_image()` which returns a dictionary of face locations, names, and encodings for all detected faces in a single pass.
- Implemented an identity clustering loop in `tests/test_basic.py` which computes the distance between new unknown encodings and a `tracked_unknowns` list, grouping sequential frames of the same unknown person into a single "Guest X" identity.

Human Action:

- Walked in front of the camera and verified that the system accurately tracked me as a single "Guest 1" entity rather than spawning hundreds of unique unknown profiles.
- Asked the AI conceptual questions regarding how the face encoding model manages varying angles and distances.

---

## Task: Prep for Future Enrollment

Prompt:
"so let's say an unknown face is found and the unknoen encoding is passed into enroll, how will enroll prompt the user to give the name? I am asking because the user won't know how to read the encoding right? how does this work?

I am thinking if we can temporirly save faces into new and save the respective frame into that so that we can recall it via enroll when asking the user for name?

Is this the best way to do it?"

"so I must not deal with enroll.py so we should forget about that but we should do everything in recognise to make sure the interface is set for enroll.py and attendance.py.

We run test_basic.py, walk into the frame until identified as "Guest 1", and hit q.
We check inside data/faces/new to verify that Guest_1.jpg was written clearly.

So just implemnt techniques for above two steps"

Result:

- Updated the exit routine in `tests/test_basic.py` to utilize `cv2.imwrite`.
- Configured the script to safely extract the highest-quality cropped matrix (`best_crop`) of each clustered guest and save it into the `data/faces/new/` directory as a JPEG file upon video termination.

Human Action:

- Verified that a clear `Guest_1.jpg` image was successfully written to the directory, ensuring the offline enrollment pipeline had valid input data to process later.

---

## Task: Generrate Code for Attendance.py

Prompt:
"Please generate code for the attendance.py script. This script should use a passed in array of results from recognize.py to append to the attendance_log.csv with an entry. An entry should be in this format: face_encoding, face_name, timestamp. Also, generate a get_current_date function inside of the utils.py. It should be used to grab the time at the time of attendance logging."

Result
- Created a simple getcurrentdate function in Utils.py
- Created the log_attendance function inside of attendance

Human Action:
- Verfied syntax and logic flow. Tested the code and verifed it worked. Successfully appended log.

---

## Task: Generate Enrollment Function

Prompt:
"Implement a function in enroll.py that will take in the cropped image of a person's face along with the person's name, stores the image in the "../data/registered_faces" directory using the person's name as the file name, and enforces a file extension of PNG or JPEG."

Result:

- A function `enroll_face()` was created which takes in an image of a single person's face in the format provided by the `recognize.py` functions, as well as the name of this person.
- This function saves the provided image using the name of the person as the file name, and enforces a file type of either PNG or JPEG, defaulting to PNG.

Human Action:

- Prompted the AI to achieve a specific and measurable goal, which aligns with the overall design of the project and the pre-existing facial recognition code.

---

## Task: Generate Enrollment Unit Test Case

Prompt:
"Implement a pytest unit test for the `enroll_face` function in the `test_basic.py` file. This unit test should create some mock cropped image in the format expected by the function, passing it on along with a fake name for the person. The unit test should ensure that after the function is called, the file exists, and when loaded matches the mock cropped face you created."

Result:

- A function `test_enroll_face()` was created in the `test_basic.py` file, which can be executed using `pytest tests/test_basic.py::test_enroll_face`, a command also provided by the AI.
- The unit test creates a mock image using a matrix-like data format, as is used internally by `cv2`, and calls the `enroll_face()` function.
- The test function ensures the image file was saved successfully, is able to be loaded, is of the correct size, and matches the mock input image.

Human Action:

- Prompted the AI to implement a specific unit test where the `enroll_face()` function can be tested effectively without worrying about the exact implementation details of how to create mock data or ensure the saved file matches the input file.
- Ran the unit test case, which passed successfully.

---

## Task: Fix Relative Directory Path

Prompt:
"The `enroll_face()` function in `enroll.py` incorrectly stores output in a data directory that is outside of the current workspace. Fix the output directory so it stores the faces within this workspace under the existing `data` directory in a (possibly new) folder named `registered_faces`."

Result:

- The `enroll_face()` function was modified to stop pointing statically to the `../data/registered_faces` directory, instead building the path from the project root to the `data` directory and then the `registered_faces` subdirectory.
-

Human Action:

- Recognized that when running the unit test generated previously, there is never any file output seen during the execution or a trace of the `registered_faces` directory afterwards.
- Located the `data/registered_faces` directory outside of the project workspace.
- Instructed the AI that currently the code points to the wrong location, and that it instead must store files in a directory `data/registered_faces` within the workspace.
- Ran the unit test once again and confirmed that the file is stored in the correct location during execution.

---

Task: Rearranging Files and Adding Unit Tests
Prompt: "I want to make some rearrangements to fix some design mistakes for this project. First I want you to move main running related stuff in tests/test_basic.py into a main function inside revognise.py. Then, populate testbasic with unittests for other functions which doesn't have unit tests. Also make sure you don't delete the unit test that is already in the testbasic, nor mess with enroll, or attendence files at any point. This rule hold for any prompt in this chat. If you need to make any changes to those particular files let me know first and also make sure you don't create any new files in the project directory since we must maintian the standard format"

Result:
- Abstracted the primary camera feed loop out of `test_basic.py` and encapsulated it within a structured `main()` execution block inside `src/recognize.py`.
- Developed mock-data unit tests in `test_basic.py` for `load_enrolled_faces`, `recognize_faces_in_image`, `is_face_enrolled`, and `log_attendance` to establish comprehensive structural code coverage.

Human Action:
- Analyzed the refactored project architecture to verify the clean separation of concerns between test automation modules and the primary executable logic.
- Noticed that the main function was still automatically dumping unknown faces into a folder without user interaction, which felt disjointed from a real-world enrollment workflow.
- Decided to pivot the design toward an interactive CLI prompt to guide the user through enrolling unknown guests immediately after the camera session ends.

---

Task: Interactive Enrollment in Terminal
Prompt: "Now, the main funciton has a logic to save the unknown faces found in the attendance video detection. I want you to make sure it doesn't save it but just after the detection period is over(when pressed q in the video) the user should be prompted to input the names of the people who were unknown. They should also have the option to choose between not enrolling or enrolling. If enroll the then we should call the enroll funciton to regester the face. If known faces are found it should call attendance to mark that someone is present on a particular day."

Result:
- Deprecated the automated file dump system for unrecognized identities.
- Developed an interactive state loop utilizing `cv2.imshow` and standard `input()` streams to prompt users dynamically.
- Implemented logical branching to pipe recognized outputs directly into `log_attendance()` and user-confirmed unknowns directly into `enroll_face()`.

Human Action:
- Tested the interactive loop to ensure the state machine properly iterated through tracked guests and handled the standard I/O streams smoothly.
- Inspected the project directory tree after a successful enrollment and realized the script had created a redundant `registered_faces` directory alongside the main `faces` folder.
- Recognized this violated the existing structural constraint to keep all data centralized, prompting a needed path correction.

---

Task: Modifying Enrollment Directory
Prompt: "I need the regestered faces go inside faces itself instead of regestered face directory. I shouldn't edit the project format remember
edit enroll.py"

Result:
- Refactored the hardcoded `output_dir` string inside `src/enroll.py` to point directly to `data/faces`.
- Updated all default keyword parameters across `src/recognize.py` (`load_enrolled_faces(enrolled_dir="../data/faces")`) to utilize the newly unified data directory structure.

Human Action:
- Verified that the `data/registered_faces` directory path was successfully deprecated and files were correctly routing exclusively to `data/faces`.
- Ran a complete enrollment test and cross-checked the daily attendance CSV.
- Discovered a logical gap: successfully enrolling a new identity did not retroactively mark them as present for the current session, meaning their attendance data for day one was lost.

---

Task: Linking Interactive Enrollment to Attendance
Prompt: "I also want to make sure after an unknown person is enrolled, they must be marked for attendance on that day"

Result:
- Injected a `log_attendance()` hook directly following the `enroll_face()` execution block within the interactive loop in `src/recognize.py`.
- Passed the freshly captured identity data (the pure name key and the first stored encoding matrix) to the logger to ensure state synchronization for new enrollments.

Human Action:
- Checked the CSV logging behavior to ensure newly enrolled user identities were instantly captured and serialized for the current operational day.
- Opened `attendance_log.csv` to review the newly inserted rows and noticed the file was cluttered with massive numerical arrays representing the facial encodings instead of a clean, readable timestamp.
- Realized the logger was misaligned with the standard `Date, Time, Name` requirements, necessitating a strict formatting cleanup.

---

Task: Re-formatting Attendance CSV
Prompt: "we don't need the encoding in attendance read the attendance csv to understnad the format: date,time,Name"

Result:
- Stripped the facial encoding list array serialization from the `src/attendance.py` writer logic.
- Parsed the `get_current_date()` string (`%Y-%m-%d %H:%M:%S`) and split it into distinct `Date` and `Time` string variables.
- Aligned the `csv.writer.writerow()` method to strictly conform to the expected `[Date, Time, Name]` column matrix requirement.

Human Action:
- Inspected the generated CSV artifact and confirmed the massive data arrays were successfully stripped, leaving perfectly clean schema alignment.
- Conducted an edge-case test by attempting to enroll the same person twice using an identical name key to see how the script handled duplicates.
- Observed that the system silently overwrote the original facial image file without warning, effectively destroying the previous snapshot.
- Recognized the critical need for a protective overwrite-warning system and a robust naming convention to allow tracking multiple frames for a single identity without corrupting the logs.

---

Task: Multiple Frames and Overwrite Logic
Prompt: "in the main function, if we give a known name that is already inside the folder/enrolled, it seems to be over writing the original image. so the following are the things that needs to be taken care of:

1. We need to alert the user as soon as a same name is found. 
2. We need to ask them if they would want to save as a different frame of the same person(because ai recognises faces differently when turned other sides) or overwrite the exisiting person completely, with a caution message
3. For saving as different frame come up with good naming convention and when recognising the faces, the added convention for recognising the same face should not appear on the window or even for the attendance, it should not appear as two different people.

For example, if we have a name enrolled as rando already and we decided to save the new recognised frame with the same convention it should be saved something like rando_1, however, the attendance should only show the original name rando. same with the box around the face in the video."

Result:
- Implemented regular expression parsing (`re.compile`) inside the `main()` enrollment loop to dynamically query the filesystem for `name` and `name_X` patterned files.
- Developed a local state machine to alert users of existing keys, handle `(s)ave` logic by calculating the `max()` suffix increment, and process `(o)verwrite` operations via `os.remove()`.
- Added an `re.sub(r'_\d+$', '', raw_name)` filter within `load_enrolled_faces()` so the UI and attendance systems abstract away the `_X` suffix and track only the pure identity key.

Human Action:
- Performed rigorous edge-case testing by simulating duplicate user scenarios to confirm the underlying suffix abstraction didn't leak into the frontend UI or the backend CSV logger.
- Verified that selecting the `(s)ave` option correctly incremented file names (e.g., `rando_1.png`), while successfully retaining the base name across the attendance sheet.
- Tested the `(o)verwrite` branch to ensure it completely purged old reference matrices from the filesystem before generating a clean slate for the identity.
