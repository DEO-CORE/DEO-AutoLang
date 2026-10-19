import { spawn } from 'node:child_process'
import { existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const services = {
  'site-api': {
    folder: 'backend_side',
    args: ['manage.py', 'runserver', '127.0.0.1:4179'],
  },
  'platform-api': {
    folder: 'deo_auto_lang_backend',
    args: ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '4178'],
  },
  base: {
    folder: 'deo_auto_lang_base/catalog_backend',
    args: ['manage.py', 'runserver', '127.0.0.1:4180'],
  },
}

const service = services[process.argv[2]]
if (!service) {
  console.error(`Unknown service: ${process.argv[2] || '(missing)'}`)
  process.exit(2)
}

const windows = process.platform === 'win32'
const serviceDirectory = resolve(root, service.folder)
const venvPython = resolve(serviceDirectory, '.venv', windows ? 'Scripts/python.exe' : 'bin/python')
const python = existsSync(venvPython) ? venvPython : process.env.PYTHON || (windows ? 'python' : 'python3')
const args = service.folder === 'deo_auto_lang_backend'
  ? [...service.args.slice(0, 2), '--app-dir', serviceDirectory, ...service.args.slice(2)]
  : service.args
const env = { ...process.env }

if (service.folder === 'deo_auto_lang_backend' && !env.BASE_CATALOG_SERVICE_KEY) {
  env.BASE_CATALOG_SERVICE_KEY = 'local-dev-platform-only-key'
}

const child = spawn(python, args, { cwd: serviceDirectory, stdio: 'inherit', env })
child.on('error', (error) => {
  console.error(`Could not start ${process.argv[2]}: ${error.message}`)
  process.exitCode = 1
})
for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => child.kill(signal))
}
child.on('exit', (code, signal) => {
  if (signal) process.kill(process.pid, signal)
  else process.exitCode = code ?? 1
})
