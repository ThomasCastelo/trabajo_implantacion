Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VERIFICADOR DE AUTO-UPDATE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar GitHub Actions
Write-Host "[1/4] Verificando GitHub Actions..." -ForegroundColor Yellow
Write-Host "      Abre: https://github.com/Thomas-Casot/fastapi_plantillascomunes/actions"
Write-Host ""
Read-Host "      Presiona ENTER cuando veas todos los checks en verde"

# 2. Verificar Docker Hub  
Write-Host ""
Write-Host "[2/4] Verificando Docker Hub..." -ForegroundColor Yellow
Write-Host "      Abre: https://hub.docker.com/r/thomascasot/museo-dinosaurios/tags"
Write-Host ""
Read-Host "      Presiona ENTER cuando veas el tag 'latest' actualizado"

# 3. Esperar Watchtower
Write-Host ""
Write-Host "[3/4] Esperando a Watchtower..." -ForegroundColor Yellow
Write-Host "      Watchtower revisara en los proximos 5 minutos"
Write-Host ""

$segundos = 300
for ($i = $segundos; $i -gt 0; $i--) {
    $minutos = [math]::Floor($i / 60)
    $segs = $i % 60
    Write-Host "`r      Tiempo maximo de espera: $minutos m $segs s" -NoNewline -ForegroundColor Cyan
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host ""

# 4. Verificar aplicación
Write-Host "[4/4] Verificando actualizacion..." -ForegroundColor Yellow
docker logs museo-dinosaurios-app --tail 10
Write-Host ""

Write-Host "Abriendo http://localhost:8000/docs..." -ForegroundColor Green
Start-Process "http://localhost:8000/docs"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "�� VERIFICACION COMPLETA" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Deberias ver el titulo actualizado:" -ForegroundColor Yellow
Write-Host "  'Museo de Dinosaurios - AUTO-UPDATE FUNCIONANDO'" -ForegroundColor Green
Write-Host ""
