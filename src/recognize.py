import os
import face_recognition
import numpy as np

def load_enrolled_faces(enrolled_dir="../data/registered_faces"):
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
                    name = os.path.splitext(filename)[0]
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

def is_face_enrolled(unknown_image, enrolled_dir="../data/registered_faces", tolerance=0.6, known_encodings=None, known_names=None):
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
