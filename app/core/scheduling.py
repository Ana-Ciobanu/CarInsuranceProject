from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from datetime import datetime, date
from app.db.session import SessionLocal
from app.db.models import InsurancePolicy
import structlog
import os
from urllib.parse import urlparse
from app.core.config import settings

INTERVAL_SECONDS = settings.SCHEDULER_INTERVAL_SECONDS

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
parsed = urlparse(redis_url)
host = parsed.hostname or "localhost"
port = parsed.port or 6379
db = int(parsed.path.lstrip("/")) if parsed.path else 0
password = parsed.password

jobstores = {
    'default': RedisJobStore(host=host, port=port, db=db, password=password)
}

scheduler = BackgroundScheduler(jobstores=jobstores)

def log_policy_expiry():
    now = datetime.now()
    today = date.today()
    db = SessionLocal()
    policies = db.query(InsurancePolicy).filter(
        InsurancePolicy.end_date == today,
        InsurancePolicy.logged_expiry_at.is_(None)
    ).all()
    for policy in policies:
        structlog.get_logger().info(
            "Policy expired",
            policy_id=policy.id,
            car_id=policy.car_id,
            end_date=str(policy.end_date)
        )
        policy.logged_expiry_at = now
        db.add(policy)
    db.commit()
    db.close()

# Add job to scheduler
scheduler.add_job(
    log_policy_expiry,
    'interval',
    seconds=INTERVAL_SECONDS,
    id='log_policy_expiry',
    replace_existing=True
)

def start_scheduler():
    scheduler.start()
    structlog.get_logger().info("BackgroundScheduler started", interval_seconds=INTERVAL_SECONDS)
