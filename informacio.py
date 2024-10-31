import paramiko
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Configuración inicial
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Interfaz para obtener datos de conexión SSH
def get_ssh_connection():
    ip_address = simpledialog.askstring("IP del Cliente", "Ingresa la IP del cliente:")
    username = simpledialog.askstring("Usuario", "Ingresa el nombre de usuario:")
    password = simpledialog.askstring("Contraseña", "Ingresa la contraseña:", show="*")

    # Conexión SSH usando Paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(ip_address, username=username, password=password)
        sftp_client = ssh_client.open_sftp()
        return ssh_client, sftp_client
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar: {e}")
        return None, None

# Función para enviar archivos
def send_file():
    ssh_client, sftp_client = get_ssh_connection()
    if ssh_client and sftp_client:
        filename = filedialog.askopenfilename()
        if filename:
            remote_filename = filename.split('/')[-1]
            sftp_client.put(filename, remote_filename)
            messagebox.showinfo("Archivo Enviado", f"Archivo {remote_filename} enviado exitosamente.")
        sftp_client.close()
        ssh_client.close()

# Configuración de la interfaz gráfica del servidor
root = tk.Tk()
root.title("Servidor SSH de Transferencia de Archivos")
root.geometry("300x200")

send_button = tk.Button(root, text="Enviar Archivo al Cliente", command=send_file)
send_button.pack(pady=20)

root.mainloop()
