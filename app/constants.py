class ResponseMessages:
    UNEXPECTED_ERROR = "Unexpected error ocurred"
    PATIENT_NO_FOUND = "Patient not found"
    CLINIC_NO_FOUND = "Clinic not found"


class ValidationMessages:
    PARAMETERS_USELESS = "Request have useless parameters"
    REQUIRED_FIELD = "The field {} is required"

    INVALID_CPF = "The field {} is not a valid cpf"
    INVALID_CNPJ = "The field {} is not a valid cnpj"

    INVALID_PHONE = "The field {} is not a valid phone number"
    INVALID_DATE = "The field {} is not a date"
    INVALID_LATITUDE = "Latitude must be a decimal between -90 and 90"
    INVALIDE_LONGITUDE = "Longitude must be a value between -180 and 180"

    CPF_REGISTERED = "The CPF has already been registered"
    CNPJ_REGISTERED = "The CNPJ has already been registered"
    PHONE_REGISTERED = "The phone number has already been registered"

    LEAST_CHARACTERS = "The field {} must have at least {} characters"
    MOST_CHARACTERS = "The field {} must have at most {} characters"

    NOT_A_NUMBER = "The value in payload is not a number"
    NOT_IN_ENUM = "{} is not a valid {}"
