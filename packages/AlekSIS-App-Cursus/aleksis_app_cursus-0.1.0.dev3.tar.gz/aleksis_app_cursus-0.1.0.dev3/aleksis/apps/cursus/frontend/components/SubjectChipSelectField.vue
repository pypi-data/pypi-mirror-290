<script setup>
import ForeignKeyChipSelectField from "aleksis.core/components/generic/forms/ForeignKeyChipSelectField.vue";
// eslint-disable-next-line no-unused-vars
import CreateSubject from "./CreateSubject.vue";
import SubjectChip from "./SubjectChip.vue";
</script>

<template>
  <foreign-key-chip-select-field
    v-bind="$attrs"
    v-on="$listeners"
    :fields="headers"
    create-item-i18n-key="cursus.subject.create"
    :gql-query="gqlQuery"
    :gql-create-mutation="gqlCreateMutation"
    :gql-patch-mutation="{}"
    :default-item="defaultItem"
    :get-create-data="getCreateData"
    :get-patch-data="getPatchData"
    :background-color="$attrs['value'].colourBg"
    :color="$attrs['value'].colourFg"
    return-object
  >
    <template #item="{ item }">
      <subject-chip :subject="item" :style="{ cursor: 'pointer' }" />
    </template>
    <template #selection="{ item }">
      <span :style="{ color: item.colourFg }">{{ item.name }}</span>
    </template>
    <template #createComponent="{ attrs, on, createMode }">
      <create-subject v-bind="attrs" v-on="on" />
    </template>
  </foreign-key-chip-select-field>
</template>

<script>
import SubjectField from "./SubjectField.vue";

export default {
  name: "SubjectChipSelectField",
  extends: SubjectField,
};
</script>

<style scoped></style>
