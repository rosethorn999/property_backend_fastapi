from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    frontend_host: str = "https://property-stg-next.nodm.app"
    app_name: str = "PROPERTY"
    db_connection: str
    db_connection_async: str
    secret: str

    smtp_use_tls: bool
    smtp_host: str
    smtp_host_user: str
    smtp_host_password: str
    smtp_port: int

    oauth2_google_client_id: str
    oauth2_google_client_secret: str
    oauth2_google_redirect_url: str

    oauth2_facebook_client_id: str
    oauth2_facebook_client_secret: str
    oauth2_facebook_redirect_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
