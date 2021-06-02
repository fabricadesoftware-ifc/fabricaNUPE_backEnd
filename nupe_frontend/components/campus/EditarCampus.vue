<template>
    <section>
        <b-field label="Nome">
            <b-input :value="valor.nome" minlength ="1" maxlength="50" required placeholder="Nome do Campus" type="text"></b-input>
        </b-field>

        <b-field label="CNPJ">
            <b-input :value="valor.cnpj" minlength="18" maxlength="18" required placeholder="CNPJ do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Endereço">
            <b-input value="valorDoBanco" minlength="1" maxlength="75" required placeholder="Endereço do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Número">
            <b-input value="valorDoBanco" minlength="1" maxlength="10" required placeholder="Número do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Website">
            <b-input value="valorDoBanco" maxlength="50" placeholder="Site do Campus" type="url"></b-input>
        </b-field>

        <b-field label="Localização">
            <b-select value="valorDoBanco" placeholder="Selecione a Localização">
                <option value="sc">SC</option>
                <option value="rj">RJ</option>
                <option value="pr">PR</option>
                <option value="sp">SP</option>
                <option value="ac">AC</option>   
            </b-select>
        </b-field>

        <b-field label="Selecione a Instituição">
            <b-select value="valorDoBanco" placeholder="Selecione a Instituição">
                <option value="ifsc">IFSC</option>
                <option value="ifrj">IFRJ</option>
                <option value="ifpr">IFPR</option>
                <option value="ifsp">IFSP</option>
                <option value="ifac">IFAC</option>   
            </b-select>
        </b-field>

        <b-button @click="clickMe">Editar</b-button>
        
        
    </section>
</template>

<script>
    export default {
        props:{
            valor: Object
        },
        methods: {
            clickMe() {
                this.$buefy.notification.open('Editado com Sucesso!')
            }
        }
    }
</script>

