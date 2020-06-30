from model_bakery import baker
from oauth2_provider.models import Application


def create_application() -> Application:
    return baker.make(
        Application, client_type=Application.CLIENT_CONFIDENTIAL, authorization_grant_type=Application.GRANT_PASSWORD,
    )
