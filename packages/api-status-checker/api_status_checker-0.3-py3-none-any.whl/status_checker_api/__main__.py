from . import check_status

def main():
    url = input('Ingrese la URL de la API: ')
    status = check_status(url)
    print(f'El status de la API es: {status}')

if __name__ == "__main__":
    main()
