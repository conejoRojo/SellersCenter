const { spawn } = require('child_process');
const fs = require('fs');
const CF = 'C:\\Program Files (x86)\\cloudflared\\cloudflared.exe';
const svcs = [{ p: 5173, n: 'Frontend Seller' }, { p: 5174, n: 'Frontend Aper' }, { p: 8001, n: 'Backend API' }];
const urls = {};

for (const s of svcs) {
  const pr = spawn(CF, ['tunnel', '--url', 'http://127.0.0.1:' + s.p], { stdio: ['ignore', 'pipe', 'pipe'] });
  const fn = d => {
    const m = d.toString().match(/https:\/\/[a-z0-9\-]+\.trycloudflare\.com/);
    if (m && !urls[s.n]) {
      urls[s.n] = m[0];
      process.stdout.write(s.n + ' -> ' + m[0] + '\n');
      if (Object.keys(urls).length === 3) {
        fs.writeFileSync('tunnel_urls.json', JSON.stringify(urls, null, 2), 'utf8');
        process.stdout.write('DONE\n');
        process.exit(0);
      }
    }
  };
  pr.stdout.on('data', fn);
  pr.stderr.on('data', fn);
}
