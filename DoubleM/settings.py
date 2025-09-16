INSTALLED_APPS = [
    # default apps...
    "rest_framework",
    "accounts",
]

AUTH_USER_MODEL = "accounts.Student"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}
