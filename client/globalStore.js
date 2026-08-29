import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
  const config = ref({});
  const encryptionPassphrase = ref(null);

  function lockEncryptedNotes() {
    encryptionPassphrase.value = null;
  }

  return { config, encryptionPassphrase, lockEncryptedNotes };
});
