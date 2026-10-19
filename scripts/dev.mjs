import { spawn } from 'node:child_process'
import { existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const isWindows = process.platform === 'win32'
const venvPython = (folder) => resolve(root, folder, '.venv', isWindows ? 'Scripts/python.exe' : 'bin/python')
const pythonFor = (folder) => existsSync(venvPython(folder)) ? venvPython(folder) : (process.env.PYTHON || (isWindows ? 'python' : 'python3'))
const localServiceEnv = {
  ...process.env,
  BASE_CATALOG_SERVICE_KEY: process.env.BASE_CATALOG_SERVICE_KEY || 'local-dev-platform-only-key',
}

const processes = [
  spawn(pythonFor('deo_auto_lang_backend'), ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '4178'], {
    cwd: resolve(root, 'deo_auto_lang_backend'), stdio: 'inherit', env: localServiceEnv,
  }),
  spawn(pythonFor('backend_side'), ['manage.py', 'runserver', '127.0.0.1:4179', '--noreload'], {
    cwd: resolve(root, 'backend_side'), stdio: 'inherit', env: process.env,
  }),
  spawn(pythonFor('deo_auto_lang_base/catalog_backend'), ['manage.py', 'runserver', '127.0.0.1:4180', '--noreload'], {
    cwd: resolve(root, 'deo_auto_lang_base/catalog_backend'), stdio: 'inherit', env: localServiceEnv,
  }),
  spawn(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', '5173'], {
    cwd: resolve(root, 'frontend_site'), stdio: 'inherit', env: process.env,
  }),
]

function stopAll() {
  for (const child of processes) if (child.exitCode === null) child.kill('SIGTERM')
}

process.on('SIGINT', stopAll)
process.on('SIGTERM', stopAll)
for (const child of processes) {
  child.on('error', (error) => {
    console.error(`Could not start a development service: ${error.message}`)
    process.exitCode = 1
    stopAll()
  })
  child.on('exit', (code) => {
  if (code !== null && code !== 0) process.exitCode = code
  stopAll()
  })
}
