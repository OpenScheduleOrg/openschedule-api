class ResponseMessages:
    UNEXPECTED_ERROR = "unexpected error ocurred"
    ENTITY_NOT_FOUND = "{} not found"

    ONLY_ADMIN = "only admin can performs this operation"
    NOT_AUHORIZED_ACCESS = "not authorized to access this data"
    NOT_AUHORIZED_OPERATION = "not authorized to perform this operation"


class ValidationMessages:
    PARAMETERS_USELESS = "Request have useless parameters"
    REQUIRED_FIELD = "field {} is required"

    INVALID_CPF = "field {} is not a valid cpf"
    INVALID_CNPJ = "field {} is not a valid cnpj"

    INVALID_PHONE = "field is not a email"
    INVALID_EMAIL = "field {} is not a valid phone number"
    INVALID_DATE = "field {} is not a date"

    CPF_REGISTERED = "CPF has already been registered"
    REGISTRATION_REGISTERED = "registration has already been registered"
    CNPJ_REGISTERED = "CNPJ has already been registered"
    PHONE_REGISTERED = "phone number has already been registered"
    USERNAME_REGISTERED = "username has already been registered"
    EMAIL_REGISTERED = "email has already been registered"

    NO_ENTITY_RELATIONSHIP = "{} referenced by {} not exists"

    LEAST_CHARACTERS = "field {} must have at least {} characters"
    MOST_CHARACTERS = "field {} must have at most {} characters"

    NOT_A_NUMBER = "field {} is not a number"
    OUT_OF_RANGE = "out of range accepted between {} and {}"
    NOT_IN_ENUM = "{} is not a valid {}"
