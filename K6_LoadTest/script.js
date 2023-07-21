import http from 'k6/http';
import { sleep,check } from 'k6';
import {Trend}  from 'k6/metrics';

const trends = {
    scenario1 : new Trend("scenario1) Response Time",true),
    scenario2 : new Trend("scenario2) Response Time",true),
}
// 테스트 성공의 기준
const VUS = 10;
const DURATION = "30s";

export const options = {
    scenarios:{
        scenario1:{
            executor:"constant-vus",
            exec: "scenarioFunc",
            vus:VUS,
            duration:DURATION,
            env:{
                SCENARIO_ID:"1"
            },
        },
        scenario2:{
            executor:"constant-vus",
            exec: "scenarioFunc",
            vus:VUS,
            duration:DURATION,
            env:{
                SCENARIO_ID:"2"
            },
        },
    },
};

export function scenarioFunc(token) {
    const scenarioUrl = "https://www.naver.com"; // 실행할 API
    const scenario = http.get(scenarioUrl);
    __ENV.SCENARIO_ID === "1"
    ? trends.scenario1.add(scenario.timings.duration)
    : trends.scenario2.add(scenario.timings.duration);

    check(scenario, {"scenario status is 200": (res) => res.status === 200,});

    sleep(1);
}