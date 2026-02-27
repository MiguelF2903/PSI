<!-- App.vue -->
<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>Personas</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <formulario-persona @add-persona="agregarPersona" />
        <tabla-personas
          :personas="personas"
          @delete-persona="eliminarPersona"
          @actualizar-persona="actualizarPersona"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
// Importacion del componente 'TablaPersonas', 'FormularioPersona' y el metodo 'ref' de Vue 3
import TablaPersonas from "@/components/TablaPersonas.vue";
import FormularioPersona from "@/components/FormularioPersona.vue";
import { ref } from "vue";

// Declaracion de una variable reactiva "personas" usando "ref"
const personas = ref([
  {
    id: 1,
    nombre: "Jon",
    apellido: "Nieve",
    email: "jon@email.com",
  },
  {
    id: 2,
    nombre: "Tyrion",
    apellido: "Lannister",
    email: "tyrion@email.com",
  },
  {
    id: 3,
    nombre: "Daenerys",
    apellido: "Targaryen",
    email: "daenerys@email.com",
  },
]);
// Definimos una funcion de nombre agregaPersona que agrega una nueva persona al array
const agregarPersona = (persona) => {
  let id = 0;
  if (personas.value.length > 0) {
    id = personas.value[personas.value.length - 1].id + 1;
  }
  // Actualizamos el valor del array creando un nuevo array con los valores existenstes y agregando la nueva persona
  personas.value = [...personas.value, { ...persona, id }];
};

// Definimos una nueva funcion para eliminar personas del array
const eliminarPersona = (id) => {
  try {
    personas.value = personas.value.filter((u) => u.id !== id);
  } catch (error) {
    console.error(error);
  }
};

// Definimos una funcion para que se guarden los cambios depues de una edicion
const actualizarPersona = (id, personaActualizada) => {
  try {
    personas.value = personas.value.map((persona) =>
      persona.id === id ? personaActualizada : persona
    );
  } catch (error) {
    console.error(error);
  }
};
</script>

<style>
/* Estilos globales para todos los elementos button en la aplicacion */
button {
  background: #009435;
  border: 1px solid #009435;
}
</style>
