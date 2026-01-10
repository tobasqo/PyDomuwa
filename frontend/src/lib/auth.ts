import { writable } from "svelte/store";
import type { JWTToken } from "$lib/api/types/jwt";

// TODO: store here info about user, not in the localStorage
const jwtToken = localStorage.getItem("jwt");

export const jwtStore = writable<JWTToken>(jwtToken ? JSON.parse(jwtToken) : null);

jwtStore.subscribe((token) => {
  if (token) {
    localStorage.setItem("jwt", JSON.stringify(token));
  } else {
    localStorage.removeItem("jwt");
  }
});
