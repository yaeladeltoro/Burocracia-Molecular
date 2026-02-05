from planificacion import PlanificadorLaboratorio
import datetime

class Visual:
    def __init__(self):
        self.lab: PlanificadorLaboratorio =  PlanificadorLaboratorio()
        pass
# --- INTERFAZ DE USUARIO (CLI) ---
    def menu(self):
        
        while True:
            print("\n--- BIO-GENIX: GESTIÓN DE LABORATORIO ---")
            print("1. Listar Experimentos")
            print("2. Planificar Nuevo Experimento")
            print("3. Buscar Hueco Disponible")
            print("4. Eliminar Experimento")
            print("5. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                print("\nLISTADO DE EVENTOS:")
                for i, e in enumerate(self.lab.eventos):
                    print(f"{i}. {e['nombre']} | {e['inicio']} - {e['fin']} | Recursos: {e['recursos']}")
            
            elif opcion == "2":
                nom = input("Nombre del experimento: ")
                ini = input("Inicio (YYYY-MM-DD HH:MM): ")
                fin = input("Fin (YYYY-MM-DD HH:MM): ")
                print(f"Recursos disponibles: {list(self.lab.recursos.keys())}")
                recs = input("IDs de recursos (separados por coma): ").replace(" ", "").split(",")
                print(self.lab.planificar_evento(nom, ini, fin, recs))

            elif opcion == "3":
                dur = float(input("Duración del experimento (en horas): "))
                recs = input("IDs de recursos necesarios (separados por coma): ").replace(" ", "").split(",")
                print(f"Sugerencia de horario: {self.lab.buscar_hueco(dur, recs)}")

            elif opcion == "4":
                idx = int(input("Número de experimento a eliminar: "))
                if 0 <= idx < len(self.lab.eventos):
                    self.lab.eventos.pop(idx)
                    self.lab.guardar_datos()
                    print("Evento eliminado.")

            elif opcion == "5":
                break

    def eventos_del_dia(self):
        print("Eventos del dia:\n")
        alarms: list[tuple] = self.lab.eventos_del_dia()
        
        if not alarms:
            print("\t No hay eventos hoy \n")
        
        print("\t * Eventos que comienzan hoy: \n")
        for e in alarms:
            if e[0] == "hoy":
                print(f'\t\t - {e[1]}') 
        print("\t * Eventos que aun estan en proceso: \n")
        for e in alarms:
            if e[0] == "en proceso":
                print(f'\t\t - {e[1]}') 
    
    
