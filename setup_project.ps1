# setup_empty_project.ps1
# Скрипт для создания структуры проекта tennis_scoreboard
# Фронтенд (HTML, css/, js/, images/) в templates/, без Flask

Write-Host "Setting up tennis_scoreboard project structure with frontend in templates/..."

# Проверка текущей директории
$projectDir = Get-Location
Write-Host "Current directory: $projectDir"
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "Error: pyproject.toml not found. Are you in the correct project directory?"
    exit 1
}

# Проверка политики выполнения
$policy = Get-ExecutionPolicy
if ($policy -eq "Restricted") {
    Write-Host "Execution policy is Restricted. Setting to RemoteSigned..."
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
}

# Удаление старой структуры src/tennis_scoreboard/ (опционально)
$srcDir = Join-Path $projectDir "src/tennis_scoreboard"
if (Test-Path $srcDir) {
    Write-Host "Existing src/tennis_scoreboard found. Remove it? (y/n)"
    $response = Read-Host
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force $srcDir
        Write-Host "Removed $srcDir"
    }
}

# Создание структуры папок
$dirs = @(
    "src/tennis_scoreboard/models",
    "src/tennis_scoreboard/services",
    "src/tennis_scoreboard/controllers",
    "src/tennis_scoreboard/templates/css",
    "src/tennis_scoreboard/templates/js",
    "src/tennis_scoreboard/templates/images",
    "src/tennis_scoreboard/tests",
    "src/tennis_scoreboard/migrations"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "Created $dir"
}

# Создание пустых Python-файлов
$pythonFiles = @(
    "src/tennis_scoreboard/__init__.py",
    "src/tennis_scoreboard/models/__init__.py",
    "src/tennis_scoreboard/models/player.py",
    "src/tennis_scoreboard/models/match.py",
    "src/tennis_scoreboard/services/__init__.py",
    "src/tennis_scoreboard/services/match_service.py",
    "src/tennis_scoreboard/services/score_service.py",
    "src/tennis_scoreboard/controllers/__init__.py",
    "src/tennis_scoreboard/controllers/web_controller.py",
    "src/tennis_scoreboard/tests/__init__.py",
    "src/tennis_scoreboard/tests/test_score.py"
)
foreach ($file in $pythonFiles) {
    New-Item -ItemType File -Path $file -Force | Out-Null
    Set-Content -Path $file -Value "# Placeholder for Python module"
    Write-Host "Created $file"
}

# Скачивание и копирование файлов из zhukovsd в templates/
Write-Host "Downloading zhukovsd/tennis-scoreboard-html-layouts..."
$tempDir = Join-Path $projectDir "temp_layouts"
git clone https://github.com/zhukovsd/tennis-scoreboard-html-layouts $tempDir
if (Test-Path $tempDir) {
    Copy-Item -Recurse "$tempDir/css/*" "src/tennis_scoreboard/templates/css/" -Force
    Copy-Item -Recurse "$tempDir/js/*" "src/tennis_scoreboard/templates/js/" -Force
    Copy-Item -Recurse "$tempDir/images/*" "src/tennis_scoreboard/templates/images/" -Force
    Copy-Item "$tempDir/index.html" "src/tennis_scoreboard/templates/index.html" -Force
    Copy-Item "$tempDir/new-match.html" "src/tennis_scoreboard/templates/new-match.html" -Force
    Copy-Item "$tempDir/match-score.html" "src/tennis_scoreboard/templates/match-score.html" -Force
    Copy-Item "$tempDir/matches.html" "src/tennis_scoreboard/templates/matches.html" -Force
    Remove-Item -Recurse -Force $tempDir
    Write-Host "Integrated frontend files from zhukovsd/tennis-scoreboard-html-layouts into src/tennis_scoreboard/templates/"
} else {
    Write-Host "Failed to clone layouts repository. Downloading ZIP as fallback..."
    Invoke-WebRequest -Uri https://github.com/zhukovsd/tennis-scoreboard-html-layouts/archive/refs/heads/main.zip -OutFile temp_layouts.zip
    Expand-Archive temp_layouts.zip -DestinationPath $tempDir
    Copy-Item -Recurse "$tempDir/tennis-scoreboard-html-layouts-main/css/*" "src/tennis_scoreboard/templates/css/" -Force
    Copy-Item -Recurse "$tempDir/tennis-scoreboard-html-layouts-main/js/*" "src/tennis_scoreboard/templates/js/" -Force
    Copy-Item -Recurse "$tempDir/tennis_scoreboard-html-layouts-main/images/*" "src/tennis_scoreboard/templates/images/" -Force
    Copy-Item "$tempDir/tennis-scoreboard-html-layouts-main/index.html" "src/tennis_scoreboard/templates/index.html" -Force
    Copy-Item "$tempDir/tennis-scoreboard-html-layouts-main/new-match.html" "src/tennis_scoreboard/templates/new-match.html" -Force
    Copy-Item "$tempDir/tennis_scoreboard-html-layouts-main/match-score.html" "src/tennis_scoreboard/templates/match-score.html" -Force
    Copy-Item "$tempDir/tennis_scoreboard-html-layouts-main/matches.html" "src/tennis_scoreboard/templates/matches.html" -Force
    Remove-Item -Recurse -Force $tempDir
    Remove-Item -Force temp_layouts.zip
    Write-Host "Integrated frontend files from ZIP"
}

# Обновление .gitignore
$gitignore = @'
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
*.egg-info/
dist/
build/
migrations/versions/
temp_layouts/
temp_layouts.zip
'@
Set-Content -Path ".gitignore" -Value $gitignore
Write-Host "Updated .gitignore"

# Проверка Ruff
Write-Host "Running Ruff check..."
rye run ruff check src/tennis_scoreboard

# Git: добавление и коммит
Write-Host "Committing changes to Git..."
git add .
git commit -m "Setup project structure with frontend in templates/ without Flask" -m "Generated by setup_empty_project.ps1"
git push

Write-Host "Project setup complete! Frontend files in src/tennis_scoreboard/templates/."
Write-Host "Python modules in models/, services/, controllers/, tests/."
Write-Host "Next steps: Implement backend logic in Python modules."