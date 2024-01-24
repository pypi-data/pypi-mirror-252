# 天弘基金统一监控安装包

1. 使用demo

```python

from monitor_utils import prometheus_monitor, registry

@app.route('/metric', methods=['GET'])
def monitor():
    data = generate_latest(registry)
    return Response(data.decode(), mimetype=CONTENT_TYPE_LATEST, status=200)


@app.route('/hello')
@prometheus_monitor
def hello():
    return 'Hello World! '
```
2. 埋点用例

```
# HELP request_count_total 接口请求次数
# TYPE request_count_total counter
request_count_total{env="PROD",url="/hello"} 1.0
# HELP request_count_created 接口请求次数
# TYPE request_count_created gauge
request_count_created{env="PROD",url="/hello"} 1.7060823348361146e+09
# HELP request_processing_time 接口请求时间
# TYPE request_processing_time gauge
request_processing_time{env="PROD",url="/hello"} 0.0
# HELP request_time_histogram 接口耗时统计
# TYPE request_time_histogram histogram
request_time_histogram_bucket{env="PROD",le="0.005",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.01",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.025",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.05",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.075",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.1",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.25",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.5",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="0.75",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="1.0",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="2.5",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="5.0",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="7.5",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="10.0",url="/hello"} 1.0
request_time_histogram_bucket{env="PROD",le="+Inf",url="/hello"} 1.0
request_time_histogram_count{env="PROD",url="/hello"} 1.0
request_time_histogram_sum{env="PROD",url="/hello"} 0.0
# HELP request_time_histogram_created 接口耗时统计
# TYPE request_time_histogram_created gauge
request_time_histogram_created{env="PROD",url="/hello"} 1.7060823348361146e+09
# HELP failure_count_total 接口失败次数
# TYPE failure_count_total counter
```