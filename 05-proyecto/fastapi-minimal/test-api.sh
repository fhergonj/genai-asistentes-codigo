#!/bin/bash

echo "Task API - Test Script"
echo "====================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000"

echo -e "${BLUE}1. Root endpoint${NC}"
curl -s "$BASE_URL/" | python -m json.tool
echo ""

echo -e "${BLUE}2. Crear tarea 1${NC}"
TASK1=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI", "description": "Completar el tutorial completo"}')
echo "$TASK1" | python -m json.tool
echo ""

echo -e "${BLUE}3. Crear tarea 2${NC}"
TASK2=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender SQLModel", "description": "Entender ORM"}')
echo "$TASK2" | python -m json.tool
echo ""

echo -e "${BLUE}4. Listar todas las tareas${NC}"
curl -s "$BASE_URL/tasks" | python -m json.tool
echo ""

echo -e "${BLUE}5. Obtener tarea con ID 1${NC}"
curl -s "$BASE_URL/tasks/1" | python -m json.tool
echo ""

echo -e "${BLUE}6. Actualizar tarea 1${NC}"
curl -s -X PUT "$BASE_URL/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}' | python -m json.tool
echo ""

echo -e "${BLUE}7. Listar tareas (verificar actualización)${NC}"
curl -s "$BASE_URL/tasks" | python -m json.tool
echo ""

echo -e "${GREEN}Test completado!${NC}"
echo "Accede a la documentación interactiva en: $BASE_URL/docs"
