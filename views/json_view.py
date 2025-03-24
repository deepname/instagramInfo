import json
from datetime import datetime

class JsonView:
    @staticmethod
    def save_results(results, output_file='instagram_data.json'):
        """Guarda los resultados en formato JSON."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return output_file

    @staticmethod
    def print_execution_info(start_time, output_file):
        """Muestra información sobre la ejecución del script."""
        end_time = datetime.now()
        print(f"\nDatos guardados en el archivo: {output_file}")
        print(f"Finalización del script: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        time_difference = end_time - start_time
        print(f"Tiempo total transcurrido: {time_difference}")

    @staticmethod
    def print_usage():
        """Muestra instrucciones de uso del script."""
        print("Uso: python main.py <nombre_de_usuario1> [nombre_de_usuario2 ...]\n")
        print("Ejemplos:")
        print("  Un usuario:    python main.py elonmusk")
        print("  Varios usuarios: python main.py elonmusk billgates markzuckerberg")
