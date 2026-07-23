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
PLAYER_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Olá {name}!\n"
    "Você foi cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
PLAYER_ALREADY_REGISTERED_ERROR = (
    "⚠️ *PLAYER JÁ CADASTRADO*.\n\n"
    "*Player* com *USER ID*: *{id}* já foi cadastrado."
)
NO_CHANGE_IN_PLAYER_MSG = (
    "*Nenhuma alteração* foi feita no jogador. "
    "Nenhum *atributo* ou *valor* válido foi informado."
)

# GROUP
GROUP_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Grupo *{name}* cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
GROUP_ALREADY_REGISTERED_ERROR = (
    "⚠️ *GRUPO JÁ CADASTRADO*.\n\n"
    "*Grupo* com *CHAT ID*: *{id}*, já foi cadastrado."
)
NO_CHANGE_IN_GROUP_MSG = (
    "*Nenhuma alteração* foi feita no grupo. "
    "Nenhum *atributo* ou *valor* válido foi informado."
)

# WORLD
WORLD_SUCCESSFULLY_REGISTERED_FORMAT = (
    "Mundo *{name}* cadastrado com sucesso!\n\n"
    "{subsection}"
    "{telegram_text}"
)
WORLD_ALREADY_REGISTERED_ERROR = (
    "⚠️ *MUNDO JÁ CADASTRADO*.\n\n"
    'O mundo com o nome "{world_name}" já foi cadastrado.'
)
WORLD_PRIVATE_CHAT_ERROR = (
    "⚠️ *CHAT PRIVADO*.\n\n"
    "Não é possível criar um mundo em um chat privado. "
    "Use o comando /{command} no grupo que deseja cadastrar."
)
WORLD_ARGS_TYPE_ERROR = (
    "⚠️ *TIPO DE ARGUMENTO INCORRETO*.\n\n"
    "Os argumentos precisam ser *DOIS NÚMEROS* separados por um espaço, "
    "representando as coordenadas X e Y do mundo.\n\n"
    "Exemplo: `/{command} 10 -20`"
)
WORLD_ARGS_COUNT_ERROR = (
    "⚠️ *NÚMERO DE ARGUMENTOS INCORRETO*.\n\n"
    "É preciso informar *NENHUM* ou *DOIS* argumentos separados por "
    "um espaço, representando as coordenadas X e Y do mundo.\n\n"
    "Exemplo: `/{command} 10 -20`"
)
WORLD_NOT_FOUND_ERROR = (
    "⚠️ *MUNDO NÃO ENCONTRADO*.\n\n"
    'Não há nenhum mundo cadastrado para o grupo "{chat_id}". '
    "Use o comando /{command} para cadastrar um novo mundo vinculado a "
    "esse chat."
)
WORLD_UNKNOWN_ERROR = (
    "⚠️ *ERRO NÃO IDENTIICADO AO CARREGAR O MUNDO*.\n\n"
    "Chat ID: {chat_id}\n"
    "ARGS: {args}\n"
    "MUNDO: {wolrd}"
)

# CITY
CITY_NO_ARGS_ERROR = (
    "⚠️ *NÃO FOI INFORMADO ARGUMENTO*.\n\n"
    "Para adicionar uma cidade, utilize o comando /{command} "
    "seguido do nome desejado.\n\n"
    "📝 Exemplo de uso:\n"
    "/{command} Recife Medieval"
)
