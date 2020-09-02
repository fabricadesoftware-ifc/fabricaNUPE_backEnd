===================
Documentação da API
===================

Informações Relevantes
----------------------

Por padrão quando o container é iniciado a aplicação estará rodando no endereço **localhost:80** ou apenas **localhost**

Mas caso deseje executar manualmente, utilize:

.. code-block:: console

   $ ./manage.py runserver 0:8000

Super Usuário Padrão:
+++++++++++++++++++++

   Username: nupexample

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