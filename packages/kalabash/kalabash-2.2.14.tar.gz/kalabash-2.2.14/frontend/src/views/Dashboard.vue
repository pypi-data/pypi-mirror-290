<template>
  <v-toolbar flat>
    <v-toolbar-title>{{ $gettext('Welcome to Kalabash') }}</v-toolbar-title>
  </v-toolbar>
  <v-alert type="info" border="top" colored-border elevation="2" class="mt-10">
    <p>
      {{
        $gettext(
          "This page presents a summary of your Kalabash server's status and some useful information about the product."
        )
      }}
    </p>
  </v-alert>
</template>

<style scoped>
.v-toolbar {
  background-color: #f7f8fa !important;
}

.v-tabs-items {
  background-color: #f7f8fa !important;
}
</style>
