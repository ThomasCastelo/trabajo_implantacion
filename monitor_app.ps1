# Monitor de la Aplicacion
# Muestra los logs de la app FastAPI en tiempo real

Write-Host "Monitoreando App FastAPI..." -ForegroundColor Green
Write-Host "Cuando se actualice veras el reinicio del servidor" -ForegroundColor Cyan
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Gray
Write-Host ""
Write-Host "===================================================" -ForegroundColor Blue
Write-Host ""

# Mostrar logs en tiempo real
docker logs -f museo-dinosaurios-app

