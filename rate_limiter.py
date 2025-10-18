import redis
import time
import logging
from datetime import datetime, timedelta
from typing import Optional
from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class RateLimiter:
    def __init__(self):
        self.redis_client = None
        self.logger = logging.getLogger(__name__)
        self.daily_usage = {}
        self.last_reset = datetime.now().date()
        
        # Initialize Redis connection
        try:
            self.redis_client = redis.from_url(Config.REDIS_URL)
            self.redis_client.ping()  # Test connection
            self.logger.info("Redis connection established")
        except Exception as e:
            self.logger.warning(f"Redis not available, using in-memory rate limiting: {e}")
            self.redis_client = None

    def _get_redis_key(self, identifier: str, prefix: str) -> str:
        """Generate Redis key for rate limiting"""
        return f"{prefix}:{identifier}"

    def _get_daily_usage_key(self) -> str:
        """Get daily usage key for today"""
        today = datetime.now().date()
        return f"daily_usage:{today}"

    def check_rate_limit(self, identifier: str) -> tuple[bool, str]:
        """Check if request is within rate limits"""
        current_time = time.time()
        
        # Check per-minute rate limit
        if not self._check_minute_limit(identifier, current_time):
            return False, "Rate limit exceeded: Maximum 1 query per minute"
        
        # Check daily usage limit
        if not self._check_daily_limit():
            return False, "Daily query limit exceeded"
        
        return True, "OK"

    def _check_minute_limit(self, identifier: str, current_time: float) -> bool:
        """Check per-minute rate limit"""
        if self.redis_client:
            key = self._get_redis_key(identifier, "rate_limit")
            try:
                # Get last request time
                last_request = self.redis_client.get(key)
                if last_request:
                    last_time = float(last_request)
                    if current_time - last_time < 60:  # 60 seconds
                        return False
                
                # Set current request time
                self.redis_client.setex(key, 60, str(current_time))
                return True
            except Exception as e:
                self.logger.error(f"Redis error in minute limit check: {e}")
                return True  # Fail open
        else:
            # In-memory fallback
            if not hasattr(self, '_last_requests'):
                self._last_requests = {}
            
            last_time = self._last_requests.get(identifier, 0)
            if current_time - last_time < 60:
                return False
            
            self._last_requests[identifier] = current_time
            return True

    def _check_daily_limit(self) -> bool:
        """Check daily usage limit"""
        if self.redis_client:
            try:
                key = self._get_daily_usage_key()
                current_usage = self.redis_client.get(key)
                usage_count = int(current_usage) if current_usage else 0
                
                if usage_count >= Config.DAILY_QUERY_LIMIT:
                    return False
                
                # Increment usage
                self.redis_client.incr(key)
                self.redis_client.expire(key, 86400)  # 24 hours
                
                # Check if we need to send alert
                if usage_count >= Config.DAILY_QUERY_LIMIT * 0.8:
                    self._send_usage_alert(usage_count + 1)
                
                return True
            except Exception as e:
                self.logger.error(f"Redis error in daily limit check: {e}")
                return True  # Fail open
        else:
            # In-memory fallback
            today = datetime.now().date()
            if today != self.last_reset:
                self.daily_usage = {}
                self.last_reset = today
            
            current_usage = self.daily_usage.get('total', 0)
            if current_usage >= Config.DAILY_QUERY_LIMIT:
                return False
            
            self.daily_usage['total'] = current_usage + 1
            return True

    def _send_usage_alert(self, current_usage: int):
        """Send email alert when approaching daily limit"""
        if not Config.ALERT_EMAIL or not Config.SMTP_USERNAME:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.SMTP_USERNAME
            msg['To'] = Config.ALERT_EMAIL
            msg['Subject'] = "Tree Whisperer - Daily Usage Alert"
            
            body = f"""
            Daily usage alert for Tree Whisperer:
            
            Current usage: {current_usage} queries
            Daily limit: {Config.DAILY_QUERY_LIMIT} queries
            Percentage: {(current_usage / Config.DAILY_QUERY_LIMIT) * 100:.1f}%
            
            This is an automated alert from the Tree Whisperer system.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Usage alert sent: {current_usage}/{Config.DAILY_QUERY_LIMIT}")
            
        except Exception as e:
            self.logger.error(f"Failed to send usage alert: {e}")

    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        if self.redis_client:
            try:
                key = self._get_daily_usage_key()
                current_usage = self.redis_client.get(key)
                usage_count = int(current_usage) if current_usage else 0
                
                return {
                    'daily_usage': usage_count,
                    'daily_limit': Config.DAILY_QUERY_LIMIT,
                    'percentage': (usage_count / Config.DAILY_QUERY_LIMIT) * 100
                }
            except Exception as e:
                self.logger.error(f"Error getting usage stats: {e}")
                return {'error': str(e)}
        else:
            today = datetime.now().date()
            if today != self.last_reset:
                self.daily_usage = {'total': 0}
                self.last_reset = today
            
            usage_count = self.daily_usage.get('total', 0)
            return {
                'daily_usage': usage_count,
                'daily_limit': Config.DAILY_QUERY_LIMIT,
                'percentage': (usage_count / Config.DAILY_QUERY_LIMIT) * 100
            }
