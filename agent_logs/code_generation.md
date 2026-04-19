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
