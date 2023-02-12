from redis import Redis
import config

rds = Redis.from_url(config.REDIS_URL)
