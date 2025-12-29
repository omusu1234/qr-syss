"""
Photo Analysis Module for Fraud Detection
Handles duplicate photo detection and face similarity matching
"""

import base64
import json
import io
from PIL import Image
import imagehash
import numpy as np

# Try to import face_recognition, but make it optional
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("Warning: face_recognition library not available. Face matching will be disabled.")


def decode_base64_image(base64_string):
    """Decode base64 string to PIL Image"""
    try:
        # Handle data URL format (data:image/png;base64,...)
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None


def calculate_photo_hash(photo_data):
    """
    Calculate perceptual hash for duplicate detection
    Returns hash string or None if error
    """
    try:
        image = decode_base64_image(photo_data)
        if image is None:
            return None
        
        # Use average hash for better duplicate detection
        hash_value = imagehash.average_hash(image)
        return str(hash_value)
    except Exception as e:
        print(f"Error calculating photo hash: {e}")
        return None


def compare_photo_hashes(hash1, hash2, threshold=5):
    """
    Compare two photo hashes
    Returns True if similar (within threshold), False otherwise
    threshold: maximum hamming distance (0-64 for average hash)
    """
    if not hash1 or not hash2:
        return False
    
    try:
        hash1_obj = imagehash.hex_to_hash(hash1)
        hash2_obj = imagehash.hex_to_hash(hash2)
        hamming_distance = hash1_obj - hash2_obj
        return hamming_distance <= threshold
    except Exception as e:
        print(f"Error comparing hashes: {e}")
        return False


def extract_face_encoding(photo_data):
    """
    Extract face encoding from photo using face_recognition
    Returns JSON-encoded face encoding or None
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return None
    
    try:
        image = decode_base64_image(photo_data)
        if image is None:
            return None
        
        # Convert PIL Image to numpy array
        image_array = np.array(image)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image_array)
        
        if not face_locations:
            # No face detected
            return None
        
        # Get face encodings (use first face if multiple)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if not face_encodings:
            return None
        
        # Convert numpy array to list for JSON serialization
        encoding = face_encodings[0].tolist()
        return json.dumps(encoding)
    except Exception as e:
        print(f"Error extracting face encoding: {e}")
        return None


def compare_face_encodings(encoding1_json, encoding2_json, tolerance=0.6):
    """
    Compare two face encodings
    Returns similarity score (0-1) or None if error
    tolerance: lower = more strict (default 0.6 is standard)
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return None
    
    if not encoding1_json or not encoding2_json:
        return None
    
    try:
        encoding1 = np.array(json.loads(encoding1_json))
        encoding2 = np.array(json.loads(encoding2_json))
        
        # Calculate face distance (lower = more similar)
        face_distance = face_recognition.face_distance([encoding1], encoding2)[0]
        
        # Convert distance to similarity score (0-1, higher = more similar)
        # face_distance of 0.6 = similarity of ~0.4, 0.0 = similarity of 1.0
        similarity = 1.0 - min(face_distance / tolerance, 1.0)
        
        return similarity
    except Exception as e:
        print(f"Error comparing face encodings: {e}")
        return None


def detect_duplicate_photo(photo_data, existing_attendance):
    """
    Check if photo is duplicate of existing attendance photo
    Returns True if duplicate, False otherwise
    """
    if not existing_attendance.photo_hash:
        return False
    
    new_hash = calculate_photo_hash(photo_data)
    if not new_hash:
        return False
    
    return compare_photo_hashes(new_hash, existing_attendance.photo_hash, threshold=5)


def detect_similar_face(face_encoding_json, existing_attendance, similarity_threshold=0.85):
    """
    Check if face encoding is similar to existing attendance
    Returns similarity score if above threshold, None otherwise
    """
    if not existing_attendance.face_encoding:
        return None
    
    similarity = compare_face_encodings(face_encoding_json, existing_attendance.face_encoding)
    
    if similarity and similarity >= similarity_threshold:
        return similarity
    
    return None


def analyze_photo_for_fraud(photo_data, session_id, current_attendance_id=None):
    """
    Analyze photo against all other photos in the session
    Returns dict with detected matches
    """
    from models import Attendance, db
    
    matches = {
        'duplicates': [],
        'similar_faces': []
    }
    
    try:
        # Get all other attendances in this session
        query = Attendance.query.filter_by(session_id=session_id)
        if current_attendance_id:
            query = query.filter(Attendance.id != current_attendance_id)
        
        existing_attendances = query.filter(Attendance.photo_data.isnot(None)).all()
        
        # Calculate hash and encoding for new photo
        new_hash = calculate_photo_hash(photo_data)
        new_face_encoding = extract_face_encoding(photo_data)
        
        for existing in existing_attendances:
            # Check for duplicate photo
            if new_hash and existing.photo_hash:
                if compare_photo_hashes(new_hash, existing.photo_hash, threshold=5):
                    matches['duplicates'].append({
                        'attendance_id': existing.id,
                        'admission_no': existing.admission_no,
                        'student_name': existing.student_name,
                        'match_type': 'duplicate'
                    })
            
            # Check for similar face
            if new_face_encoding and existing.face_encoding:
                similarity = compare_face_encodings(new_face_encoding, existing.face_encoding)
                if similarity and similarity >= 0.85:  # 85% similarity threshold
                    matches['similar_faces'].append({
                        'attendance_id': existing.id,
                        'admission_no': existing.admission_no,
                        'student_name': existing.student_name,
                        'similarity_score': similarity,
                        'match_type': 'face_similar'
                    })
        
        return matches
    except Exception as e:
        print(f"Error analyzing photo for fraud: {e}")
        return matches

