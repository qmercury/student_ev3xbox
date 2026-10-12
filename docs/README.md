# 학생용 EV3 Xbox — 문서 안내

> 2026-10-12 정리. 학생이 로봇 프로그램을 작성·업로드하는 **현재 운영 저장소**의 문서입니다.

- [README](../README.md) — Mac/Windows 복제 명령, 처음 사용, EV3 LCD·LED JSON 설정
- [VSCode 업로드 및 실행 가이드](python/vscode.md) — `main.py`, 학생별 `.vscode/ev3-target.json`, SSH, 업로드·정지·로그
- [EV3 Python Reference](python/README.md) — `python-ev3dev2` 기반 모터·센서·Xbox·비동기 학습
- [EV3 Robot ID 및 교사 서비스](https://github.com/qmercury/relay_ev3xbox/blob/main/docs/reference/xbox_service.md) — 학생 프로그램과 별도로 상주하는 Xbox 서비스
- [대회용 Relay 운영 계획](https://github.com/qmercury/relay_ev3xbox/blob/main/docs/relay/alliance-relay.md) — 교사 중계, Wi-Fi 구성 및 남은 검증
- [전체 개발 현황 및 다음 단계](https://github.com/qmercury/ev3XboxConnect/blob/main/docs/NEXT_STEPS.md)

현재 완료: EV3 1대에 VSCode 업로드·실행·정지 및 상태 LCD 표시는 실기 확인. JSON 문구/LED 설정은 구현·자동 테스트를 통과했지만 변경된 LED 색상의 EV3 실기 확인은 아직 남아 있습니다.

학생 개인 설정 파일(`.vscode/ev3-target.json`)은 Git에 업로드하지 않습니다. 학교에서 실습할 때에는 `main.py`의 학생 코드를 임의로 덮어쓰지 않습니다.
