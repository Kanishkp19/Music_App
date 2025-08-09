"""Background worker for music generation"""
import time
import threading
from db.redis_client import redis_client
from modules.music_generator import MusicGenerator
from typing import Dict

class GeneratorWorker:
    def __init__(self):
        self.generator = MusicGenerator()
        self.running = False
    
    def start(self):
        """Start the background worker"""
        self.running = True
        thread = threading.Thread(target=self._work_loop)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop the background worker"""
        self.running = False
    
    def _work_loop(self):
        """Main work loop"""
        while self.running:
            # Check for pending jobs
            job_data = redis_client.client.lpop('queue:generation')
            if job_data:
                self._process_job(job_data)
            else:
                time.sleep(1)  # Wait before checking again
    
    def _process_job(self, job_data: str):
        """Process a single generation job"""
        try:
            import json
            job = json.loads(job_data)
            job_id = job['job_id']
            
            # Update status to processing
            redis_client.set(f"job:{job_id}", {'status': 'processing'})
            
            # Generate music (placeholder)
            result = self.generator.generate_music(
                job['mood'], job.get('tempo', 120), job.get('length', 30)
            )
            
            # Update status to completed
            redis_client.set(f"job:{job_id}", {
                'status': 'completed',
                'result': result
            })
            
        except Exception as e:
            print(f"Job failed: {e}")
            redis_client.set(f"job:{job_id}", {'status': 'failed', 'error': str(e)})

if __name__ == '__main__':
    worker = GeneratorWorker()
    worker.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        worker.stop()
