import unittest
from vjmail import EmailSender

class TestEmailSender(unittest.TestCase):
    def test_send_email(self):
        sender = EmailSender('smtp.example.com', 'user@example.com', 'password')
        # Aqui você pode testar as funções da classe. Exemplo:
        # sender.send_email('from@example.com', 'Test Subject', 'Test Body')
        # Apenas verificar se o objeto foi criado corretamente:
        self.assertEqual(sender.smtp_server, 'smtp.example.com')

if __name__ == '__main__':
    unittest.main()
