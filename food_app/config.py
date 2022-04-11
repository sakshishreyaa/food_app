import os

SECRET_KEY = "vughifxdere4r/;;;][iuityffxccr/drdr46"
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", 5432)
database = os.getenv("POSTGRES_DB", "reservation_system")
