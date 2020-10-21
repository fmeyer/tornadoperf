tornadoperf on  master [!] via 🐍 v2.7.18 on ☁️  us-east-1
❯ echo 'GET http://localhost:8888/ping3' | vegeta attack -rate 50 -duration 10s  | tee results.bin | vegeta report
Requests      [total, rate, throughput]         500, 50.10, 50.04
Duration      [total, attack, wait]             9.992s, 9.98s, 11.934ms
Latencies     [min, mean, 50, 90, 95, 99, max]  9.107ms, 12.254ms, 12.096ms, 13.726ms, 14.027ms, 15.524ms, 20.307ms
Bytes In      [total, mean]                     8500, 17.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:500
Error Set:

tornadoperf on  master [!?] via 🐍 v2.7.18 on ☁️  us-east-1 took 10s
❯ echo 'GET http://localhost:8888/ping2' | vegeta attack -rate 50 -duration 10s  | tee results.bin | vegeta report
Requests      [total, rate, throughput]         500, 50.10, 50.09
Duration      [total, attack, wait]             9.981s, 9.98s, 1.238ms
Latencies     [min, mean, 50, 90, 95, 99, max]  1.078ms, 1.444ms, 1.396ms, 1.711ms, 1.822ms, 1.956ms, 3.922ms
Bytes In      [total, mean]                     12500, 25.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:500
Error Set:

tornadoperf on  master [!?] via 🐍 v2.7.18 on ☁️  us-east-1 took 10s
❯ echo 'GET http://localhost:8888/ping1' | vegeta attack -rate 50 -duration 10s  | tee results.bin | vegeta report
Requests      [total, rate, throughput]         500, 50.10, 50.09
Duration      [total, attack, wait]             9.982s, 9.98s, 2.41ms
Latencies     [min, mean, 50, 90, 95, 99, max]  1.99ms, 2.516ms, 2.476ms, 2.827ms, 2.988ms, 3.31ms, 4.256ms
Bytes In      [total, mean]                     7500, 15.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:500
Error Set:

tornadoperf on  master [!?] via 🐍 v2.7.18 on ☁️  us-east-1 took 10s
❯ echo 'GET http://localhost:8080/ping' | vegeta attack -rate 50 -duration 10s  | tee results.bin | vegeta report
Requests      [total, rate, throughput]         500, 50.10, 50.10
Duration      [total, attack, wait]             9.98s, 9.98s, 231.848µs
Latencies     [min, mean, 50, 90, 95, 99, max]  176.432µs, 292.289µs, 276.187µs, 378.739µs, 418.3µs, 505.143µs, 1.321ms
Bytes In      [total, mean]                     3000, 6.00
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:500
Error Set:
