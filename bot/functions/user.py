from telegram import Update, User


def get_username(update: Update = None, user: User = None) -> str:
    """Obtém o nome de usuário do Telegram do jogador.
    Retorna uma string vazia caso usuário não tenha um @username.
    """

    if not update and not user:
        raise ValueError("Nenhum update ou user válido foi passado.")

    if update:
        user = update.effective_user

    user_name = user.name
    if not user_name.startswith("@"):
        user_name = ""

    return user_name
