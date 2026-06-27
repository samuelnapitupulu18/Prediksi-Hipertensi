#!/bin/bash
# health-check.sh — Jalankan setiap 5 menit via cron
# File ini digunakan untuk monitoring performa microservices 

echo "=== System Health Check ==="
echo "Time: $(date)"
echo ""

# Check Nginx
echo -n "Nginx: "
curl -sf -o /dev/null -w "%{http_code}" https://localhost/ && echo " ✅ OK" || echo " ❌ DOWN"

# Check Backend
echo -n "Backend: "
curl -sf -o /dev/null -w "%{http_code}" https://localhost/api/health && echo " ✅ OK" || echo " ❌ DOWN"

# Check ML Engine (via backend)
echo -n "ML Engine: "
docker compose exec -T backend curl -sf http://ml-engine:8000/health | grep -q "healthy" && echo " ✅ OK" || echo " ❌ DOWN"

# Check PostgreSQL
echo -n "PostgreSQL: "
docker compose exec -T postgres pg_isready -U hyper_admin > /dev/null 2>&1 && echo " ✅ OK" || echo " ❌ DOWN"

# Disk usage
echo ""
echo "Disk Usage:"
docker system df
