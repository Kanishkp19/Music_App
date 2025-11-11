import os
import random
import mido
from mido import MidiFile, MidiTrack, Message
from datetime import datetime
import numpy as np
from typing import Dict, Tuple
import wave
import struct

class MusicGenerator:
    """
    AI-powered music generator that creates MIDI and audio files based on mood parameters.
    Uses algorithmic composition techniques mapped to valence/arousal coordinates.
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Musical scales for different moods
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],  # Happy, uplifting
            'minor': [0, 2, 3, 5, 7, 8, 10],  # Sad, melancholic
            'dorian': [0, 2, 3, 5, 7, 9, 10],  # Calm, balanced
            'phrygian': [0, 1, 3, 5, 7, 8, 10],  # Dark, tense
            'pentatonic': [0, 2, 4, 7, 9]  # Simple, peaceful
        }
    
    def generate_music(self, valence: float, arousal: float, duration: int = 30, 
                      tempo: int = None, style: str = 'auto') -> Tuple[str, str]:
        """
        Generate music based on mood parameters.
        
        Args:
            valence: Emotional valence (0-1, negative to positive)
            arousal: Emotional arousal (0-1, calm to energetic)
            duration: Duration in seconds
            tempo: BPM (if None, auto-calculated from arousal)
            style: Music style ('auto', 'ambient', 'rhythmic', 'melodic')
        
        Returns:
            Tuple of (midi_path, wav_path)
        """
        # Map mood to musical parameters
        params = self._mood_to_music_params(valence, arousal, tempo, style)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"generated_{timestamp}_{random.randint(1000, 9999)}"
        midi_path = os.path.join(self.output_dir, f"{filename}.mid")
        wav_path = os.path.join(self.output_dir, f"{filename}.wav")
        
        # Create MIDI file
        self._create_midi(midi_path, params, duration)
        
        # Convert MIDI to WAV
        self._midi_to_wav(midi_path, wav_path, params)
        
        return midi_path, wav_path
    
    def _mood_to_music_params(self, valence: float, arousal: float, 
                              tempo: int = None, style: str = 'auto') -> Dict:
        """Map mood coordinates to musical parameters"""
        
        # Determine scale based on valence
        if valence > 0.6:
            scale_type = 'major'
        elif valence < 0.4:
            scale_type = 'minor'
        elif arousal > 0.6:
            scale_type = 'dorian'
        elif arousal < 0.4:
            scale_type = 'pentatonic'
        else:
            scale_type = 'dorian'
        
        # Calculate tempo from arousal if not provided
        if tempo is None:
            # Map arousal (0-1) to tempo (60-180 BPM)
            tempo = int(60 + (arousal * 120))
        
        # Determine key (C=60 in MIDI)
        base_note = 60  # Middle C
        
        # Adjust octave based on valence
        if valence < 0.3:
            base_note -= 12  # Lower octave for sad moods
        elif valence > 0.7:
            base_note += 0  # Keep middle range for happy moods
        
        # Determine note density (notes per measure)
        if arousal > 0.7:
            note_density = 'high'  # More notes
            notes_per_measure = 16
        elif arousal < 0.3:
            note_density = 'low'  # Fewer notes
            notes_per_measure = 4
        else:
            note_density = 'medium'
            notes_per_measure = 8
        
        # Determine dynamics (velocity)
        velocity = int(40 + (arousal * 60))  # 40-100
        
        # Determine style
        if style == 'auto':
            if arousal > 0.6 and valence > 0.5:
                style = 'rhythmic'
            elif arousal < 0.4:
                style = 'ambient'
            else:
                style = 'melodic'
        
        return {
            'scale_type': scale_type,
            'scale': self.scales[scale_type],
            'base_note': base_note,
            'tempo': tempo,
            'note_density': note_density,
            'notes_per_measure': notes_per_measure,
            'velocity': velocity,
            'style': style,
            'valence': valence,
            'arousal': arousal
        }
    
    def _create_midi(self, filepath: str, params: Dict, duration: int):
        """Create MIDI file with generated music"""
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        # Set tempo
        tempo_microseconds = mido.bpm2tempo(params['tempo'])
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_microseconds))
        
        # Calculate number of measures based on duration and tempo
        beats_per_second = params['tempo'] / 60
        total_beats = int(duration * beats_per_second)
        measures = max(4, total_beats // 4)  # At least 4 measures
        
        # Generate melody
        if params['style'] == 'ambient':
            self._generate_ambient(track, params, measures)
        elif params['style'] == 'rhythmic':
            self._generate_rhythmic(track, params, measures)
        else:
            self._generate_melodic(track, params, measures)
        
        mid.save(filepath)
    
    def _generate_melodic(self, track: MidiTrack, params: Dict, measures: int):
        """Generate melodic music"""
        scale = params['scale']
        base_note = params['base_note']
        velocity = params['velocity']
        ticks_per_beat = 480
        
        current_note = 0
        direction = 1
        
        for measure in range(measures):
            for beat in range(4):
                # Choose note from scale
                scale_degree = current_note % len(scale)
                note = base_note + scale[scale_degree]
                
                # Add some variation
                if random.random() > 0.7:
                    note += random.choice([-12, 0, 12])  # Octave jumps
                
                # Note duration based on density
                if params['note_density'] == 'high':
                    duration = ticks_per_beat // 2
                elif params['note_density'] == 'low':
                    duration = ticks_per_beat * 2
                else:
                    duration = ticks_per_beat
                
                # Add note
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
                track.append(Message('note_off', note=note, velocity=0, time=duration))
                
                # Move melodically
                if random.random() > 0.3:
                    current_note += direction
                    if current_note >= len(scale) * 2:
                        direction = -1
                    elif current_note <= 0:
                        direction = 1
    
    def _generate_ambient(self, track: MidiTrack, params: Dict, measures: int):
        """Generate ambient/atmospheric music"""
        scale = params['scale']
        base_note = params['base_note']
        velocity = max(30, params['velocity'] - 20)  # Softer
        ticks_per_beat = 480
        
        for measure in range(measures):
            # Long sustained chords
            chord_notes = [
                base_note + scale[0],
                base_note + scale[2],
                base_note + scale[4]
            ]
            
            # Add chord
            for note in chord_notes:
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
            
            # Hold for full measure
            time.sleep(0)  # Placeholder
            
            for i, note in enumerate(chord_notes):
                time_offset = ticks_per_beat * 4 if i == len(chord_notes) - 1 else 0
                track.append(Message('note_off', note=note, velocity=0, time=time_offset))
    
    def _generate_rhythmic(self, track: MidiTrack, params: Dict, measures: int):
        """Generate rhythmic/energetic music"""
        scale = params['scale']
        base_note = params['base_note']
        velocity = params['velocity']
        ticks_per_beat = 480
        
        for measure in range(measures):
            for beat in range(4):
                for subdivision in range(4):
                    if random.random() > 0.3:  # 70% chance of note
                        scale_degree = random.randint(0, len(scale) - 1)
                        note = base_note + scale[scale_degree]
                        
                        duration = ticks_per_beat // 4
                        
                        track.append(Message('note_on', note=note, velocity=velocity, time=0))
                        track.append(Message('note_off', note=note, velocity=0, time=duration))
    
    def _midi_to_wav(self, midi_path: str, wav_path: str, params: Dict):
        """Convert MIDI to WAV using simple synthesis"""
        # Read MIDI file
        mid = MidiFile(midi_path)
        
        # Audio parameters
        sample_rate = 44100
        duration_seconds = sum(msg.time for msg in mid.tracks[0]) / mid.ticks_per_beat / (params['tempo'] / 60)
        num_samples = int(sample_rate * duration_seconds)
        
        # Generate audio samples
        audio_data = np.zeros(num_samples)
        current_sample = 0
        active_notes = {}
        
        for msg in mid.tracks[0]:
            # Calculate time in samples
            if msg.time > 0:
                time_seconds = msg.time / mid.ticks_per_beat / (params['tempo'] / 60)
                samples_to_advance = int(time_seconds * sample_rate)
                current_sample += samples_to_advance
            
            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = msg.velocity
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    del active_notes[msg.note]
            
            # Generate audio for active notes
            if active_notes and current_sample < num_samples:
                for note, velocity in active_notes.items():
                    frequency = 440 * (2 ** ((note - 69) / 12))
                    amplitude = velocity / 127.0 * 0.3
                    
                    # Generate samples for this note
                    end_sample = min(current_sample + 1000, num_samples)
                    t = np.arange(current_sample, end_sample) / sample_rate
                    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
                    audio_data[current_sample:end_sample] += waveform
        
        # Normalize audio
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.8
        
        # Convert to 16-bit PCM
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Write WAV file
        with wave.open(wav_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
    
    def cleanup_old_files(self, hours: int = 24):
        """Remove generated files older than specified hours"""
        import time
        current_time = time.time()
        cutoff_time = current_time - (hours * 3600)
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                file_time = os.path.getmtime(filepath)
                if file_time < cutoff_time:
                    try:
                        os.remove(filepath)
                    except Exception as e:
                        print(f"Error removing file {filepath}: {e}")
