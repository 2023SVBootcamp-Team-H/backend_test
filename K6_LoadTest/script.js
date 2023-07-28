import http from 'k6/http';
import { sleep, check } from 'k6';
import { Trend } from 'k6/metrics';

const BASE_URL = 'http://34.195.3.25:5000';
const JSON_HEADER = { headers: { 'Content-Type': 'application/json' } };
const PAYLOAD = JSON.stringify({ /* 필요한 데이터 추가 */ });

const trends = {
    getAnswer: new Trend("GET /answer Response Time", true),
    postAnswer: new Trend("POST /answer Response Time", true),
    getWorry: new Trend("GET /worry/1 Response Time", true),
    deleteAnswer: new Trend("DELETE /answer/1 Response Time", true),
    getTestWorry: new Trend("GET /worry/test/1 Response Time", true),
    putWorry: new Trend("PUT /worry Response Time", true),
}

export const options = {
    scenarios: {
        getAnswerScenario: {
            executor: "constant-vus",
            exec: "getAnswerFunc",
            vus: 10,
            duration: "30s",
        },
        postAnswerScenario: {
            executor: "constant-vus",
            exec: "postAnswerFunc",
            vus: 10,
            duration: "30s",
        },
        getWorryScenario: {
            executor: "constant-vus",
            exec: "getWorryFunc",
            vus: 10,
            duration: "30s",
        },
        deleteAnswerScenario: {
            executor: "constant-vus",
            exec: "deleteAnswerFunc",
            vus: 10,
            duration: "30s",
        },
        getTestWorryScenario: {
            executor: "constant-vus",
            exec: "getTestWorryFunc",
            vus: 10,
            duration: "30s",
        },
        putWorryScenario: {
            executor: "constant-vus",
            exec: "putWorryFunc",
            vus: 10,
            duration: "30s",
        },
    },
};

function runScenario(path, method, trend, payload = null, params = null) {
    const url = `${BASE_URL}${path}`;
    const scenario = http.request(method, url, payload, params);
    trend.add(scenario.timings.duration);
    check(scenario, { "status is 200": (res) => res.status === 200 });
    sleep(1);
}

export function getAnswerFunc() {
    runScenario('/answer/', 'GET', trends.getAnswer);
}

export function postAnswerFunc() {
    runScenario('/answer/', 'POST', trends.postAnswer, PAYLOAD, JSON_HEADER);
}

export function getWorryFunc() {
    runScenario('/worry/1', 'GET', trends.getWorry);
}

// export function deleteAnswerFunc() {
//     runScenario('/answer/1', 'DELETE', trends.deleteAnswer);
// }

export function getTestWorryFunc() {
    runScenario('/worry/test/1', 'GET', trends.getTestWorry);
}

// export function putWorryFunc() {
//     runScenario('/worry/', 'PUT', trends.putWorry, PAYLOAD, JSON_HEADER);
// }
