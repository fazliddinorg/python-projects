import time
import threading
from datetime import datetime, timedelta

class PomodoroTimer:
    def __init__(self):
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.short_break = 5 * 60     # 5 minutes in seconds
        self.long_break = 15 * 60     # 15 minutes in seconds
        self.sessions_completed = 0
        self.is_running = False
        self.timer_thread = None
    
    def play_sound(self):
        """Play notification sound (cross-platform)."""
        try:
            import winsound
            winsound.Beep(1000, 1000)  # Windows
        except ImportError:
            try:
                import os
                os.system('say "Timer finished"')  # macOS
            except:
                print("\n🔔 TIMER FINISHED! 🔔")
    
    def format_time(self, seconds):
        """Format seconds into MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def countdown(self, duration, session_type):
        """Run countdown timer."""
        self.is_running = True
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=duration)
        
        print(f"\n⏰ {session_type} started at {start_time.strftime('%H:%M:%S')}")
        print(f"📅 Session will end at {end_time.strftime('%H:%M:%S')}")
        print("Press Ctrl+C to stop the timer\n")
        
        try:
            while duration > 0 and self.is_running:
                mins, secs = divmod(duration, 60)
                timer_display = f"{mins:02d}:{secs:02d}"
                print(f"\r⏱️  {session_type}: {timer_display} remaining", end="", flush=True)
                time.sleep(1)
                duration -= 1
            
            if self.is_running:
                print(f"\n\n✅ {session_type} completed!")
                self.play_sound()
                
                if session_type == "Work Session":
                    self.sessions_completed += 1
                    print(f"🎯 Sessions completed today: {self.sessions_completed}")
                
        except KeyboardInterrupt:
            print(f"\n\n⏹️  {session_type} stopped by user.")
        
        self.is_running = False
    
    def start_work_session(self):
        """Start a work session."""
        if not self.is_running:
            self.timer_thread = threading.Thread(
                target=self.countdown, 
                args=(self.work_duration, "Work Session")
            )
            self.timer_thread.start()
    
    def start_short_break(self):
        """Start a short break."""
        if not self.is_running:
            self.timer_thread = threading.Thread(
                target=self.countdown, 
                args=(self.short_break, "Short Break")
            )
            self.timer_thread.start()
    
    def start_long_break(self):
        """Start a long break."""
        if not self.is_running:
            self.timer_thread = threading.Thread(
                target=self.countdown, 
                args=(self.long_break, "Long Break")
            )
            self.timer_thread.start()
    
    def stop_timer(self):
        """Stop the current timer."""
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join()
    
    def get_next_break_type(self):
        """Determine if next break should be short or long."""
        return "long" if self.sessions_completed % 4 == 0 and self.sessions_completed > 0 else "short"

def main():
    timer = PomodoroTimer()
    
    print("🍅 Pomodoro Timer")
    print("=================")
    print(f"Work Session: {timer.work_duration // 60} minutes")
    print(f"Short Break: {timer.short_break // 60} minutes")
    print(f"Long Break: {timer.long_break // 60} minutes")
    print("Long break after every 4 work sessions\n")
    
    while True:
        print("\n📋 Options:")
        print("1. Start work session")
        print("2. Start short break")
        print("3. Start long break")
        print("4. View stats")
        print("5. Stop current timer")
        print("6. Exit")
        
        choice = input("\nChoose an option (1-6): ").strip()
        
        if choice == "1":
            timer.start_work_session()
        elif choice == "2":
            timer.start_short_break()
        elif choice == "3":
            timer.start_long_break()
        elif choice == "4":
            print(f"\n📊 Sessions completed today: {timer.sessions_completed}")
            next_break = timer.get_next_break_type()
            print(f"🎯 Next break type: {next_break}")
        elif choice == "5":
            timer.stop_timer()
        elif choice == "6":
            timer.stop_timer()
            print("👋 Goodbye! Great work today!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
