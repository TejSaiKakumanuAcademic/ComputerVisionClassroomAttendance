# Agent Code Generation Logs

## Task: Generate Recognise Function

Prompt:
"Implement src/recognise.py to accept a face and check if the face is already enrolled or not."

Result:
- Used face_recognition library to load enrolled faces.
- Implemented logic to check face distances and return matches.

Human Action:
- Looked at the design docs and asked the AI to write the base recognition component.

---

## Task: Real-time Camera Testing

Prompt:
"can you also implement testbasic.py where I can run recognise and get an output on whether or not the face is recognised. make it use my camera for real time tetsing"

Result:
- Created a test script using OpenCV to stream my webcam.
- Refactored the recognize function to cache encodings instead of loading from disk every single frame so it doesn't freeze up the computer.

Human Action:
- Wanted to test the recognize function with my laptop camera to actually see if it worked.

---

## Task: Fixing Package & Env Issues

Prompt:
"can you install all the required packages, I think I installed them but it just doesnt work can you make sure my file runs properly"
"look it just won't run"

Result:
- AI figured out that PyCharm was trying to use a virtual environment from a completely different class project (`PINN/.venv`) instead of my system Python.
- Forced the pip install of OpenCV and face_recognition directly into that .venv so it would run when I clicked 'Run' in PyCharm.

Human Action:
- Got a bunch of module import errors and camera failures. Copied my terminal logs to the AI to help me debug the environment path mixup.

---

## Task: UI Boxes, Frame Extraction, and FPS Boost

Prompt:
"if it is not recognised, can you make a code to cut the specific frame out and send the encoding of that face as a return value batch? I also want you to show the frame that you are cutting on the video screen with the appropriate color instead of saying unknown on the top. Also the video has very few frames, can you try making it 60frames per second? is it too much to ask?"

Result:
- Dropped the image processing size by 75% so it's super fast and hits high FPS.
- Added green/red bounding boxes over the head tracking.
- Set it up to pull the full-res crops of unrecognized people out of the frames.

Human Action:
- Realized the framerate was terrible and it was hard to tell who it was recognizing without boxes on the video output. 

---

## Task: Identity Clustering (Short-Term Memory)

Prompt:
"I just ran it and I was the only person in front of the camera and it said Collected data for 669 unknown face frames... will it know it was only one person or it will think each face is different? does it matter?"
"sounds good, implement it"

Result:
- Implemented short-term memory logic so the script knows that 600 slightly different frames of me walking forward is still just "Guest 1".
- Now tracks guests across the frame seamlessly without making duplicates.

Human Action:
- Tested the video script and got spammed with 600+ exports of myself. Brainstormed with AI on how to deduplicate them using face distances.

---

## Task: Prep for Future Enrollment 

Prompt:
"I am thinking if we can temporirly save faces into new and save the respective frame into that so that we can recall it via enroll when asking the user for name? Is this the best way to do it?"
"We run test_basic.py, walk into the frame until identified as 'Guest 1', and hit q. We check inside data/faces/new to verify that Guest_1.jpg was written clearly. So just implemnt techniques for above two steps"

Result:
- Updated the camera script exit logic. When I quit, it automatically saves the clearest crop of 'Guest 1' cleanly into the `data/faces/new/` folder.

Human Action:
- Asked some conceptual questions to figure out the best architecture to bridge the camera tracking into the upcoming enrollment script. Directed the AI to just focus on the camera export part for now.

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