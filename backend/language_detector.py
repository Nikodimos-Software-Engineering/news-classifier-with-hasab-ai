from geezswitch import detect, detect_langs
from geezswitch import DetectorFactory

# Set seed for consistent results
DetectorFactory.seed = 0

def lang_detected(text):
    """
    Returns a list: [type, language]
    type: 'Pure' or 'Mixed'
    language: 'Amharic' or 'English'
    """
    # Script detection for Amharic/Ethiopic characters
    def has_amharic_script(txt):
        # Amharic/Ethiopic Unicode range: ሀ (U+1200) to ኿ (U+137F)
        return any(0x1200 <= ord(char) <= 0x137F for char in txt)
    
    def has_english_script(txt):
        # Check for ASCII letters
        return any('a' <= char.lower() <= 'z' for char in txt if char.isalpha())
    
    contains_amharic = has_amharic_script(text)
    contains_english = has_english_script(text)
    
    # If both scripts are present, it's mixed
    if contains_amharic and contains_english:
        # Determine dominant language by character count
        amharic_chars = sum(1 for char in text if 0x1200 <= ord(char) <= 0x137F)
        english_chars = sum(1 for char in text if char.isalpha() and char.isascii())
        
        if english_chars >= amharic_chars:
            return ['Mixed', 'English']
        else:
            return ['Mixed', 'Amharic']
    
    # If only one script, use geezswitch to determine which language
    lang = detect(text)
    
    if lang == 'amh':
        return ['Pure', 'Amharic']
    elif lang == 'en':
        return ['Pure', 'English']
    else:
        # Fallback based on script
        if contains_amharic:
            return ['Pure', 'Amharic']
        elif contains_english:
            return ['Pure', 'English']
        else:
            return ['Pure', 'Other']