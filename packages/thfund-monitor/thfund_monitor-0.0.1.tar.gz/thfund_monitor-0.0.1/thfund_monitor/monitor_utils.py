import os
from functools import wraps
from time import time

from prometheus_client import Gauge, Counter, Histogram, CollectorRegistry
from flask import request

registry = CollectorRegistry()

labels = ['env', 'url']
# 定义请求次数度量指标
request_count = Counter('request_count', '接口请求次数', labels, registry=registry)

# 定义请求耗时度量指标
request_time = Gauge('request_processing_time', '接口请求时间', labels, registry=registry)

# 定义请求耗时统计指标
request_time_histogram = Histogram('request_time_histogram', '接口耗时统计', labels, registry=registry)

# 定义失败次数度量指标
failure_count = Counter('failure_count', '接口失败次数', labels, registry=registry)


def prometheus_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            failure_count.labels(os.environ['ENV'], request.path).inc()
            raise e
        finally:
            end_time = time()
            request_count.labels(os.environ['ENV'], request.path).inc()
            request_time.labels(os.environ['ENV'], request.path).set(end_time - start_time)
            request_time_histogram.labels(os.environ['ENV'], request.path).observe(end_time - start_time)
        return result

    return wrapper
