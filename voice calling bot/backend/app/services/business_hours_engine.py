from datetime import datetime
import pytz

class BusinessHoursEngine:
    """Evaluates whether a campaign is allowed to make calls based on business hours and timezone."""

    def is_within_business_hours(self, timezone_str: str, start_time, end_time) -> bool:
        """
        Checks if the current time in the target timezone is a weekday and within start_time and end_time.
        """
        try:
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)
            
            # Skip weekends (5 = Saturday, 6 = Sunday)
            if current_time.weekday() >= 5:
                return False
                
            # Check hours
            current_time_val = current_time.time()
            if start_time <= current_time_val <= end_time:
                return True
                
            return False
        except Exception as e:
            print(f"Error checking business hours: {e}")
            # Fail closed
            return False

business_hours_engine = BusinessHoursEngine()
