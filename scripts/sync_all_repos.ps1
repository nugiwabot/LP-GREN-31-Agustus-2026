# ==========================================================
# UNIVERSAL GIT AUTO-SYNC FOR ALL LOCAL REPOSITORIES
# ==========================================================

# Daftar folder yang dipindai (bisa ditambah folder lain jika perlu):
$ROOT_DIRS = @(
    "C:\Users\Nugi\Documents",
    "C:\Users\Nugi\Desktop",
    "C:\Users\Nugi\Projects",
    "D:\",
    "E:\"
)

$INTERVAL_DETIK = 180  # Cek otomatis setiap 3 menit

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "🤖 Universal Multi-Directory Git Auto-Sync Aktif!" -ForegroundColor Green
Write-Host "📁 Memantau semua repository Git di lokasi berikut:" -ForegroundColor Yellow
$ROOT_DIRS | ForEach-Object { if (Test-Path $_) { Write-Host "   - $_" -ForegroundColor White } }
Write-Host "======================================================" -ForegroundColor Cyan

while ($true) {
    $time = Get-Date -Format "HH:mm:ss"
    
    foreach ($dir in $ROOT_DIRS) {
        if (-not (Test-Path $dir)) { continue }

        # Cari semua subfolder yang memiliki folder .git
        $gitFolders = Get-ChildItem -Path $dir -Directory -Recurse -Depth 2 -Force -ErrorAction SilentlyContinue | 
                      Where-Object { Test-Path (Join-Path $_.FullName ".git") }

        foreach ($repo in $gitFolders) {
            $repoPath = $repo.FullName
            $repoName = $repo.Name

            Push-Location $repoPath
            try {
                # Fetch update dari remote diam-diam
                git fetch --quiet origin 2>$null

                $LOCAL = git rev-parse HEAD 2>$null
                $REMOTE = git rev-parse '@{u}' 2>$null

                if ($LOCAL -and $REMOTE -and ($LOCAL -ne $REMOTE)) {
                    $branch = git branch --show-current
                    Write-Host "[$time] ⚡ [$repoName ($branch)] Ditemukan commit baru dari komputer lain! Menarik file..." -ForegroundColor Green
                    git pull --autostash origin $branch
                }
            } catch {
                # Abaikan error koneksi sementara
            } finally {
                Pop-Location
            }
        }
    }

    Start-Sleep -Seconds $INTERVAL_DETIK
}
