from fastapi_mail import ConnectionConfig

CONFIG = ConnectionConfig(
    MAIL_USERNAME="d97a5498-c6ec-4e46-a5c9-df1ace1a82c6",
    MAIL_PASSWORD="f02c08df-cb92-46ed-a51f-f2bcc879aafe",
    MAIL_PORT=9025,
    MAIL_SERVER="app.debugmail.io",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="addo@test.com",
)
