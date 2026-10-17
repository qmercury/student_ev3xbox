'use strict';

const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const dgram = require('dgram');
const { execFile } = require('child_process');
const { promisify } = require('util');
const { Client } = require('ssh2');

const execFileAsync = promisify(execFile);
const DISCOVERY_PORT = 5005;
const DISCOVERY_MILLISECONDS = 3500;
const SSH_PORT = 22;
const ID_PATTERN = /^[A-Za-z0-9._-]{1,32}$/;
let activePanel;

function shellQuote(value) {
  return "'" + String(value).replace(/'/g, "'\\''") + "'";
}

function keyFiles() {
  const privateKey = path.join(os.homedir(), '.ssh', 'ev3_classroom_ed25519');
  return { privateKey, publicKey: privateKey + '.pub' };
}

function findStudentRoot() {
  const folders = vscode.workspace.workspaceFolders || [];
  for (const folder of folders) {
    const candidate = folder.uri.fsPath;
    if (fs.existsSync(path.join(candidate, '.vscode', 'ev3-target.example.json'))) {
      return candidate;
    }
  }
  return null;
}

function isValidIp(ip) {
  if (typeof ip !== 'string') return false;
  const octets = ip.split('.');
  return octets.length === 4 && octets.every((s) =>
    /^\d{1,3}$/.test(s) && Number(s) >= 0 && Number(s) <= 255
  );
}

async function discoverEv3() {
  return new Promise((resolve, reject) => {
    const socket = dgram.createSocket('udp4');
    const byRobotId = new Map();
    let completed = false;
    let queryInterval;
    let finishTimer;

    function finish(error) {
      if (completed) return;
      completed = true;
      clearInterval(queryInterval);
      clearTimeout(finishTimer);
      try { socket.close(); } catch (_) {}
      if (error) {
        reject(error);
      } else {
        const list = Array.from(byRobotId.entries()).map(([robot_id, ips]) => ({
          robot_id, ip: [...ips][0], conflict: ips.size !== 1
        }));
        resolve(list.sort((a, b) => a.robot_id.localeCompare(b.robot_id)));
      }
    }

    socket.on('error', finish);
    socket.on('message', (bytes, address) => {
      try {
        const packet = JSON.parse(bytes.toString('utf8'));
        const robotId = packet.robot_id;
        if (packet.type !== 'ev3_discover_reply' ||
            !ID_PATTERN.test(String(robotId || '')) ||
            packet.service_port !== DISCOVERY_PORT ||
            !isValidIp(address.address)) return;
        if (!byRobotId.has(robotId)) byRobotId.set(robotId, new Set());
        byRobotId.get(robotId).add(address.address);
      } catch (_) {
        // Ignore unrelated or malformed broadcast responses.
      }
    });

    socket.bind(0, '0.0.0.0', () => {
      try { socket.setBroadcast(true); } catch (error) { finish(error); return; }
      const message = Buffer.from(JSON.stringify({ type: 'discover_request', version: 1 }));
      function query() {
        if (!completed) socket.send(message, DISCOVERY_PORT, '255.255.255.255', () => {});
      }
      query();
      queryInterval = setInterval(query, 400);
      finishTimer = setTimeout(() => finish(null), DISCOVERY_MILLISECONDS);
    });
  });
}

async function makeKeyIfNecessary() {
  const files = keyFiles();
  const hasPrivate = fs.existsSync(files.privateKey);
  const hasPublic = fs.existsSync(files.publicKey);
  if (hasPrivate !== hasPublic) {
    throw new Error('SSH 개인키와 공개키 중 하나가 없습니다. 교사에게 키 파일 확인을 요청하세요.');
  }
  if (!hasPrivate) {
    fs.mkdirSync(path.dirname(files.privateKey), { recursive: true, mode: 0o700 });
    try {
      await execFileAsync('ssh-keygen', [
        '-t', 'ed25519', '-f', files.privateKey, '-N', '', '-C', 'ev3-classroom'
      ], { timeout: 20000, windowsHide: true });
    } catch (error) {
      throw new Error('SSH 키 생성에 실패했습니다. OpenSSH 클라이언트가 설치되어 있는지 확인하세요. ' + error.message);
    }
  }
  const publicKey = fs.readFileSync(files.publicKey, 'utf8').trim();
  if (!/^ssh-ed25519 [A-Za-z0-9+/=]+(?: .*)?$/.test(publicKey)) {
    throw new Error('공개키 형식이 올바르지 않습니다.');
  }
  return { ...files, publicKey };
}

function sshConnection(host, credentials, robotId, context) {
  return new Promise((resolve, reject) => {
    const client = new Client();
    let complete = false;
    let trustedFingerprint = null;
    let verifierRejected = false;

    function rejectOnce(error) {
      if (complete) return;
      complete = true;
      try { client.end(); } catch (_) {}
      const result = error instanceof Error ? error : new Error(String(error));
      if (verifierRejected) result.hostKeyRejected = true;
      reject(result);
    }

    client.on('error', rejectOnce);
    client.on('ready', async () => {
      if (complete) return;
      complete = true;
      if (trustedFingerprint) {
        await context.globalState.update('trustedHostKey:' + robotId, trustedFingerprint);
      }
      resolve(client);
    });

    const config = {
      host, port: SSH_PORT, username: 'robot', readyTimeout: 12000,
      hostHash: 'sha256',
      hostVerifier: (fingerprint, verify) => {
        const previouslyTrusted = context.globalState.get('trustedHostKey:' + robotId);
        if (previouslyTrusted) {
          if (previouslyTrusted === fingerprint) {
            trustedFingerprint = fingerprint;
            verify(true);
          } else {
            verifierRejected = true;
            vscode.window.showErrorMessage(
              robotId + '의 SSH 서버 키가 이전과 다릅니다. 다른 로봇이거나 재설치된 장치일 수 있습니다. 연결을 차단했습니다.'
            );
            verify(false);
          }
          return;
        }
        vscode.window.showWarningMessage(
          robotId + ' (' + host + ')의 SSH 서버 키를 처음 등록합니다.\nSHA256 지문(16진수): ' +
          fingerprint + '\n선택한 EV3가 맞는지 교사가 확인해 주세요.',
          { modal: true }, '이 EV3 신뢰'
        ).then((choice) => {
          if (choice === '이 EV3 신뢰') {
            trustedFingerprint = fingerprint;
            verify(true);
          } else {
            verifierRejected = true;
            verify(false);
          }
        }, () => {
          verifierRejected = true;
          verify(false);
        });
      }
    };
    if (credentials.privateKey) config.privateKey = credentials.privateKey;
    if (credentials.password) config.password = credentials.password;
    try { client.connect(config); } catch (error) { rejectOnce(error); }
  });
}

function executeSsh(client, script) {
  return new Promise((resolve, reject) => {
    client.exec('sh -lc ' + shellQuote(script), (error, stream) => {
      if (error) { reject(error); return; }
      let stdout = '';
      let stderr = '';
      stream.on('data', (bytes) => { stdout += bytes.toString('utf8').slice(0, 4000); });
      stream.stderr.on('data', (bytes) => { stderr += bytes.toString('utf8').slice(0, 1000); });
      stream.on('error', reject);
      stream.on('close', (code) => {
        if (code === 0) resolve(stdout);
        else reject(new Error('EV3 설정 실패 (exit ' + code + '): ' + stderr.slice(0, 500)));
      });
    });
  });
}

function saveStudentConfig(root, robotId, ip, privateKey) {
  const configDir = path.join(root, '.vscode');
  const configPath = path.join(configDir, 'ev3-target.json');
  const samplePath = path.join(configDir, 'ev3-target.example.json');
  const source = fs.existsSync(configPath) ? configPath : samplePath;
  const config = JSON.parse(fs.readFileSync(source, 'utf8'));
  config.robot_id = robotId;
  config.host = ip;
  config.user = 'robot';
  config.identity_file = privateKey;
  const tempPath = configPath + '.tmp';
  try {
    fs.writeFileSync(tempPath, JSON.stringify(config, null, 2) + '\n', { encoding: 'utf8', mode: 0o600 });
    fs.renameSync(tempPath, configPath);
  } finally {
    if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
  }
}

async function pairEv3(context, root, robotId, ip) {
  const files = await makeKeyIfNecessary();
  const privateKey = fs.readFileSync(files.privateKey);

  // Reuse an already-authorized key without requesting a password.
  let client;
  try {
    client = await sshConnection(ip, { privateKey }, robotId, context);
    await executeSsh(client, 'printf "KEY_AUTH=OK\\n"');
  } catch (error) {
    if (error.hostKeyRejected) throw error;
    if (client) { client.end(); client = null; }
    const password = await vscode.window.showInputBox({
      title: robotId + ' 최초 인증 (교사 입력)',
      prompt: 'EV3 robot 계정의 비밀번호를 입력하세요. 초기 설정을 변경하지 않았다면 maker입니다.',
      password: true,
      ignoreFocusOut: true,
      placeHolder: 'EV3 비밀번호',
      validateInput: (value) => value ? null : '비밀번호를 입력하세요.'
    });
    if (password === undefined) throw new Error('교사가 최초 인증을 취소했습니다.');
    try {
      client = await sshConnection(ip, { password }, robotId, context);
      const installScript = [
        'set -e',
        'umask 077',
        'mkdir -p "$HOME/.ssh"',
        'chmod 700 "$HOME/.ssh"',
        'touch "$HOME/.ssh/authorized_keys"',
        'chmod 600 "$HOME/.ssh/authorized_keys"',
        'key=' + shellQuote(files.publicKey),
        'grep -qxF "$key" "$HOME/.ssh/authorized_keys" || printf "%s\\n" "$key" >> "$HOME/.ssh/authorized_keys"',
        'echo SSH_KEY=INSTALLED'
      ].join('\n');
      const output = await executeSsh(client, installScript);
      if (!output.includes('SSH_KEY=INSTALLED')) {
        throw new Error('EV3가 SSH 키 설치를 확인하지 않았습니다.');
      }
    } finally {
      if (client) client.end();
      client = null;
    }
    // Confirm future student deployment can authenticate without a password.
    client = await sshConnection(ip, { privateKey }, robotId, context);
    await executeSsh(client, 'echo SSH_KEY=OK');
  } finally {
    if (client) client.end();
  }
  saveStudentConfig(root, robotId, ip, files.privateKey);
}

async function executeDeployTask() {
  const tasks = await vscode.tasks.fetchTasks();
  const target = tasks.find((task) => task.name === 'EV3: 업로드 및 실행');
  if (!target) {
    throw new Error('학생용 프로젝트를 열고 EV3: 업로드 및 실행 작업이 있는지 확인하세요.');
  }
  await vscode.tasks.executeTask(target);
}

function pageHtml(nonce) {
  return [
    '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'nonce-' + nonce + '\'; script-src \'nonce-' + nonce + '\';">',
    '<title>EV3 최초 연결 도우미</title>',
    '<style nonce="' + nonce + '">',
    'body{font-family:var(--vscode-font-family);color:var(--vscode-foreground);padding:22px;max-width:760px;margin:auto;line-height:1.6}',
    'h1{font-size:22px;margin:0 0 8px}h2{font-size:16px;margin:18px 0 10px}',
    '.sub{color:var(--vscode-descriptionForeground);margin:0 0 18px}',
    'button{padding:9px 14px;border:0;border-radius:6px;background:var(--vscode-button-background);color:var(--vscode-button-foreground);cursor:pointer;font:inherit}',
    'button:hover{background:var(--vscode-button-hoverBackground)}button:disabled{opacity:.5;cursor:not-allowed}',
    '.secondary{background:var(--vscode-button-secondaryBackground);color:var(--vscode-button-secondaryForeground)}',
    '.card{border:1px solid var(--vscode-panel-border);border-radius:8px;padding:12px;margin:8px 0}',
    '.card.selected{outline:2px solid var(--vscode-focusBorder)}.card button{width:100%;text-align:left;background:transparent;color:inherit}',
    '.muted{color:var(--vscode-descriptionForeground);font-size:12px}',
    '.status{border-left:3px solid var(--vscode-focusBorder);padding:10px 12px;background:var(--vscode-editorWidget-background);margin:12px 0;white-space:pre-line}',
    '.row{display:flex;gap:8px;flex-wrap:wrap}.good{color:var(--vscode-testing-iconPassed)}.warn{color:var(--vscode-errorForeground)}',
    '</style></head><body>',
    '<h1>EV3 최초 연결 도우미</h1>',
    '<p class="sub">Mac·Windows 공통 · 학생은 로봇을 선택하고 교사가 최초 인증을 진행합니다.</p>',
    '<p>① EV3와 노트북을 같은 Wi-Fi에 연결하고 EV3의 Xbox 서비스를 실행하세요.</p>',
    '<button id="scan">EV3 자동 검색</button>',
    '<h2>② 발견된 EV3 로봇</h2><div id="devices" class="muted">검색 버튼을 눌러주세요.</div>',
    '<div class="row"><button id="pair" disabled>선택한 EV3 최초 연결</button>',
    '<button id="deploy" class="secondary" disabled>프로그램 업로드 및 실행</button></div>',
    '<div class="status" id="status" role="status" aria-live="polite">준비됨</div>',
    '<p class="muted">SSH 개인키는 노트북의 .ssh 폴더에만 저장됩니다. 교사 비밀번호는 저장하지 않습니다. 최초 연결 후에는 Ctrl + Shift + B를 사용하세요.</p>',
    '<script nonce="' + nonce + '">',
    'const vscode=acquireVsCodeApi();',
    'const scan=document.getElementById("scan"),pair=document.getElementById("pair"),deploy=document.getElementById("deploy"),devicesEl=document.getElementById("devices"),statusEl=document.getElementById("status");',
    'let devices=[],selected=null,busy=false,paired=false;',
    'function update(){scan.disabled=busy;pair.disabled=busy||!selected||selected.conflict;deploy.disabled=busy||!paired;}',
    'function render(){devicesEl.replaceChildren();if(!devices.length){devicesEl.textContent="검색된 EV3가 없습니다. 같은 Wi-Fi와 EV3 Xbox 서비스를 확인하세요.";return;}',
    'for(const d of devices){const outer=document.createElement("div");outer.className="card"+(selected&&selected.robot_id===d.robot_id?" selected":"");',
    'const item=document.createElement("button");item.type="button";item.disabled=busy||d.conflict;',
    'item.textContent=d.robot_id+"  ·  "+d.ip+(d.conflict?"  (동일 ID 중복: 교사 확인 필요)":"");',
    'item.onclick=()=>{selected=d;paired=false;render();update();};outer.appendChild(item);devicesEl.appendChild(outer);}}',
    'scan.onclick=()=>{busy=true;paired=false;selected=null;devices=[];statusEl.textContent="EV3 검색 중…";render();update();vscode.postMessage({type:"scan"});};',
    'pair.onclick=()=>{if(!selected||busy)return;busy=true;statusEl.textContent="최초 연결 중… 교사의 인증 확인이 필요할 수 있습니다.";update();vscode.postMessage({type:"pair",robot_id:selected.robot_id,ip:selected.ip});};',
    'deploy.onclick=()=>{if(busy||!paired)return;vscode.postMessage({type:"deploy"});};',
    'window.addEventListener("message",event=>{const m=event.data;',
    'if(m.type==="scanResult"){devices=m.devices||[];busy=false;render();statusEl.textContent=devices.length? "로봇을 선택하세요.":"로봇을 찾지 못했습니다.";update();}',
    'if(m.type==="pairResult"){busy=false;paired=!!m.ok;statusEl.textContent=m.message;statusEl.className="status "+(m.ok?"good":"warn");update();}',
    'if(m.type==="error"){busy=false;statusEl.textContent=m.message;statusEl.className="status warn";update();}',
    'if(m.type==="info"){statusEl.textContent=m.message;}});',
    '</script></body></html>'
  ].join('\n');
}

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('robottagram.ev3Connect', async () => {
    const root = findStudentRoot();
    if (!root) {
      vscode.window.showErrorMessage('VSCode에서 student_ev3xbox 프로젝트 폴더를 먼저 열어주세요.');
      return;
    }
    if (activePanel) { activePanel.reveal(); return; }

    const panel = vscode.window.createWebviewPanel(
      'robottagramEv3Connect', 'EV3 최초 연결 도우미',
      vscode.ViewColumn.One, { enableScripts: true, retainContextWhenHidden: true }
    );
    activePanel = panel;
    panel.onDidDispose(() => { activePanel = null; });
    panel.webview.html = pageHtml(crypto.randomBytes(18).toString('base64'));
    let candidates = [];

    panel.webview.onDidReceiveMessage(async (message) => {
      try {
        if (message.type === 'scan') {
          candidates = await discoverEv3();
          panel.webview.postMessage({ type: 'scanResult', devices: candidates });
        } else if (message.type === 'pair') {
          const robotId = String(message.robot_id || '');
          const ip = String(message.ip || '');
          const allowed = candidates.some((d) =>
            d.robot_id === robotId && d.ip === ip && !d.conflict
          );
          if (!allowed) throw new Error('검색 목록에 없는 로봇입니다. 다시 검색해주세요.');
          await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: robotId + ' 최초 SSH 연결 설정',
            cancellable: false
          }, () => pairEv3(context, root, robotId, ip));
          panel.webview.postMessage({
            type: 'pairResult', ok: true,
            message: robotId + ' 연결 준비 완료! 이제 Ctrl + Shift + B로 업로드할 수 있습니다.'
          });
        } else if (message.type === 'deploy') {
          await executeDeployTask();
          panel.webview.postMessage({ type: 'info', message: '업로드 작업을 시작했습니다. VSCode 터미널의 실행 결과를 확인하세요.' });
        }
      } catch (error) {
        panel.webview.postMessage({
          type: message.type === 'pair' ? 'pairResult' : 'error',
          ok: false, message: String(error.message || error)
        });
      }
    });
  }));
}

function deactivate() {}

module.exports = { activate, deactivate };
