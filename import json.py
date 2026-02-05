import json
from datetime import datetime, timedelta

class PlanificadorLaboratorio:
    def __init__(self, archivo_datos="datos_laboratorio.json"):
        # Nombre del archivo donde se guardará todo el estado del sistema
        self.archivo_datos = archivo_datos
        # Diccionario para almacenar los recursos (ID: {nombre, tipo})
        self.recursos = {}
        # Lista para almacenar los objetos de tipo evento
        self.eventos = []
        # Carga inicial de datos desde el archivo persistente
        self.cargar_datos()

    def cargar_datos(self):
        """Carga la configuración y eventos desde un archivo JSON."""
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.recursos = datos.get("recursos", {})
                # Convertimos los strings de fecha del JSON de nuevo a objetos datetime de Python
                self.eventos = datos.get("eventos", [])
                for e in self.eventos:
                    e['inicio'] = datetime.fromisoformat(e['inicio'])
                    e['fin'] = datetime.fromisoformat(e['fin'])
        except FileNotFoundError:
            # Si el archivo no existe, creamos un inventario por defecto para el laboratorio
            self.recursos = {
                "SEC01": {"nombre": "Secuenciador Genómico", "tipo": "maquinaria"},
                "BIO01": {"nombre": "Analista Bioinformático", "tipo": "personal"},
                "CRIO1": {"nombre": "Criostato", "tipo": "frio"},
                "INC01": {"nombre": "Incubador de Cultivos", "tipo": "calor"},
                "MIC01": {"nombre": "Microscopio Electrónico", "tipo": "optico"}
            }
            self.guardar_datos()

    def guardar_datos(self):
        """Guarda el estado actual en el archivo JSON para persistencia."""
        eventos_serializables = []
        for e in self.eventos:
            # Copiamos el evento pero convirtiendo las fechas a string ISO para el JSON
            e_copy = e.copy()
            e_copy['inicio'] = e['inicio'].isoformat()
            e_copy['fin'] = e['fin'].isoformat()
            eventos_serializables.append(e_copy)
        
        datos = {"recursos": self.recursos, "eventos": eventos_serializables}
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def validar_restricciones(self, ids_recursos):
        """Verifica las reglas de Co-requisito y Exclusión Mutua."""
        tipos = [self.recursos[rid]["tipo"] for rid in ids_recursos if rid in self.recursos]
        
        # REGLA 1: Co-requisito (Maquinaria de secuenciación requiere Personal)
        if "maquinaria" in tipos and "personal" not in tipos:
            return False, "ERROR: El Secuenciador requiere un Analista Bioinformático asignado."
            
        # REGLA 2: Exclusión Mutua (No mezclar frío y calor por seguridad)
        if "frio" in tipos and "calor" in tipos:
            return False, "ERROR: No se puede usar el Criostato y el Incubador en el mismo experimento."
            
        return True, ""

    def hay_solapamiento(self, inicio1, fin1, inicio2, fin2):
        """Comprueba si dos intervalos de tiempo chocan entre sí."""
        return inicio1 < fin2 and inicio2 < fin1

    def planificar_evento(self, nombre, inicio_str, fin_str, ids_recursos):
        """Intenta agregar un nuevo experimento validando conflictos."""
        try:
            inicio = datetime.fromisoformat(inicio_str)
            fin = datetime.fromisoformat(fin_str)
            if inicio >= fin: return "Error: La fecha de inicio debe ser anterior a la de fin."
        except ValueError:
            return "Error: Formato de fecha incorrecto (Use YYYY-MM-DD HH:MM)."

        # 1. Validar Restricciones de Dominio
        valido, mensaje = self.validar_restricciones(ids_recursos)
        if not valido: return mensaje

        # 2. Validar Conflictos de Recursos (solapamiento de tiempo)
        for evento_existente in self.eventos:
            if self.hay_solapamiento(inicio, fin, evento_existente['inicio'], evento_existente['fin']):
                # Si hay choque de tiempo, revisamos si comparten algún recurso
                recursos_en_conflicto = set(ids_recursos) & set(evento_existente['recursos'])
                if recursos_en_conflicto:
                    return f"Error: Recursos {recursos_en_conflicto} ya están ocupados por el evento '{evento_existente['nombre']}'."

        # Si todo es correcto, guardamos el evento
        self.eventos.append({
            "nombre": nombre, "inicio": inicio, "fin": fin, "recursos": ids_recursos
        })
        self.guardar_datos()
        return "¡Experimento planificado con éxito!"

    def buscar_hueco(self, duracion_horas, ids_recursos):
        """Busca el primer espacio libre para un experimento."""
        ahora = datetime.now().replace(minute=0, second=0, microsecond=0)
        duracion = timedelta(hours=duracion_horas)
        
        # Buscamos en los próximos 7 días, hora por hora
        for i in range(24 * 7):
            candidato_inicio = ahora + timedelta(hours=i)
            candidato_fin = candidato_inicio + duracion
            
            conflicto = False
            # Verificamos si algún evento existente choca con este hueco
            for e in self.eventos:
                if self.hay_solapamiento(candidato_inicio, candidato_fin, e['inicio'], e['fin']):
                    if set(ids_recursos) & set(e['recursos']):
                        conflicto = True
                        break
            
            if not conflicto:
                # Si no hay choque, verificamos que cumpla las reglas del laboratorio
                valido, _ = self.validar_restricciones(ids_recursos)
                if valido:
                    return candidato_inicio.strftime("%Y-%m-%d %H:%M")
        
        return "No se encontró ningún hueco disponible en la próxima semana."

    def sugerir_huecos(self, duracion_horas, ids_recursos, max_sugerencias=5):
        """
        Busca múltiples espacios libres para un experimento.
        Retorna una lista con los próximos intervalos disponibles.
        """
        ahora = datetime.now().replace(minute=0, second=0, microsecond=0)
        duracion = timedelta(hours=duracion_horas)
        sugerencias = []

        # Recorremos las próximas 7 días, hora por hora
        for i in range(24 * 7):
            candidato_inicio = ahora + timedelta(hours=i)
            candidato_fin = candidato_inicio + duracion

            conflicto = False
            # Verificamos si algún evento existente choca con este hueco
            for e in self.eventos:
                if self.hay_solapamiento(candidato_inicio, candidato_fin, e['inicio'], e['fin']):
                    if set(ids_recursos) & set(e['recursos']):
                        conflicto = True
                        break

            if not conflicto:
                # Validamos reglas del laboratorio
                valido, _ = self.validar_restricciones(ids_recursos)
                if valido:
                    sugerencias.append(
                        f"{candidato_inicio.strftime('%Y-%m-%d %H:%M')} - {candidato_fin.strftime('%Y-%m-%d %H:%M')}"
                    )
                    if len(sugerencias) >= max_sugerencias:
                        break

        if not sugerencias:
            return ["No se encontraron huecos disponibles en la próxima semana."]
        
        return sugerencias

