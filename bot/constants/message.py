# PLAYER
PLAYER_ALREADY_REGISTERED_FORMAT = (
    "*Player* com *USER ID*: *{id}* já está cadastrado."
)
PLAYER_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Olá {name}!\n"
    "Você foi cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
FAIL_UPDATE_NOT_ARGS = (
    "⚠️ Este comando requer *argumentos* para funcionar.\n\n"
    "*Como usar:*\n"
    "Informe o atributo e o novo valor separados por `=`.\n"
    "Exemplo: `atributo`=`valor`\n\n"
    "*Múltiplos atributos:*\n"
    "Separe cada par por espaço.\n"
    "Exemplo: `arg_1`=`true` `arg_2`=`123` `arg_3`=`abc`\n\n"
    "⚠️ Argumentos fora desse formato, atributos não alteráveis ou valores "
    "inválidos serão ignorados.\n\n"
)
PLAYER_ALTERABLE_ATTRIBUTES_HEADER = "*Atributos alteráveis do jogador*:\n"
NO_CHANGE_IN_PLAYER = (
    "*Nenhuma alteração* foi feito no jogador. "
    "Nenhum *atributo* ou *valor* válido foi informado."
)
