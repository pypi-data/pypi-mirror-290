class ConfigError(ValueError):
    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        if self.error_code:
            return f"[Error {self.error_code}]: {self.message}"
        return self.message
