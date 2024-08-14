def log(message):
    with open("logs/framework.log", "a") as log_file:
        log_file.write(message + "\n")