import http from "k6/http";

export let options = {
    stages: [
        { duration: "1m", target: 100  },
        { duration: "2m", target: 200 },
        { duration: "10m", target: 200 },
        // { duration: "3m", target: 300 },
        // { duration: "4m", target: 400 },
        // { duration: "5m", target: 500 },
    ],

    ext: {
        loadimpact: {
          projectID: 3515783,
          name: "golang"
        }
      }
    ,
    "thresholds": {
        "http_req_duration": ["avg<100", "p(95)<200"]
      },
    "noConnectionReuse": true,
};


export default function() {
    let response = http.get("http://localhost:8080/random");
};
