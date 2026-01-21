"""
Virtual Mouse Performance Benchmark
Test and optimize performance metrics
"""

import time
import cv2
import mediapipe as mp
import statistics
import psutil
import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PerformanceMetrics:
    """Performance measurement data"""
    fps: float
    cpu_usage: float
    memory_usage: float
    detection_latency: float
    gesture_accuracy: float
    frame_processing_time: float

class PerformanceBenchmark:
    """Benchmark virtual mouse performance"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.cap = cv2.VideoCapture(0)
        self.metrics_history: List[PerformanceMetrics] = []
        
    def measure_fps(self, duration_seconds: int = 10) -> float:
        """Measure frames per second"""
        frame_count = 0
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            ret, _ = self.cap.read()
            if ret:
                frame_count += 1
            time.sleep(0.001)  # Small delay to prevent 100% CPU
        
        fps = frame_count / duration_seconds
        return fps
    
    def measure_latency(self, iterations: int = 100) -> float:
        """Measure hand detection latency"""
        latencies = []
        
        for _ in range(iterations):
            ret, frame = self.cap.read()
            if ret:
                start_time = time.perf_counter()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                end_time = time.perf_counter()
                latencies.append((end_time - start_time) * 1000)  # Convert to ms
        
        return statistics.mean(latencies) if latencies else 0
    
    def measure_resource_usage(self, duration_seconds: int = 10) -> tuple:
        """Measure CPU and memory usage"""
        cpu_samples = []
        memory_samples = []
        
        process = psutil.Process(os.getpid())
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            cpu_samples.append(process.cpu_percent())
            memory_samples.append(process.memory_info().rss / 1024 / 1024)  # MB
            time.sleep(0.1)
        
        avg_cpu = statistics.mean(cpu_samples) if cpu_samples else 0
        avg_memory = statistics.mean(memory_samples) if memory_samples else 0
        
        return avg_cpu, avg_memory
    
    def run_full_benchmark(self) -> Dict:
        """Run comprehensive performance benchmark"""
        print("🚀 Starting Performance Benchmark...")
        print("=" * 50)
        
        results = {}
        
        # Test FPS
        print("📊 Measuring FPS...")
        fps = self.measure_fps(5)
        results['fps'] = fps
        print(f"   FPS: {fps:.1f}")
        
        # Test latency
        print("⏱️ Measuring detection latency...")
        latency = self.measure_latency(50)
        results['latency_ms'] = latency
        print(f"   Latency: {latency:.1f}ms")
        
        # Test resource usage
        print("💻 Measuring resource usage...")
        cpu, memory = self.measure_resource_usage(5)
        results['cpu_percent'] = cpu
        results['memory_mb'] = memory
        print(f"   CPU: {cpu:.1f}%")
        print(f"   Memory: {memory:.1f}MB")
        
        # Calculate performance score
        score = self.calculate_performance_score(results)
        results['performance_score'] = score
        print(f"🏆 Performance Score: {score}/100")
        
        return results
    
    def calculate_performance_score(self, results: Dict) -> int:
        """Calculate overall performance score (0-100)"""
        score = 0
        
        # FPS scoring (30 FPS = 100 points)
        fps_score = min(100, (results['fps'] / 30) * 100)
        score += fps_score * 0.3
        
        # Latency scoring (10ms = 100 points)
        latency_score = max(0, 100 - (results['latency_ms'] / 10) * 100)
        score += latency_score * 0.3
        
        # CPU usage scoring (10% = 100 points)
        cpu_score = max(0, 100 - (results['cpu_percent'] / 10) * 100)
        score += cpu_score * 0.2
        
        # Memory usage scoring (100MB = 100 points)
        memory_score = max(0, 100 - (results['memory_mb'] / 100) * 100)
        score += memory_score * 0.2
        
        return int(score)
    
    def generate_report(self, results: Dict):
        """Generate performance report"""
        print("\n" + "=" * 50)
        print("📋 PERFORMANCE REPORT")
        print("=" * 50)
        
        print(f"🎯 Overall Score: {results['performance_score']}/100")
        print(f"📊 FPS: {results['fps']:.1f} (Target: 30+)")
        print(f"⏱️ Latency: {results['latency_ms']:.1f}ms (Target: <20ms)")
        print(f"💻 CPU Usage: {results['cpu_percent']:.1f}% (Target: <20%)")
        print(f"🧠 Memory: {results['memory_mb']:.1f}MB (Target: <100MB)")
        
        print("\n💡 Recommendations:")
        if results['fps'] < 25:
            print("   - Lower camera resolution")
            print("   - Reduce detection frequency")
        if results['latency_ms'] > 30:
            print("   - Use faster hardware")
            print("   - Optimize MediaPipe settings")
        if results['cpu_percent'] > 30:
            print("   - Lower confidence thresholds")
            print("   - Reduce frame rate")
        if results['memory_mb'] > 150:
            print("   - Reduce buffer sizes")
            print("   - Clear unused variables")
        
        print("\n🏅 Performance Grade:", self.get_grade(results['performance_score']))
    
    def get_grade(self, score: int) -> str:
        """Get performance grade based on score"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        self.hands.close()

def main():
    """Run performance benchmark"""
    benchmark = PerformanceBenchmark()
    
    try:
        results = benchmark.run_full_benchmark()
        benchmark.generate_report(results)
        
        # Save results to file
        import json
        with open('performance_report.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("\n💾 Report saved to 'performance_report.json'")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
    finally:
        benchmark.cleanup()

if __name__ == "__main__":
    main()
