from flask import Blueprint, request, jsonify, send_file
from src.services.music_generator import MusicGenerator
from src.models.generation_job import GenerationJob
from src.models.mood_entry import MoodEntry
from src.utils.helpers import require_auth
from src.config import Config
import os
import threading

generator_bp = Blueprint('generator', __name__, url_prefix='/api/v1/generate')
music_generator = None

def init_generator_service(generator: MusicGenerator):
    global music_generator
    music_generator = generator

def process_generation(job_id: str, valence: float, arousal: float, 
                      duration: int, tempo: int, style: str):
    """Background task to process music generation"""
    try:
        # Update status to processing
        GenerationJob.update_status(job_id, 'processing')
        
        # Generate music
        midi_path, wav_path = music_generator.generate_music(
            valence=valence,
            arousal=arousal,
            duration=duration,
            tempo=tempo,
            style=style
        )
        
        # Update status to completed
        GenerationJob.update_status(job_id, 'completed', file_path=wav_path)
        
    except Exception as e:
        print(f"Generation error: {e}")
        GenerationJob.update_status(job_id, 'failed', error_message=str(e))

@generator_bp.route('', methods=['POST'])
@require_auth
def start_generation():
    """Start a new music generation job"""
    try:
        data = request.get_json()
        
        # Get mood parameters
        use_current_mood = data.get('use_current_mood', True)
        
        if use_current_mood:
            # Get user's latest mood
            mood = MoodEntry.get_latest(request.user_id)
            if not mood:
                return jsonify({'error': 'No mood data found. Please check your mood first.'}), 400
            valence = mood['valence']
            arousal = mood['arousal']
        else:
            # Use provided mood parameters
            valence = data.get('valence', 0.5)
            arousal = data.get('arousal', 0.5)
        
        # Validate mood parameters
        valence = max(0.0, min(1.0, float(valence)))
        arousal = max(0.0, min(1.0, float(arousal)))
        
        # Get generation parameters
        duration = data.get('duration', 30)
        duration = max(Config.MIN_GENERATION_DURATION, 
                      min(Config.MAX_GENERATION_DURATION, int(duration)))
        
        tempo = data.get('tempo')
        if tempo:
            tempo = max(60, min(180, int(tempo)))
        
        style = data.get('style', 'auto')
        if style not in ['auto', 'ambient', 'rhythmic', 'melodic']:
            style = 'auto'
        
        # Create job
        parameters = {
            'valence': valence,
            'arousal': arousal,
            'duration': duration,
            'tempo': tempo,
            'style': style
        }
        
        job_id = GenerationJob.create(request.user_id, parameters)
        
        # Start generation in background thread
        thread = threading.Thread(
            target=process_generation,
            args=(job_id, valence, arousal, duration, tempo, style)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'pending',
            'message': 'Music generation started'
        }), 202
        
    except Exception as e:
        print(f"Error starting generation: {e}")
        return jsonify({'error': 'Failed to start generation'}), 500

@generator_bp.route('/<job_id>', methods=['GET'])
@require_auth
def get_generation_status(job_id):
    """Get the status of a generation job"""
    try:
        job = GenerationJob.get_by_id(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check if user owns this job
        if job['user_id'] != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        response = {
            'job_id': job['_id'],
            'status': job['status'],
            'parameters': job['parameters'],
            'created_at': job['created_at'].isoformat(),
            'updated_at': job['updated_at'].isoformat()
        }
        
        if job['status'] == 'completed':
            response['download_url'] = f"/api/v1/generate/{job_id}/download"
            response['completed_at'] = job['completed_at'].isoformat()
        
        if job['status'] == 'failed':
            response['error_message'] = job.get('error_message', 'Unknown error')
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error getting job status: {e}")
        return jsonify({'error': 'Failed to get job status'}), 500

@generator_bp.route('/<job_id>/download', methods=['GET'])
@require_auth
def download_generation(job_id):
    """Download the generated music file"""
    try:
        job = GenerationJob.get_by_id(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check if user owns this job
        if job['user_id'] != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if job['status'] != 'completed':
            return jsonify({'error': 'Generation not completed yet'}), 400
        
        file_path = job['file_path']
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Generated file not found'}), 404
        
        filename = os.path.basename(file_path)
        
        return send_file(
            file_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return jsonify({'error': 'Failed to download file'}), 500

@generator_bp.route('/history', methods=['GET'])
@require_auth
def get_generation_history():
    """Get user's generation history"""
    try:
        limit = request.args.get('limit', 20, type=int)
        limit = min(limit, 100)  # Max 100
        
        jobs = GenerationJob.get_user_jobs(request.user_id, limit)
        
        # Format response
        history = []
        for job in jobs:
            item = {
                'job_id': job['_id'],
                'status': job['status'],
                'parameters': job['parameters'],
                'created_at': job['created_at'].isoformat()
            }
            
            if job['status'] == 'completed':
                item['download_url'] = f"/api/v1/generate/{job['_id']}/download"
            
            history.append(item)
        
        return jsonify({'history': history}), 200
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({'error': 'Failed to get history'}), 500
