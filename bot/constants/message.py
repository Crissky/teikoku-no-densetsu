# GENERAL
FAIL_UPDATE_NOT_ARGS_FORMAT = (
    "⚠️ Este comando requer *argumentos* para funcionar.\n\n"
    "*Como usar:*\n"
    "Informe o atributo e o novo valor separados por `=`.\n"
    "Exemplo: `atributo`=`valor`\n\n"
    "*Múltiplos atributos:*\n"
    "Separe cada par por espaço.\n"
    "Exemplo: `arg_1`=`true` `arg_2`=`123` `arg_3`=`abc`\n\n"
    "⚠️ Argumentos fora desse formato, atributos não alteráveis ou valores "
    "inválidos serão ignorados.\n\n"
    "*Atributos alteráveis*:\n"
    "{attrs}"
)

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
NO_CHANGE_IN_PLAYER = (
    "*Nenhuma alteração* foi feita no jogador. "
    "Nenhum *atributo* ou *valor* válido foi informado."
)

# GROUP
GROUP_ALREADY_REGISTERED_FORMAT = (
    "*Grupo* com *CHAT ID*: *{id}*, já está cadastrado."
)
GROUP_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Grupo *{name}* cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
NO_CHANGE_IN_GROUP = (
    "*Nenhuma alteração* foi feita no grupo. "
    "Nenhum *atributo* ou *valor* válido foi informado."
)


# WORLD
WORLD_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Mundo *{name}* cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
WORLD_ARGS_TYPE_ERROR = (
    "⚠️ *TIPO DE ARGUMENTO INCORRETO*.\n\n"
    "Os argumentos precisam ser *DOIS NÚMEROS* separados por um espaço, "
    "representando as coordenadas X e Y do mundo.\n\n"
    "Exemplo: `/{command} 10 -20`\n\n"
)
