# 💳 CredCrud
## Microsserviço de cadastro de cartões de crédito simples - pun intended 😅

Este projeto será montado apenas para fins de estudo. O mesmo trabalhará em cima do FastAPI e utilizando boas práticas.

## 🧭 Requisitos técnicos
* Será necessário cadastrar os dados do cartão;
* Faz-se necessário a utilização da biblioteca [MaisTodos/python-creditcard]( https://github.com/MaisTodos/python-creditcard) para a validação da numeração do cartão.
  * Vale ressaltar que se faz necessário a configuração dos outros dados, como Data de expiração, CVV, etc.
* Os dado da numeração do cartão precisa estar criptografado.
* A API precisa estar protegida por meio de credenciais.

# 🛠️ Estratégia de trabalho
Para o desafio acima proposto, será adotado o microframework FastAPI e como persistencia de dados será utilizado SQLAlchemy com Alembic. Como possuo pouco tempo disponível para o projeto, tentarei fazer tradeoffs de modo a não ter prejuízo no desenvolvimento.

Criei [um arquivo de log](CHANGELOG.md) onde eu descreverei o conjunto de ações tomadas de modo a chegar no objetivo final.

**Observação**: Caso seja necessário eu avaliarei se manterei essa estratégia. Caso haja modificação do plano, eu irei documentando aqui prontamente, assim como explicando o motivo para tal ação.

# 🫡 Humanos

* Jon Trigueiro - [jon.dev.br](https://jon.dev.br)
