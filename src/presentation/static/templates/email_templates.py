

def get_reset_password_template(token: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Сброс пароля</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; text-align: center;">
            <p>Для сброса пароля нажмите на кнопку ниже:</p>
            <a href="http://127.0.0.1:8000/reset-password/confirm/?token={token}" 
            style="background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px;">
                Сбросить пароль
            </a>
        </body>
        </html>
        """

def after_reset_password_template(username: str, new_password: str) -> str:
    return f"""
       <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Сброс пароля</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; text-align: left;">
            <p>
                Вы успешно сбросили пароль<br>
                Ваш логин: <strong>{username}</strong><br>
                Ваш новый пароль: <strong>{new_password}</strong><br>
                Теперь вы можете войти на сервис с новым паролем.
            </p>
        </body>
        </html>
    """