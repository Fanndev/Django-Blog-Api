class StatusCode:
    INTERNAL_SERVER_ERROR = 500
    CONFLICT = 409
    NOT_FOUND = 404
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    OK = 200
    CREATED = 201
    UNPROCESSABLE_ENTITY = 422


class ResponseMessage:
    LOADED = "Data loaded successfully"
    ADDED = "Data added successfully"
    UPDATED = "Data updated successfully"
    REMOVED = "Data removed successfully"
    RESTORED = "Data restored successfully"
    FAIL_LOADED = "Failed to load data"
    FAIL_ADDED = "Failed to add data"
    FAIL_UPDATED = "Failed to update data"
    FAIL_REMOVED = "Failed to remove data"
    FAIL_RESTORED = "Failed to restore data"
    FAIL_REGISTERED = "Failed to register data"
    USER_NOT_FOUND = "User not found"
    EMAIL_ALREADY_EXIST = "Email already registered"
    SUCCESS = "Successfully"
    SUCCESS_REGISTERED = "Successfully registered."
    LOGIN_SUCCESS = "You have successfully logged in."
    LOGIN_FAILED = "Invalid credentials."
    NOT_FOUND = "Data not found"
    UNAUTHORIZED = "Unauthorized"
    NOT_REQUIRED = "Email and Password not found"
    EMAIL_NOT_FOUND = "Email not found"
    WRONG_PASSWORD = "Wrong password"