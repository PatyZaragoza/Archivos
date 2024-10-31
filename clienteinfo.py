import paramiko
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Configuración inicial
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Interfaz para obtener datos de conexión SSH
def get_ssh_connection():
    ip_address = simpledialog.askstring("IP del Servidor", "Ingresa la IP del servidor:")
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

# Función para recibir archivos
def receive_file():
    ssh_client, sftp_client = get_ssh_connection()
    if ssh_client and sftp_client:
        remote_filename = filedialog.asksaveasfilename(title="Guardar archivo como")
        if remote_filename:
            local_filename = remote_filename.split('/')[-1]
            sftp_client.get(remote_filename, local_filename)
            messagebox.showinfo("Archivo Recibido", f"Archivo {local_filename} recibido exitosamente.")
        sftp_client.close()
        ssh_client.close()

# Configuración de la interfaz gráfica del cliente
root = tk.Tk()
root.title("Cliente SSH de Transferencia de Archivos")
root.geometry("300x200")

receive_button = tk.Button(root, text="Recibir Archivo del Servidor", command=receive_file)
receive_button.pack(pady=20)

root.mainloop()
