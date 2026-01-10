import { type Actions, fail, redirect } from "@sveltejs/kit";
import { apiClient } from "$lib/api/client";

export const actions = {
  default: async ({ fetch, cookies, request }) => {
    const formData = await request.formData();
    try {
      await apiClient.createUser(fetch, cookies, {
        username: formData.get("username")!.toString(),
        password: formData.get("password")!.toString(),
      });
    } catch (err: any) {
      return fail(500, {
        error: "Registration failed. Please try again.",
        details: err,
      });
    }
    throw redirect(303, "/login");
  },
} satisfies Actions;
