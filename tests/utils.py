import socket

def get_free_ephemeral_port():
    """
    Binds a socket to port 0 to get a free ephemeral port assigned by the OS,
    then closes the socket and returns the assigned port number.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to an available port chosen by the OS
        return s.getsockname()[1]  # Get the assigned port number