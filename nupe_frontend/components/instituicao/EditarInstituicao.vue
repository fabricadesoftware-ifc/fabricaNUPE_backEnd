<template>
<!--Adicionar edição de id-->
    <section>
        <b-field label="Nome">
            <b-input value="valorDoBanco" minlength ="1" maxlength="50" required placeholder="Nome do Campus" type="text"></b-input>
        </b-field>

        <b-button @click="clickMe">Editar</b-button>
        
        
    </section>
</template>

<script>
    export default {
        methods: {
            clickMe() {
                this.$buefy.notification.open('Editado com Sucesso!')
            }
        }
    }
</script>

