# Monitor de Watchtower y App
# Este script abre dos ventanas para ver los logs en tiempo real

Write-Host "Iniciando monitoreo de Watchtower..." -ForegroundColor Green
Write-Host ""
Write-Host "Leyenda:" -ForegroundColor Cyan
Write-Host "  - Watchtower revisara Docker Hub cada 5 minutos" -ForegroundColor Yellow
Write-Host "  - Cuando detecte cambios veras:" -ForegroundColor Yellow
Write-Host "    + Found new ... image" -ForegroundColor Green
Write-Host "    + Stopping /museo-dinosaurios-app" -ForegroundColor Yellow
Write-Host "    + Starting /museo-dinosaurios-app" -ForegroundColor Green
Write-Host ""
Write-Host "Proxima revision en menos de 5 minutos..." -ForegroundColor Magenta
Write-Host "Presiona Ctrl+C para detener el monitoreo" -ForegroundColor Gray
Write-Host ""
Write-Host "===================================================" -ForegroundColor Blue
Write-Host ""

# Mostrar logs en tiempo real
docker logs -f watchtower

