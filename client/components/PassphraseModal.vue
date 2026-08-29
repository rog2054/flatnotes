<template>
  <Modal v-model="isVisible" class="px-6 py-4">
    <form @submit.prevent="submit">
      <div class="mb-2 text-xl">{{ title }}</div>
      <div v-if="message" class="mb-4 text-sm text-theme-text-muted">
        {{ message }}
      </div>
      <label class="mb-1 block text-sm" for="note-passphrase">Passphrase</label>
      <input
        id="note-passphrase"
        ref="passphraseInput"
        v-model="passphrase"
        type="password"
        autocomplete="off"
        class="mb-3 w-full rounded-md border border-theme-border bg-theme-background px-3 py-2 focus:outline-none dark:bg-theme-background-elevated"
      />
      <template v-if="confirmPassphrase">
        <label class="mb-1 block text-sm" for="note-passphrase-confirm">
          Confirm passphrase
        </label>
        <input
          id="note-passphrase-confirm"
          v-model="confirmation"
          type="password"
          autocomplete="off"
          class="mb-3 w-full rounded-md border border-theme-border bg-theme-background px-3 py-2 focus:outline-none dark:bg-theme-background-elevated"
        />
      </template>
      <div v-if="validationError" class="mb-3 text-sm text-red-500">
        {{ validationError }}
      </div>
      <div class="flex justify-end">
        <CustomButton
          label="Cancel"
          style="subtle"
          class="mr-2"
          @click="close"
        />
        <button
          type="submit"
          class="rounded px-3 py-2 text-theme-brand hover:bg-theme-background-elevated"
        >
          {{ confirmButtonText }}
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { nextTick, ref, watch } from "vue";

import CustomButton from "./CustomButton.vue";
import Modal from "./Modal.vue";

const props = defineProps({
  title: { type: String, default: "Unlock encrypted note" },
  message: String,
  confirmButtonText: { type: String, default: "Unlock" },
  confirmPassphrase: Boolean,
  initialPassphrase: String,
});
const emit = defineEmits(["submit"]);
const isVisible = defineModel({ type: Boolean });
const passphrase = ref("");
const confirmation = ref("");
const validationError = ref("");
const passphraseInput = ref();

watch(isVisible, (visible) => {
  if (visible) {
    passphrase.value = props.initialPassphrase || "";
    confirmation.value = "";
    validationError.value = "";
    nextTick(() => passphraseInput.value?.focus());
  } else {
    clear();
  }
});

function submit() {
  if (!passphrase.value) {
    validationError.value = "Enter a passphrase.";
    return;
  }
  if (props.confirmPassphrase && passphrase.value !== confirmation.value) {
    validationError.value = "Passphrases do not match.";
    return;
  }
  const submittedPassphrase = passphrase.value;
  isVisible.value = false;
  emit("submit", submittedPassphrase);
  clear();
}

function close() {
  isVisible.value = false;
  clear();
}

function clear() {
  passphrase.value = "";
  confirmation.value = "";
  validationError.value = "";
}
</script>
