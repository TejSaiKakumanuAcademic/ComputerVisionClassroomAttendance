import os
import cv2

def enroll_face(image, name, extension=".png"):
    """
    Stores the cropped face image in the registered_faces directory using the person's name.
    Enforces a file extension of PNG or JPEG.
    
    Args:
        image: Numpy array representing the cropped image of the person's face.
        name: Name of the person.
        extension: File extension (default is .png). Must be .png, .jpg, or .jpeg.
    """
    # Enforce allowed extensions
    ext = extension.lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        raise ValueError("Extension must be .png, .jpg, or .jpeg")
        
    # Define the output directory relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "data", "faces")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Construct the full file path
    file_path = os.path.join(output_dir, f"{name}{ext}")
    
    # Save the image
    success = cv2.imwrite(file_path, image)
    
    if not success:
        raise IOError(f"Could not write image to {file_path}")
        
    return file_path
