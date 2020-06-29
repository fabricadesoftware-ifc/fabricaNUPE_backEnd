from oauth2_provider.models import Application


def get_or_create_application(*, client_id: str, client_secret: str) -> Application:
    application, created = Application.objects.get_or_create(
        client_id=client_id,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        client_secret=client_secret,
    )

    return application
