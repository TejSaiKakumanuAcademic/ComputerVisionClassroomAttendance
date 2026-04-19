import sys
import os

try:
    import cv2
    import numpy as np
except ImportError:
    print("Error: OpenCV and Numpy are not installed. run 'pip install opencv-python numpy'")
    sys.exit(1)

# Add the project root to sys.path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recognize import load_enrolled_faces, recognize_faces_in_image
import face_recognition

def main():
    print("Loading enrolled faces from data/registered_faces...")
    known_encodings, known_names = load_enrolled_faces("data/registered_faces")
    
    if not known_encodings:
        print("Warning: No enrolled faces found. Please add faces to data/registered_faces.")
    else:
        print(f"Loaded {len(known_names)} face(s): {', '.join(known_names)}")
    
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Starting video stream. Press 'q' to quit.")
    
    # We will accumulate data for unique unknown faces
    # Format: [{'id': 'Guest 1', 'encodings': [...], 'crops': [...]}, ...]
    tracked_unknowns = []
    guest_counter = 1

    process_this_frame = True
    face_results = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
            
        # Optimization: Resize frame to 1/4 size
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Only process every other frame to save time
        if process_this_frame:
            face_results = recognize_faces_in_image(
                rgb_small_frame, 
                known_encodings=known_encodings, 
                known_names=known_names
            )
            
            # --- IDENTITY CLUSTERING FOR UNKNOWN FACES ---
            for face in face_results:
                if face['name'] == "Unknown":
                    # Extract high-res crop
                    top, right, bottom, left = face['location']
                    top *= 4; right *= 4; bottom *= 4; left *= 4
                    pad = 20
                    h, w, _ = frame.shape
                    fc_top = max(0, top - pad)
                    fc_bottom = min(h, bottom + pad)
                    fc_left = max(0, left - pad)
                    fc_right = min(w, right + pad)
                    face_crop = frame[fc_top:fc_bottom, fc_left:fc_right].copy()
                    
                    if not tracked_unknowns:
                        assigned_name = f"Guest {guest_counter}"
                        tracked_unknowns.append({
                            'id': assigned_name,
                            'encodings': [face['encoding']],
                            'crops': [face_crop]
                        })
                        face['display_name'] = assigned_name
                        guest_counter += 1
                    else:
                        # Compare against the first encoding of each known guest
                        guest_encodings = [g['encodings'][0] for g in tracked_unknowns]
                        dists = face_recognition.face_distance(guest_encodings, face['encoding'])
                        best_match_idx = np.argmin(dists)
                        
                        if dists[best_match_idx] <= 0.6:  # Same tolerance threshold
                            # Matched an existing Guest
                            matched_guest = tracked_unknowns[best_match_idx]
                            # Only store up to 50 crops per guest to avoid memory issues
                            if len(matched_guest['crops']) < 50:
                                matched_guest['crops'].append(face_crop)
                                matched_guest['encodings'].append(face['encoding'])
                            face['display_name'] = matched_guest['id']
                        else:
                            # Too far from any known guest; create a new one!
                            assigned_name = f"Guest {guest_counter}"
                            tracked_unknowns.append({
                                'id': assigned_name,
                                'encodings': [face['encoding']],
                                'crops': [face_crop]
                            })
                            face['display_name'] = assigned_name
                            guest_counter += 1
                else:
                    # Known person from Database
                    face['display_name'] = face['name']

        process_this_frame = not process_this_frame

        # --- DRAWING ---
        for face in face_results:
            top, right, bottom, left = face['location']
            top *= 4; right *= 4; bottom *= 4; left *= 4

            name = face.get('display_name', face['name'])

            # Red for Guests, Green for Known Enrolled
            color = (0, 0, 255) if face['name'] == "Unknown" else (0, 255, 0)

            # Draw Box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw Label
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
    # --- SUMMARY & EXPORT ---
    print("\n--- Summary ---")
    if not tracked_unknowns:
        print("No unknown guests detected.")
    else:
        print(f"Tracked {len(tracked_unknowns)} unique unknown guest(s):")
        
        # Ensure the pending enrollment directory exists
        new_faces_dir = "data/faces/new"
        os.makedirs(new_faces_dir, exist_ok=True)
        
        for g in tracked_unknowns:
            print(f" - {g['id']}: Gathered {len(g['crops'])} frames.")
            if g['crops']:
                # The crops were taken directly from the OpenCV video frame, so they are already in BGR format
                best_crop = g['crops'][0]  
                
                # Format name safely (e.g. "Guest 1" -> "Guest_1.jpg")
                safe_name = g['id'].replace(' ', '_')
                filename = os.path.join(new_faces_dir, f"{safe_name}.jpg")
                
                # Save the image physically to disk for enroll.py to use
                cv2.imwrite(filename, best_crop)
                print(f"   -> Saved clearest snapshot to {filename}")
            
    return tracked_unknowns

if __name__ == '__main__':
    extracted_guests = main()
