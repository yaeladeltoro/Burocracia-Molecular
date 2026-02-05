# 🧬 BIO-GENIX: Planificador de Laboratorio

## 📌 Descripción del Proyecto
**BIO-GENIX** es un sistema de gestión y planificación de experimentos en un laboratorio, desarrollado en **Python**.  
El objetivo principal es administrar de manera eficiente los recursos disponibles (equipos especializados y personal técnico), garantizando que se cumplan las **reglas de seguridad** y los **requisitos operativos** del entorno científico.

Este proyecto integra conceptos de:
- **Programación orientada a objetos (POO)**
- **Manejo de fechas y tiempos** con la librería estándar `datetime`
- **Persistencia de datos** mediante archivos en formato **JSON**
- **Interacción con el usuario** a través de una interfaz de línea de comandos (**CLI**)

---

## ⚙️ Funcionalidades Principales
El sistema ofrece las siguientes capacidades:

- **Gestión de recursos**: Inventario inicial de equipos y personal del laboratorio.
- **Planificación de experimentos**:
  - Validación de reglas de seguridad y co-requisitos.
  - Prevención de solapamientos de tiempo y recursos.
- **Búsqueda de huecos disponibles**:
  - Sugerencia automática de horarios libres en los próximos 7 días.
- **Persistencia de datos**:
  - Todos los eventos y recursos se guardan en un archivo JSON (`datos_laboratorio.json`).
- **Interfaz CLI**:
  - Menú interactivo para listar, crear, buscar y eliminar experimentos.

---

## 🧪 Reglas de Negocio Implementadas
El sistema valida automáticamente las siguientes restricciones:

1. **Co-requisito**  
   - El **Secuenciador Genómico** (maquinaria) requiere que esté asignado un **Analista Bioinformático** (personal).

2. **Exclusión Mutua**  
   - No se pueden usar simultáneamente recursos de tipo **frío** (Criostato) y **calor** (Incubador), por motivos de seguridad.

3. **Prevención de solapamientos**  
   - El sistema detecta conflictos de agenda cuando dos experimentos comparten recursos en intervalos de tiempo que se superponen.

---

## 📂 Estructura del Proyecto
├── datos_laboratorio.json   # Archivo de persistencia (se genera automáticamente)
├── planificador.py           # Código principal con la clase y la interfaz CLI
└── README.md                 # Documentación del proyecto


---

## ▶️ Uso del Programa
# 1. Ejecuta el programa:
    main.py
    
# 2. Interactúa con el menú:

1. Listar Experimentos → Muestra todos los eventos planificados.

2. Planificar Nuevo Experimento → Permite crear un nuevo evento con nombre, fechas y recursos.

3. Buscar Hueco Disponible → Sugiere el primer horario libre para los recursos seleccionados.

4. Eliminar Experimento → Borra un evento existente.

5. Salir → Finaliza el programa.


---

## 📊 Ejemplo de Uso
# Planificar un nuevo experimento:

Nombre del experimento: Secuenciación ADN
Inicio (YYYY-MM-DD HH:MM): 2026-02-05 09:00
Fin (YYYY-MM-DD HH:MM): 2026-02-05 12:00
Recursos disponibles: ['SEC01', 'BIO01', 'CRIO1', 'INC01', 'MIC01']
IDs de recursos (separados por coma): SEC01,BIO01
¡Experimento planificado con éxito!

---

## Buscar hueco disponible:

Duración del experimento (en horas): 3
IDs de recursos necesarios (separados por coma): MIC01
Sugerencia de horario: 2026-02-03 14:00


---

## 🛠️ Tecnologías Utilizadas
# Lenguaje: Python 3.x

1. Módulos estándar:

2. json → Persistencia de datos.

3. datetime → Manejo de fechas y horas.

4. timedelta → Cálculo de intervalos de tiempo.


