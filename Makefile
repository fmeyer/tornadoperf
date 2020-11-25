go_perf:
	/usr/bin/k6 run --out influxdb=http://localhost:8086/k6perfdata k6/golang_local.js

perf:
	/usr/bin/k6 run --out influxdb=http://localhost:8086/k6perfdata k6/python_local.js