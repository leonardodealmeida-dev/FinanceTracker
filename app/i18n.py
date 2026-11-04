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
        "err_rate_limit": (
            "Muitas tentativas ou e-mails enviados. Aguarde um pouco "
            "e tente novamente."
        ),
        "err_email_not_authorized": (
            "Não foi possível enviar o e-mail de confirmação para este "
            "endereço agora. Tente novamente mais tarde."
        ),
        "err_user_exists": (
            "Já existe uma conta com este e-mail. Tente entrar."
        ),
        "err_weak_password": (
            "Senha muito fraca. Use uma senha mais longa e difícil de "
            "adivinhar."
        ),
        "err_signup_disabled": (
            "Novos cadastros estão temporariamente indisponíveis."
        ),
        "err_email_not_confirmed": (
            "Confirme seu e-mail pelo link que enviamos antes de entrar."
        ),
        "err_network": (
            "Sem conexão com o servidor. Verifique sua internet e "
            "tente novamente."
        ),
        "err_server_config": (
            "O aplicativo não conseguiu se autenticar no servidor. "
            "Atualize para a versão mais recente."
        ),
        "err_same_password": (
            "A nova senha precisa ser diferente da anterior."
        ),
        "reset_update_failed": (
            "Código aceito, mas não foi possível definir a nova senha. "
            "Tente outra senha."
        ),
        "err_timeout": (
            "O servidor demorou demais para responder (geralmente o envio "
            "do e-mail de confirmação). Aguarde alguns minutos e tente "
            "novamente."
        ),
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
        "err_rate_limit": (
            "Too many attempts or emails sent. Please wait a bit and "
            "try again."
        ),
        "err_email_not_authorized": (
            "We couldn't send the confirmation email to this address "
            "right now. Please try again later."
        ),
        "err_user_exists": (
            "An account with this email already exists. Try signing in."
        ),
        "err_weak_password": (
            "That password is too weak. Use a longer, harder-to-guess "
            "password."
        ),
        "err_signup_disabled": "New sign-ups are temporarily unavailable.",
        "err_email_not_confirmed": (
            "Please confirm your email using the link we sent before "
            "signing in."
        ),
        "err_network": (
            "Can't reach the server. Check your internet connection and "
            "try again."
        ),
        "err_server_config": (
            "The app couldn't authenticate with the server. Please "
            "update to the latest version."
        ),
        "err_same_password": (
            "The new password must be different from the old one."
        ),
        "reset_update_failed": (
            "Code accepted, but the new password couldn't be set. "
            "Try a different password."
        ),
        "err_timeout": (
            "The server took too long to respond (usually sending the "
            "confirmation email). Please wait a few minutes and try again."
        ),
    },
}


def tr(key):
    return TRANSLATIONS[LANGUAGE].get(
        key, TRANSLATIONS["en_US"].get(key, key)
    )
