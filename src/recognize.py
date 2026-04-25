import os
import cv2
import face_recognition
import numpy as np
import re

try:
    from src.enroll import enroll_face
    from src.attendance import log_attendance
except ImportError:
    from enroll import enroll_face
    from attendance import log_attendance

def load_enrolled_faces(enrolled_dir="../data/faces"):
    """
    Loads all enrolled faces from the given directory and returns their encodings and names.
    """
    known_face_encodings = []
    known_face_names = []
    
    # Check if we are running from src/ or project root
    if not os.path.exists(enrolled_dir):
        # Fallback to current directory assuming it's run from project root
        if enrolled_dir.startswith("../"):
            enrolled_dir = enrolled_dir[3:]
            
    if not os.path.exists(enrolled_dir):
        return known_face_encodings, known_face_names

    for filename in os.listdir(enrolled_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(enrolled_dir, filename)
            try:
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Add the first face found in the image
                    known_face_encodings.append(encodings[0])
                    raw_name = os.path.splitext(filename)[0]
                    name = re.sub(r'_\d+$', '', raw_name)
                    known_face_names.append(name)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    return known_face_encodings, known_face_names

def recognize_faces_in_image(image, known_encodings, known_names, tolerance=0.6):
    """
    Finds all faces in an image and matches them against known encodings.
    Args:
        image: numpy array (RGB) of the image.
        known_encodings: Pre-loaded list of known face encodings.
        known_names: Pre-loaded list of known face names.
        tolerance: Distance tolerance.
    Returns:
        List of dictionaries with keys: 'location', 'name', 'encoding'.
        'name' is "Unknown" if not matched.
    """
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    results = []
    
    for location, face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        
        if known_encodings:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] <= tolerance:
                name = known_names[best_match_index]
                
        results.append({
            'location': location, # (top, right, bottom, left)
            'name': name,
            'encoding': face_encoding
        })
        
    return results

def is_face_enrolled(unknown_image, enrolled_dir="../data/faces", tolerance=0.6, known_encodings=None, known_names=None):
    """
    Legacy method. Checks if the unknown face is already enrolled.
    """
    if known_encodings is None or known_names is None:
        known_encodings, known_names = load_enrolled_faces(enrolled_dir)
    
    if not known_encodings:
        return False, None
        
    if isinstance(unknown_image, str):
        if not os.path.exists(unknown_image):
            raise FileNotFoundError(f"Image File not found at {unknown_image}")
        image = face_recognition.load_image_file(unknown_image)
    else:
        image = unknown_image
        
    results = recognize_faces_in_image(image, known_encodings, known_names, tolerance)
    if results:
        # Check first face
        if results[0]['name'] != "Unknown":
            return True, results[0]['name']
            
    return False, None

def main():
    print("Loading enrolled faces from data/faces...")
    known_encodings, known_names = load_enrolled_faces("data/faces")
    
    if not known_encodings:
        print("Warning: No enrolled faces found. Please add faces to data/faces.")
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
    attendance_to_log = {} # Track known faces for attendance

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
                    # Add to attendance log
                    if face['name'] not in attendance_to_log:
                        attendance_to_log[face['name']] = face['encoding']

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
    
    # --- LOG ATTENDANCE ---
    if attendance_to_log:
        results_to_log = [{'name': name, 'encoding': enc} for name, enc in attendance_to_log.items()]
        try:
            log_attendance(results_to_log)
            print(f"\nLogged attendance for {len(results_to_log)} known person(s).")
        except Exception as e:
            print(f"\nFailed to log attendance: {e}")
            
    # --- SUMMARY & INTERACTIVE ENROLLMENT ---
    print("\n--- Summary ---")
    if not tracked_unknowns:
        print("No unknown guests detected.")
    else:
        print(f"Tracked {len(tracked_unknowns)} unique unknown guest(s).")
        print("Starting interactive enrollment...")
        
        for g in tracked_unknowns:
            print(f"\n- {g['id']}: Gathered {len(g['crops'])} frames.")
            if g['crops']:
                # The crops were taken directly from the OpenCV video frame, so they are already in BGR format
                best_crop = g['crops'][0]  
                
                # Show the face to the user
                cv2.imshow("Unknown Face", best_crop)
                cv2.waitKey(100) # Give UI time to draw
                
                choice = input(f"Do you want to enroll {g['id']}? (y/n): ").strip().lower()
                if choice == 'y':
                    name = input("Enter the name for this person: ").strip()
                    if name:
                        # --- DUPLICATE/MULTIPLE FRAME LOGIC ---
                        faces_dir = "data/faces"
                        pattern = re.compile(rf'^{re.escape(name)}(_\d+)?\.(png|jpg|jpeg)$', re.IGNORECASE)
                        
                        existing_files = []
                        if os.path.exists(faces_dir):
                            existing_files = [f for f in os.listdir(faces_dir) if pattern.match(f)]
                            
                        final_name = name
                        proceed_with_enrollment = True
                        
                        if existing_files:
                            print(f"   [!] Alert: The name '{name}' is already enrolled.")
                            choice2 = input("   Do you want to (s)ave as a different frame or (o)verwrite completely? (s/o): ").strip().lower()
                            
                            if choice2 == 'o':
                                print("   [CAUTION] You are about to overwrite the existing person entirely.")
                                confirm = input("   Are you sure? (y/n): ").strip().lower()
                                if confirm == 'y':
                                    for m in existing_files:
                                        try:
                                            os.remove(os.path.join(faces_dir, m))
                                        except Exception as e:
                                            print(f"   -> Failed to remove {m}: {e}")
                                    final_name = name
                                else:
                                    print("   -> Skipping enrollment.")
                                    proceed_with_enrollment = False
                            elif choice2 == 's':
                                max_suffix = 0
                                for m in existing_files:
                                    m_name = os.path.splitext(m)[0]
                                    suffix_match = re.search(r'_(\d+)$', m_name)
                                    if suffix_match:
                                        val = int(suffix_match.group(1))
                                        if val > max_suffix:
                                            max_suffix = val
                                final_name = f"{name}_{max_suffix + 1}"
                            else:
                                print("   -> Invalid choice. Skipping enrollment.")
                                proceed_with_enrollment = False
                        
                        if proceed_with_enrollment:
                            try:
                                enroll_face(best_crop, final_name)
                                print(f"   -> Successfully enrolled {final_name}.")
                                try:
                                    log_attendance([{'name': name, 'encoding': g['encodings'][0]}])
                                    print(f"   -> Logged attendance for newly enrolled {name}.")
                                except Exception as e:
                                    print(f"   -> Failed to log attendance for newly enrolled {name}: {e}")
                            except Exception as e:
                                print(f"   -> Failed to enroll: {e}")
                    else:
                        print("   -> No name entered. Skipping enrollment.")
                else:
                    print("   -> Skipping enrollment.")
                    
        cv2.destroyAllWindows()
            
    return tracked_unknowns

if __name__ == '__main__':
    extracted_guests = main()
