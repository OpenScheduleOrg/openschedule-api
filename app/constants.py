class ResponseMessages:
    UNEXPECTED_ERROR = "Unexpected error ocurred"
    PATIENT_NO_FOUND = "Patient not found"


class ValidationMessages:
    PARAMETERS_USELESS = "Request have useless parameters"
    REQUIRED_FIELD = "The field {} is required"
    INVALID_CPF = "The field {} is not a valid cpf"
    INVALID_PHONE = "The field {} is not a valid phone number"
    INVALID_DATE = "The field {} is not a date"
    CPF_REGISTERED = "The CPF has already been registered"
    PHONE_REGISTERED = "The phone number has already been registered"
