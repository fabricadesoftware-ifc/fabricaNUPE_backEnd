<template>
<!-- Adiconar uma ID unica -->
    <section>

    
        <b-field label="Nome">
            <b-input minlength ="1" maxlength="50" required placeholder="Nome do Campus" type="text"></b-input>
        </b-field>

        

        <b-button @click="clickMe">Cadastrar</b-button>
    
        
    </section>
</template>

<script>
    export default {
        methods: {
            clickMe() {
                this.$buefy.notification.open('Cadastrado com Sucesso!')
            }
        }
    }
</script>
