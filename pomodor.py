import pickle
import os


class PomodoroCalculator:
    def __init__(self, save_file="pomodoro_state.pkl"):
        self.save_file = save_file
        self.total_worked_minutes = 0
        self.position_in_session = 0
        self.load_state()

    def save_state(self):
        """Save current state to file"""
        state = {
            'total_worked_minutes': self.total_worked_minutes,
            'position_in_session': self.position_in_session
        }
        try:
            with open(self.save_file, 'wb') as f:
                pickle.dump(state, f)
            print("State saved successfully!")
        except Exception as e:
            print(f"Error saving state: {e}")

    def load_state(self):
        """Load state from file if it exists"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'rb') as f:
                    state = pickle.load(f)
                self.total_worked_minutes = state.get('total_worked_minutes', 0)
                self.position_in_session = state.get('position_in_session', 0)
                print("Previous state loaded!")
            except Exception as e:
                print(f"Error loading state: {e}")
                self.reset()
        else:
            print("No previous state found. Starting fresh.")

    def add_work_time(self, hours, minutes):
        """Add work time and automatically save state"""
        total_minutes = hours * 60 + minutes
        self.total_worked_minutes += total_minutes
        self.save_state()  # Auto-save after adding time

        return self.calculate_sessions_and_breaks(total_minutes)

    def remove_work_time(self, hours, minutes):
        """Remove work time and automatically save state"""
        total_minutes_to_remove = hours * 60 + minutes

        # Calculate total available time
        total_available = self.total_worked_minutes + self.position_in_session

        if total_minutes_to_remove > total_available:
            print(f"Warning: Cannot remove {total_minutes_to_remove} minutes.")
            print(f"Only {total_available} minutes available.")
            return None

        # Remove the time
        remaining_to_remove = total_minutes_to_remove

        # First, remove from position_in_session
        if remaining_to_remove <= self.position_in_session:
            self.position_in_session -= remaining_to_remove
            remaining_to_remove = 0
        else:
            remaining_to_remove -= self.position_in_session
            self.position_in_session = 0

        # Then remove from total_worked_minutes
        if remaining_to_remove > 0:
            self.total_worked_minutes -= remaining_to_remove

        self.save_state()  # Auto-save after removing time

        print(f"Removed {hours}h {minutes}m successfully!")
        return self.calculate_sessions_and_breaks()

    def calculate_sessions_and_breaks(self, current_input_minutes=0):
        """Calculate sessions and breaks based on current state and current input time"""
        total_minutes = self.total_worked_minutes + self.position_in_session
        full_sessions = total_minutes // 25
        remaining_minutes = total_minutes % 25

        # Calculate breaks
        long_breaks = full_sessions // 4
        short_breaks = full_sessions - long_breaks

        # Total break time
        total_break_time = long_breaks * 20 + short_breaks * 5

        # Calculate break time earned for current input only
        current_full_sessions = current_input_minutes // 25
        current_long_breaks = current_full_sessions // 4
        current_short_breaks = current_full_sessions - current_long_breaks
        current_break_time = current_long_breaks * 20 + current_short_breaks * 5

        # Update position in session
        self.position_in_session = remaining_minutes

        return {
            'full_sessions': full_sessions,
            'remaining_minutes': remaining_minutes,
            'long_breaks': long_breaks,
            'short_breaks': short_breaks,
            'total_break_time': total_break_time,
            'current_break_time': current_break_time,
            'position_in_session': self.position_in_session
        }

    def get_status(self):
        """Get current status without adding time"""
        result = self.calculate_sessions_and_breaks()
        print(f"\n--- Pomodoro Status ---")
        print(f"Total sessions completed: {result['full_sessions']}")
        print(f"Current session progress: {result['position_in_session']}/25 minutes")
        print(f"Short breaks taken: {result['short_breaks']}")
        print(f"Long breaks taken: {result['long_breaks']}")
        print(f"Total break time: {result['total_break_time']} minutes")
        return result

    def reset(self):
        """Reset all progress and save"""
        self.total_worked_minutes = 0
        self.position_in_session = 0
        self.save_state()
        print("Progress reset!")


# Simple command-line interface
def main():
    pomodoro = PomodoroCalculator()

    while True:
        print("\n=== Pomodoro Calculator ===")
        print("1. Add work time")
        print("2. Remove work time")
        print("3. Check status")
        print("4. Reset progress")
        print("5. Exit")

        choice = input("Choose option (1-5): ").strip()

        if choice == '1':
            try:
                hours = int(input("Hours worked: "))
                minutes = int(input("Minutes worked: "))
                result = pomodoro.add_work_time(hours, minutes)

                print(f"\nAdded {hours}h {minutes}m")
                print(f"Sessions: {result['full_sessions']}")
                print(f"Break time earned: {result['current_break_time']} minutes")
                print(f"Current session: {result['position_in_session']}/25 minutes")

            except ValueError:
                print("Please enter valid numbers!")

        elif choice == '2':
            try:
                hours = int(input("Hours to remove: "))
                minutes = int(input("Minutes to remove: "))
                result = pomodoro.remove_work_time(hours, minutes)

                if result:
                    print(f"\nRemoved {hours}h {minutes}m")
                    print(f"Remaining sessions: {result['full_sessions']}")
                    print(f"Current session: {result['position_in_session']}/25 minutes")

            except ValueError:
                print("Please enter valid numbers!")

        elif choice == '3':
            pomodoro.get_status()

        elif choice == '4':
            confirm = input("Reset all progress? (y/n): ").lower()
            if confirm == 'y':
                pomodoro.reset()

        elif choice == '5':
            print("Goodbye! Your progress is saved.")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
