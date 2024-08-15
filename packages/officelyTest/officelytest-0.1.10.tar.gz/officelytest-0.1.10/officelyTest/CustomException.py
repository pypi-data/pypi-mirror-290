

class CustomExceptionUser(Exception):
    pass

class RootValidatorException(CustomExceptionUser):
    pass

class MissingEnvKeys(CustomExceptionUser):
    pass