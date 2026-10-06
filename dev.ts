import { spawn } from 'node:child_process';

function start(label: string, args: string[], envOverride: Record<string, string>) {
  const child = spawn('bun', args, {
    stdio: 'inherit',
    env: {
      ...process.env,
      ...envOverride,
    },
  });

  child.on('error', (err) => {
    console.error(`[${label}] spawn error`, err);
  });

  child.on('exit', (code, signal) => {
    console.error(`[${label}] exited`, { code, signal });
  });

  return child;
}

function main() {
  const api = start('api', ['run', 'server']);
  const frontend = start('frontend', ['run', 'dev']);

  const shutdown = () => {
    [api, frontend].forEach((p) => p.kill('SIGTERM'));
    process.exit(0);
  };

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

main();
