<template>
    <section>
        <b-field label="Nome">
            <b-input minlength ="1" maxlength="50" required placeholder="Nome do Campus" type="text"></b-input>
        </b-field>

        <b-field label="CNPJ">
            <b-input minlength="18" maxlength="18" required placeholder="CNPJ do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Endereço">
            <b-input minlength="1" maxlength="75" required placeholder="Endereço do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Número">
            <b-input minlength="1" maxlength="10" required placeholder="Número do Campus" type="text"></b-input>
        </b-field>

        <b-field label="Website">
            <b-input maxlength="50" placeholder="Site do Campus" type="url"></b-input>
        </b-field>

        <b-field label="Localização">
            <b-select placeholder="Selecione a Localização">
                <option value="sc">SC</option>
                <option value="rj">RJ</option>
                <option value="pr">PR</option>
                <option value="sp">SP</option>
                <option value="ac">AC</option>   
            </b-select>
        </b-field>

        <b-field label="Selecione a Instituição">
            <b-select placeholder="Selecione a Instituição">
                <option value="ifsc">IFSC</option>
                <option value="ifrj">IFRJ</option>
                <option value="ifpr">IFPR</option>
                <option value="ifsp">IFSP</option>
                <option value="ifac">IFAC</option>   
            </b-select>
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
