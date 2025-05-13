
import speech_recognition as sr
from g2p_en import G2p
from Levenshtein import ratio as levenshtein_ratio
import numpy as np

class PronunciationAnalyzer:
    def __init__(self):
        self.g2p = G2p()
        self.recognizer = sr.Recognizer()
    
    def text_to_phonemes(self, text):
        """Convert text to phonemes using g2p-en"""
        phones = self.g2p(text)
        return [p for p in phones if p not in [' ', '.', '?', '!']]

    def phoneme_similarity(self, reference, recorded):
        """Calculate similarity between two phoneme sequences"""
        ref_str = ' '.join(reference)
        rec_str = ' '.join(recorded)
        return levenshtein_ratio(ref_str, rec_str) * 100

    def analyze_audio(self, audio_path, reference_word):
        """Main analysis function"""
        # Convert reference word to phonemes
        reference_phonemes = self.text_to_phonemes(reference_word)
        
        # Speech recognition
        with sr.AudioFile(audio_path) as source:
            audio = self.recognizer.record(source)
        
        try:
            recognized_text = self.recognizer.recognize_google(audio).lower()
            recognized_phonemes = self.text_to_phonemes(recognized_text)
            
            # Calculate similarity score
            score = self.phoneme_similarity(reference_phonemes, recognized_phonemes)
            
            # Identify mispronunciations
            mispronounced = self._find_mispronounced_phonemes(
                reference_phonemes, 
                recognized_phonemes
            )
            
            # Generate feedback
            feedback = self._generate_feedback(score, mispronounced)
            
            return {
                "score": round(score, 2),
                "recognized_text": recognized_text,
                "reference_phonemes": reference_phonemes,
                "recognized_phonemes": recognized_phonemes,
                "feedback": feedback,
                "mispronounced": mispronounced
            }
            
        except sr.UnknownValueError:
            return {"error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"error": f"Speech recognition error: {str(e)}"}

    def _find_mispronounced_phonemes(self, reference, recorded):
        """Identify mismatched phonemes using sequence alignment"""
        matrix = np.zeros((len(reference)+1, len(recorded)+1))
        
        # Initialize matrix for alignment
        for i in range(len(reference)+1):
            matrix[i][0] = i
        for j in range(len(recorded)+1):
            matrix[0][j] = j
            
        # Fill matrix
        for i in range(1, len(reference)+1):
            for j in range(1, len(recorded)+1):
                cost = 0 if reference[i-1] == recorded[j-1] else 1
                matrix[i][j] = min(
                    matrix[i-1][j] + 1,    # deletion
                    matrix[i][j-1] + 1,    # insertion
                    matrix[i-1][j-1] + cost  # substitution
                )
                
        # Backtrack to find mispronunciations
        i, j = len(reference), len(recorded)
        mismatches = []
        
        while i > 0 and j > 0:
            if reference[i-1] == recorded[j-1]:
                i -= 1
                j -= 1
            else:
                mismatches.append({
                    'position': i-1,
                    'expected': reference[i-1],
                    'actual': recorded[j-1] if j-1 >= 0 else None
                })
                if matrix[i][j] == matrix[i-1][j-1] + 1:
                    i -= 1
                    j -= 1
                elif matrix[i][j] == matrix[i-1][j] + 1:
                    i -= 1
                else:
                    j -= 1
                    
        return mismatches[::-1]  # Reverse to maintain chronological order

    def _generate_feedback(self, score, mispronounced):
        """Generate human-readable feedback"""
        if score >= 90:
            return "Excellent pronunciation! 🎉"
        elif score >= 75:
            feedback = "Good effort! Almost there!"
        elif score >= 50:
            feedback = "Keep practicing! You're making progress."
        else:
            feedback = "Let's try that again. Pay attention to the sounds."
            
        if mispronounced:
            feedback += "\nPay special attention to:"
            for i, m in enumerate(mispronounced[:3]):  # Show top 3 issues
                feedback += f"\n- Sound {m['position']+1}: " \
                          f"Expected '{m['expected']}', " \
                          f"heard '{m['actual'] or 'missing'}'"
                          
        return feedback