class TropaError(Exception):
    def __init__(self, mensaje, codigo):
        self.mensaje = mensaje
        self.codigo = codigo