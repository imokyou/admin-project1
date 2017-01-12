# coding=utf-8
resetpwd_template = {
    'version': 1.0,
    'subject': '{title}',
    'to': [],
    'account':
    """
    <div>
    您的账号为: {username}
    </div>
    """,
    'password':
    """
    <div>
    您的账号为: {username}
    请点击以下链接重置该账号的密码: <a href="{reset_url}">重置密码>>></a>
    </div>
    """
}