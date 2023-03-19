def start_bot_message(user_full_name):
    return f'Привет, {user_full_name}! Я бот ProjectE.\n\nProjectE – это чат-бот\n\nБот может:\n├ установить напоминание\n└добавить новую задачу'


new_task_message='Введите название новой задачи'


def cool_view(sp):
    new_sp='\n\n'
    for i in range(1,len(sp)):
        new_sp+='📜'+str(sp[i][0])+'\n\n'
    return new_sp
