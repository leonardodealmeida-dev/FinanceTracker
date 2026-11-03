from PySide6.QtCore import QLocale

system_language = QLocale.system().name().lower()
LANGUAGE = "pt_BR" if system_language.startswith("pt_br") else "en_US"

TRANSLATIONS = {
    "pt_BR": {
        "brand": "FinanceTracker",
        "tagline": "Seu dinheiro, organizado.",
        "login_heading": "Bem-vindo de volta",
        "signup_heading": "Crie sua conta",
        "email_placeholder": "Seu e-mail",
        "password_placeholder": "Sua senha",
        "login": "Entrar",
        "signup": "Cadastrar",
        "create_account": "Não tem uma conta? Criar conta",
        "have_account": "Já tem uma conta? Entrar",
        "fill_fields": "Preencha o e-mail e a senha.",
        "invalid_email": "Digite um endereço de e-mail válido.",
        "password_short": "Use uma senha com pelo menos 8 caracteres.",
        "connecting": "Conectando ao Supabase...",
        "wait": "Aguarde...",
        "check_email_title": "Confira seu e-mail",
        "check_email_message": (
            "Cadastro enviado! Se a confirmação por e-mail estiver "
            "habilitada, confirme sua conta antes de entrar."
        ),
        "login_failed": "Login não concluído. Verifique sua conta.",
        "operation_failed": (
            "Não foi possível concluir a operação. "
            "Confira os dados e tente novamente."
        ),
        "dashboard_title": "FinanceTracker — Painel",
        "welcome": "Bem-vindo ao FinanceTracker!",
        "connected_as": "Conectado como: {}",
        "dashboard_message": (
            "Login concluído! O painel financeiro será implementado "
            "na próxima etapa."
        ),
        "config_error": (
            "O aplicativo não está configurado para se conectar ao "
            "servidor."
        ),
        "forgot_password": "Esqueceu a senha?",
        "reset_title": "Redefinir senha",
        "reset_intro": "Digite seu e-mail para receber um código.",
        "reset_send_code": "Enviar código",
        "reset_code_sent": (
            "Se existir uma conta com esse e-mail, enviamos um código. "
            "Digite-o abaixo com sua nova senha."
        ),
        "reset_code_placeholder": "Código recebido por e-mail",
        "reset_new_password": "Nova senha (mín. 8 caracteres)",
        "reset_confirm": "Redefinir senha",
        "reset_failed": "Código inválido ou expirado.",
        "reset_send_failed": (
            "Não foi possível enviar o código. Tente novamente em "
            "alguns minutos."
        ),
        "reset_done": "Senha atualizada! Agora você pode entrar.",
        "cancel": "Cancelar",
    },
    "en_US": {
        "brand": "FinanceTracker",
        "tagline": "Your money, organized.",
        "login_heading": "Welcome back",
        "signup_heading": "Create your account",
        "email_placeholder": "Your email",
        "password_placeholder": "Your password",
        "login": "Sign in",
        "signup": "Create account",
        "create_account": "Don't have an account? Sign up",
        "have_account": "Already have an account? Sign in",
        "fill_fields": "Enter your email and password.",
        "invalid_email": "Enter a valid email address.",
        "password_short": "Use a password with at least 8 characters.",
        "connecting": "Connecting to Supabase...",
        "wait": "Please wait...",
        "check_email_title": "Check your email",
        "check_email_message": (
            "Registration submitted! If email confirmation is enabled, "
            "confirm your account before signing in."
        ),
        "login_failed": "Login incomplete. Check your account.",
        "operation_failed": (
            "The operation could not be completed. "
            "Check your details and try again."
        ),
        "dashboard_title": "FinanceTracker — Dashboard",
        "welcome": "Welcome to FinanceTracker!",
        "connected_as": "Signed in as: {}",
        "dashboard_message": (
            "Login successful! The financial dashboard will be "
            "implemented in the next step."
        ),
        "config_error": (
            "The app isn't configured to connect to the server."
        ),
        "forgot_password": "Forgot password?",
        "reset_title": "Reset password",
        "reset_intro": "Enter your email to receive a code.",
        "reset_send_code": "Send code",
        "reset_code_sent": (
            "If an account exists for that email, we sent a code. "
            "Enter it below with your new password."
        ),
        "reset_code_placeholder": "Code from the email",
        "reset_new_password": "New password (min. 8 characters)",
        "reset_confirm": "Reset password",
        "reset_failed": "Invalid or expired code.",
        "reset_send_failed": (
            "Couldn't send the code. Please try again in a few minutes."
        ),
        "reset_done": "Password updated! You can now sign in.",
        "cancel": "Cancel",
    },
}


def tr(key):
    return TRANSLATIONS[LANGUAGE].get(
        key, TRANSLATIONS["en_US"].get(key, key)
    )
