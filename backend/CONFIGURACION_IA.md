# Configuración de IA para Validación de Informes

El sistema soporta **3 modos** de validación con IA:

## 📋 Opciones Disponibles

### 1️⃣ xAI Grok (Premium - Requiere Créditos)
```bash
# En backend/.env
GROQ_API_KEY=xai-tu-api-key-aqui
```

**Características:**
- ✅ Modelo más avanzado
- ✅ Mejores resultados
- ❌ **Requiere créditos activos**: https://console.x.ai
- ⏱️ ~20-30 segundos por informe

**Estado actual:** ⚠️ Sin créditos activados

---

### 2️⃣ Groq API (GRATIS - Recomendado)
```bash
# En backend/.env
GROQ_API_KEY=gsk_TU_KEY_AQUI
```

**Características:**
- ✅ Totalmente GRATIS
- ✅ Rápido (~5-10 segundos)
- ✅ Modelo Llama 3.3 70B
- ✅ No requiere tarjeta de crédito

**Cómo obtener tu API Key:**
1. Ve a: https://console.groq.com/keys
2. Regístrate gratis
3. Crea una API key
4. Pega en `.env` con prefijo `gsk_`

---

### 3️⃣ Modo Local (Fallback Automático)
Si las APIs fallan, el sistema usa validación local basada en reglas.

**Características:**
- ✅ Sin internet necesario
- ✅ Sin costos
- ⚠️ Resultados más básicos
- ⚡ Instantáneo

---

## 🔧 Configuración Actual

### Verificar qué API estás usando:
```bash
cd backend
grep GROQ_API_KEY .env
```

- Empieza con `xai-` → xAI Grok
- Empieza con `gsk_` → Groq API  
- No existe → Modo local

### Ver logs en tiempo real:
```bash
cd backend
tail -f server.log
```

Verás:
```
⏱️  [00s] 🤖 Usando xAI Grok API
⏱️  [00s] 🌐 Enviando request...
⏱️  [23s] ✅ 8 observaciones generadas
```

---

## 🚨 Errores Comunes

### "Model not found: grok-beta"
**Causa:** xAI cambió el nombre del modelo o sin créditos  
**Solución:** Usa Groq API (gratis) o activa créditos en https://console.x.ai

### "Sin créditos en xAI"
**Causa:** Cuenta xAI sin créditos activados  
**Solución:** 
- Opción A: Activa créditos en https://console.x.ai (de pago)
- Opción B: Usa Groq API (gratis, igualmente buena)

### "API Key inválida"
**Causa:** Key mal copiada o expirada  
**Solución:** Regenera la key en la consola de tu proveedor

### "Límite de requests excedido"
**Causa:** Demasiadas validaciones en poco tiempo  
**Solución:** Espera 1-2 minutos y reintenta

---

## 🎯 Recomendación

**Para desarrollo y uso académico:**
```bash
# Usa Groq API (gratis + rápido)
GROQ_API_KEY=gsk_TU_KEY_DE_GROQ
```

**Para producción con presupuesto:**
```bash
# Usa xAI Grok (más avanzado)
GROQ_API_KEY=xai-TU_KEY_DE_XAI
```

---

## ✅ Sistema Funcionando

**Actualmente el sistema está funcionando con:**
- ✅ Detección automática de API por prefijo de key
- ✅ Fallback a modo local si falla la API
- ✅ Timeout de 90 segundos
- ✅ Manejo de errores claro
- ✅ Progreso visual en pantalla
- ✅ Logs detallados en consola

**El sistema NUNCA falla:** siempre genera observaciones, aunque sea en modo local.