# --- INTERFAZ DE USUARIO (CLI) ---
def menu():
    lab = PlanificadorLaboratorio()
    while True:
        print("\n--- BIO-GENIX: GESTIÓN DE LABORATORIO ---")
        print("1. Listar Experimentos")
        print("2. Planificar Nuevo Experimento")
        print("3. Buscar Hueco Disponible")
        print("4. Eliminar Experimento")
        print("5. Salir")
        print("6. Sugerir Intervalos Disponibles")  # Nueva opción
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\nLISTADO DE EVENTOS:")
            for i, e in enumerate(lab.eventos):
                print(f"{i}. {e['nombre']} | {e['inicio']} - {e['fin']} | Recursos: {e['recursos']}")
        
        elif opcion == "2":
            nom = input("Nombre del experimento: ")
            ini = input("Inicio (YYYY-MM-DD HH:MM): ")
            fin = input("Fin (YYYY-MM-DD HH:MM): ")
            print(f"Recursos disponibles: {list(lab.recursos.keys())}")
            recs = input("IDs de recursos (separados por coma): ").replace(" ", "").split(",")
            print(lab.planificar_evento(nom, ini, fin, recs))
    
        elif opcion == "3":
                dur = float(input("Duración del experimento (en horas): "))
                recs = input("IDs de recursos necesarios (separados por coma): ").replace(" ", "").split(",")
                print(f"Sugerencia de horario: {lab.buscar_hueco(dur, recs)}")
                

        elif opcion == "4":
            idx = int(input("Número de experimento a eliminar: "))
            if 0 <= idx < len(lab.eventos):
                lab.eventos.pop(idx)
                lab.guardar_datos()
                print("Evento eliminado.")

        elif opcion == "5":
            break

if __name__ == "__main__":
    menu()
