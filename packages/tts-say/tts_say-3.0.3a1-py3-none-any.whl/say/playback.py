import threading
import queue
import simpleaudio as sa
from pydub import AudioSegment

class PlaybackEngine:
    
    playback = None
    
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.playback_thread = threading.Thread(target=self._playback_loop)
        self.playback_thread.daemon = True
        self.stop_event = threading.Event()
        self.playback_thread.start()

    def __del__(self):
        self.stop()

    def _playback_loop(self):
        while not self.stop_event.is_set():
            try:
                if self.playback is not None:
                    if self.playback.is_playing():
                        continue
                    self.playback = None
                audio_segment = self.audio_queue.get(timeout=1)
                self.playback = self._play_audio(audio_segment)
                while self.playback.is_playing():
                    if self.stop_event.is_set():
                        self.playback.stop()
                        self.playback = None
                        break
                self.playback = None
                self.audio_queue.task_done()
            except queue.Empty:
                continue

    def _play_audio(self, audio_segment: AudioSegment):
        playback = sa.play_buffer(audio_segment.raw_data, num_channels=audio_segment.channels, bytes_per_sample=audio_segment.sample_width, sample_rate=audio_segment.frame_rate)
        return playback
    
    @property
    def is_playing(self) -> bool:
        return bool(
            self.playback is not None \
            and self.playback.is_playing()
        )
    
    def add_audio_segment(self, audio_segment: AudioSegment):
        self.audio_queue.put(audio_segment)

    def wait_done(self):
        self.audio_queue.join()

    def stop(self):
        self.audio_queue = queue.Queue()
        self.stop_event.set()
        self.playback_thread.join()
        self.stop_event.clear()
