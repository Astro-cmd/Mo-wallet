$djangoServer = Start-Process -FilePath "python" -ArgumentList "manage.py runserver" -PassThru
$nextServer = Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "./dashboard" -PassThru

Write-Host "Both servers are running..."
Write-Host "Django server running on http://localhost:8000"
Write-Host "Next.js server running on http://localhost:3000"
Write-Host "Press Ctrl+C to stop both servers"

try {
    Wait-Process -Id $djangoServer.Id, $nextServer.Id
} finally {
    if (-not $djangoServer.HasExited) { Stop-Process -Id $djangoServer.Id }
    if (-not $nextServer.HasExited) { Stop-Process -Id $nextServer.Id }
}