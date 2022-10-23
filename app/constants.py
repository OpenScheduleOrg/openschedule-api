class ResponseMessages:
    UNEXPECTED_ERROR = "Unexpected error ocurred"
    ENTITY_NOT_FOUND = "{} not found"


class ValidationMessages:
    PARAMETERS_USELESS = "Request have useless parameters"
    REQUIRED_FIELD = "The field {} is required"

    INVALID_CPF = "The field {} is not a valid cpf"
    INVALID_CNPJ = "The field {} is not a valid cnpj"

    INVALID_PHONE = "The field is not a email"
    INVALID_EMAIL = "The field {} is not a valid phone number"
    INVALID_DATE = "The field {} is not a date"

    CPF_REGISTERED = "The CPF has already been registered"
    CNPJ_REGISTERED = "The CNPJ has already been registered"
    PHONE_REGISTERED = "The phone number has already been registered"
    USERNAME_REGISTERED = "The username has already been registered"
    EMAIL_REGISTERED = "The email has already been registered"

    NO_ENTITY_RELATIONSHIP = "The {} referenced by {} not exists"

    LEAST_CHARACTERS = "The field {} must have at least {} characters"
    MOST_CHARACTERS = "The field {} must have at most {} characters"

    NOT_A_NUMBER = "The value in payload is not a number"
    NOT_IN_ENUM = "{} is not a valid {}"
