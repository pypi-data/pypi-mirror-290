import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, smtp_server, username, password, smtp_port=None):
        """
        Inicializa o objeto EmailSender.

        :param smtp_server: Endereço do servidor SMTP
        :param smtp_port: Porta do servidor SMTP (opcional)
        :param username: Nome de usuário para autenticação
        :param password: Senha para autenticação
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, from_addr, subject, body='VJMail Rocks!', to_addr='vjbots2023@gmail.com'):
        """
        Envia um e-mail.

        :param from_addr: Endereço de e-mail do remetente
        :param subject: Assunto do e-mail
        :param body: Corpo do e-mail (opcional)
        :param to_addr: Endereço de e-mail do destinatário (caso seja um alerta, é opcional)
        """
        try:
            # Configuração da mensagem
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = subject

            # Adicionando o corpo da mensagem
            msg.attach(MIMEText(body, 'plain'))

            # Configuração do servidor SMTP
            if self.smtp_port:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server)

            server.starttls()  # Iniciando a conexão TLS (caso necessário)
            server.login(self.username, self.password)

            # Enviando o e-mail
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)

            # Encerrando a conexão
            server.quit()

            print("E-mail enviado com sucesso!")

        except Exception as e:
            print(f"Falha ao enviar e-mail: {str(e)}")
