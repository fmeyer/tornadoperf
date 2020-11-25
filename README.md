# Base tornado perf image

## utilities 

- perf tooling k6 + grafana + influxdb
- upstream golang http server


## Grafana


import dashboard https://grafana.com/grafana/dashboards/2587

run perf 

    k6 run --out influxdb=http://localhost:8086/k6perfdata k6/golang_local.js

    k6 run --out influxdb=http://localhost:8086/k6perfdata k6/python_local.js


## sample test

    ❯ make perf
    /usr/bin/k6 run --out influxdb=http://localhost:8086/k6perfdata k6/python_local.js

            /\      |‾‾| /‾‾/   /‾‾/
       /\  /  \     |  |/  /   /  /
      /  \/    \    |     (   /   ‾‾\
     /          \   |  |\  \ |  (‾)  |
    / __________ \  |__| \__\ \_____/ .io

    execution: local
        script: k6/python_local.js
        output: influxdb=http://localhost:8086/k6perfdata (http://localhost:8086)

    scenarios: (100.00%) 1 scenario, 500 max VUs, 15m30s max duration (incl. graceful stop):
            * default: Up to 500 looping VUs for 15m0s over 5 stages (gracefulRampDown: 30s, gracefulStop: 30s)

    WARN[0666] Request Failed                                error="Get \"http://localhost:9000/ping2\": read tcp 127.0.0.1:36458->127.0.0.1:9000: read: connection reset by peer"

    running (15m00.3s), 000/500 VUs, 1161934 complete and 0 interrupted iterations
    default ✓ [======================================] 000/500 VUs  15m0s

    data_received..............: 1.4 GB  1.6 MB/s
    data_sent..................: 121 MB  134 kB/s
    http_req_blocked...........: avg=132.61µs min=50.34µs  med=110.13µs max=64.66ms  p(90)=175.85µs p(95)=210.6µs
    http_req_connecting........: avg=95.4µs   min=34.14µs  med=75.53µs  max=64.64ms  p(90)=121.18µs p(95)=146.5µs
    ✗ http_req_duration..........: avg=244.78ms min=232.3µs  med=257.63ms max=560.82ms p(90)=385.44ms p(95)=407.27ms
    http_req_receiving.........: avg=64.83µs  min=0s       med=56.45µs  max=24.24ms  p(90)=100.33µs p(95)=125.37µs
    http_req_sending...........: avg=42.32µs  min=13.78µs  med=39.01µs  max=23.72ms  p(90)=61.47µs  p(95)=71.04µs
    http_req_tls_handshaking...: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s
    http_req_waiting...........: avg=244.67ms min=154.24µs med=257.52ms max=560.73ms p(90)=385.33ms p(95)=407.16ms
    http_reqs..................: 1161934 1290.620708/s
    iteration_duration.........: avg=244.96ms min=536.14µs med=257.81ms max=561.01ms p(90)=385.63ms p(95)=407.46ms
    iterations.................: 1161934 1290.620708/s
    vus........................: 499     min=2   max=499
    vus_max....................: 500     min=500 max=500

    ERRO[0903] some thresholds have failed
    make: *** [Makefile:5: perf] Error 99

![alt](https://i.imgur.com/nmi3l00.png)