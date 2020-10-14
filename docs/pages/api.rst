===================
Documentação da API
===================

Informações Relevantes
----------------------

Por padrão quando o container é iniciado o backend estará rodando no endereço **localhost:8000/**.

Mas caso você esteja dentro do container e deseje executar manualmente, utilize:

.. code-block:: console

   $ ./manage.py runserver 0:8000

ou o comando seguinte, para popular o banco de dados com o super usuário padrão e os outros dados base da aplicação:

.. code-block:: console

   $ ./manage.py populate

Se não estiver dentro do container, execute em um novo terminal:

.. code-block:: console

   $ docker container exec -d dev_backend bash -c "./manage.py runserver 0:8000"

ou

.. code-block:: console

   $ docker container exec -d dev_backend bash -c "./manage.py populate"

Super Usuário Padrão:
+++++++++++++++++++++

   Email: nupexample@example.com

   Senha: nuperoot

Endpoints
---------

.. raw:: html

   <iframe src="redoc_api.html" width="100%" height="500"></iframe>

   <style>
      div.document {
         width: auto;
         margin: 30px 0 0 15%;
      }
      div.body {
         max-width: none;
      }
   </style>
