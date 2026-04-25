import sys
import os
import pytest

try:
    import cv2
    import numpy as np
except ImportError:
    print("Error: OpenCV and Numpy are not installed. run 'pip install opencv-python numpy'")
    sys.exit(1)

# Add the project root to sys.path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recognize import load_enrolled_faces, recognize_faces_in_image, is_face_enrolled
from src.enroll import enroll_face
from src.attendance import log_attendance
from src.utils import get_current_date
import face_recognition

def test_load_enrolled_faces(tmp_path):
    # Create a temporary directory with a dummy image
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    img_path = tmp_path / "test_user.jpg"
    cv2.imwrite(str(img_path), dummy_img)
    
    # load_enrolled_faces on dummy image without a face will return empty since no face is detected
    encodings, names = load_enrolled_faces(str(tmp_path))
    assert len(encodings) == 0
    assert len(names) == 0

def test_recognize_faces_in_image():
    # Provide a blank image
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    results = recognize_faces_in_image(dummy_img, [], [])
    assert len(results) == 0

def test_is_face_enrolled():
    # Provide a blank image
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    is_enrolled, name = is_face_enrolled(dummy_img, known_encodings=[], known_names=[])
    assert is_enrolled is False
    assert name is None

def test_log_attendance(tmp_path):
    log_file = tmp_path / "test_log.csv"
    dummy_results = [{'name': 'Test User', 'encoding': np.array([0.1, 0.2])}]
    log_attendance(dummy_results, log_file=str(log_file))
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
        assert "Test User" in content
        assert "face_encoding" in content

def test_get_current_date():
    date_str = get_current_date()
    assert isinstance(date_str, str)
    assert len(date_str) > 0

def test_enroll_face():
    # 1. Create mock cropped image
    mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # 2. Fake name
    fake_name = "test_mock_user_123"
    
    # 3. Call enroll_face
    saved_path = enroll_face(mock_image, fake_name, extension=".png")
    
    try:
        # 4. Check if file exists
        assert os.path.exists(saved_path), "File was not created."
        
        # 5. Load and match
        loaded_image = cv2.imread(saved_path)
        assert loaded_image is not None, "Failed to load the saved image."
        assert loaded_image.shape == mock_image.shape, "Loaded image shape does not match."
        assert np.array_equal(mock_image, loaded_image), "Loaded image pixels do not match the mock image."
    finally:
        # Cleanup
        if os.path.exists(saved_path):
            os.remove(saved_path)

