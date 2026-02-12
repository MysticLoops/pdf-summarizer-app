import os
from typing import Optional
from datetime import datetime

class AudioPlayer:
    """Handles text-to-speech conversion and audio playback."""
    
    def __init__(self, output_dir: str = "data/audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.audio_available = self._check_tts_availability()
    
    def _check_tts_availability(self) -> bool:
        """Check if TTS libraries are available."""
        try:
            import gtts
            return True
        except ImportError:
            try:
                import pyttsx3
                return True
            except ImportError:
                return False
    
    def text_to_speech(self, text: str, voice_type: str = "Female", 
                      speed: float = 1.0) -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text: Text to convert
            voice_type: Voice type (Male, Female, Neutral)
            speed: Speech speed (0.5 to 2.0)
            
        Returns:
            Path to audio file or None if failed
        """
        # Try Google TTS first (online)
        audio_file = self._gtts_convert(text, speed)
        
        if audio_file:
            return audio_file
        
        # Fallback to pyttsx3 (offline)
        audio_file = self._pyttsx3_convert(text, voice_type, speed)
        
        return audio_file
    
    def _gtts_convert(self, text: str, speed: float) -> Optional[str]:
        """
        Convert text using Google TTS.
        
        Args:
            text: Text to convert
            speed: Speech speed
            
        Returns:
            Path to audio file or None
        """
        try:
            from gtts import gTTS
            
            # Limit text length for demo purposes
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"speech_{timestamp}.mp3"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create TTS object
            tts = gTTS(text=text, lang='en', slow=(speed < 0.8))
            
            # Save to file
            tts.save(filepath)
            
            return filepath
        
        except ImportError:
            print("gTTS not available")
            return None
        except Exception as e:
            print(f"Error in gTTS conversion: {e}")
            return None
    
    def _pyttsx3_convert(self, text: str, voice_type: str, speed: float) -> Optional[str]:
        """
        Convert text using pyttsx3 (offline TTS).
        
        Args:
            text: Text to convert
            voice_type: Voice type
            speed: Speech speed
            
        Returns:
            Path to audio file or None
        """
        try:
            import pyttsx3
            
            # Initialize engine
            engine = pyttsx3.init()
            
            # Set properties
            voices = engine.getProperty('voices')
            
            # Select voice based on type
            if voice_type == "Male" and len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
            elif voice_type == "Female" and len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            
            # Set rate (speed)
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate * speed)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"speech_{timestamp}.mp3"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save to file
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            
            return filepath
        
        except ImportError:
            print("pyttsx3 not available")
            return None
        except Exception as e:
            print(f"Error in pyttsx3 conversion: {e}")
            return None
    
    def generate_audio_summary(self, summary: str, title: str = "Summary") -> Optional[str]:
        """
        Generate audio for a summary with introduction.
        
        Args:
            summary: Summary text
            title: Title for the summary
            
        Returns:
            Path to audio file
        """
        intro = f"Here is the summary of {title}. "
        full_text = intro + summary
        
        return self.text_to_speech(full_text)
    
    def batch_convert(self, texts: list, prefix: str = "audio") -> list:
        """
        Convert multiple texts to audio files.
        
        Args:
            texts: List of texts to convert
            prefix: Prefix for audio files
            
        Returns:
            List of audio file paths
        """
        audio_files = []
        
        for i, text in enumerate(texts, 1):
            audio_file = self.text_to_speech(text)
            if audio_file:
                audio_files.append(audio_file)
        
        return audio_files
    
    def get_audio_duration(self, audio_file: str) -> float:
        """
        Get duration of audio file in seconds.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Duration in seconds
        """
        try:
            from mutagen.mp3 import MP3
            audio = MP3(audio_file)
            return audio.info.length
        except:
            # Estimate based on text length (rough approximation)
            # Average speaking rate is about 150 words per minute
            return 0.0
    
    def cleanup_old_audio(self, days: int = 7):
        """
        Remove audio files older than specified days.
        
        Args:
            days: Number of days to keep files
        """
        import time
        
        current_time = time.time()
        max_age = days * 24 * 60 * 60  # Convert days to seconds
        
        if not os.path.exists(self.output_dir):
            return
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age:
                    try:
                        os.remove(filepath)
                        print(f"Removed old audio file: {filename}")
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")
