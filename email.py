"""Mover e-mails enviados contendo "ALERTA" no assunto para a lixeira.

Este módulo busca e-mails enviados pelo usuário para clientes na caixa
"Sent" do Gmail. E-mails endereçados ao cliente e contendo "ALERTA" no
assunto são movidos para a pasta Lixeira. Variáveis de ambiente EMAIL,
EMAIL_PASSWORD e CLIENT_EMAIL devem estar definidas.

Autor: Renan Rodrigues
Data: 2025
"""

import os

import imap_tools


def read_emails_and_delete():
    with imap_tools.MailBox("imap.gmail.com").login(
        os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"), "SENT"
    ) as mailbox:
        for msg in mailbox.fetch(
            imap_tools.AND(to=os.getenv("CLIENT_EMAIL")),
            sort="DATE",
            reverse=True,
            mark_seen=False,
        ):
            print(f"From: {msg.from_} To: {msg.to} Date: {msg.date}")
            print(f"Subject: {msg.subject}\nMessage: {msg.text}")
            if msg.to == os.getenv("CLIENT_EMAIL") and "ALERTA" in msg.subject:
                print(f"This email is to {msg.to}. Then deleting it.")
                mailbox.move(msg.uid, "Trash")
                print("Email deleted successfully.")
        mailbox.expunge()
