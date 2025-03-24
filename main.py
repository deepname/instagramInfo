import sys
from datetime import datetime
from controllers.instagram_controller import InstagramController
from views.json_view import JsonView

def main():
    if len(sys.argv) < 2:
        JsonView.print_usage()
        sys.exit(1)

    usernames = sys.argv[1:]
    start_time = datetime.now()
    print(f"Inicio del script: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Procesar los datos
    controller = InstagramController()
    results = controller.get_users_data(usernames)

    # Guardar y mostrar resultados
    output_file = JsonView.save_results(results)
    JsonView.print_execution_info(start_time, output_file)

if __name__ == '__main__':
    main()
