def create_and_write_to_file():
    filename = "test2"
    with open(filename+".txt", 'w') as file:
        file.write("test")
    print(f"Plik {filename} został utworzony i zapisano w nim słowo 'test'.")


# Wywołanie funkcji
create_and_write_to_file()