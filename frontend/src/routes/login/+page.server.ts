import { type Actions, redirect } from "@sveltejs/kit";
import { apiClient } from "$lib/api/client";

export const actions = {
	default: async ({ fetch, cookies, request }) => {
		const formData = await request.formData();
		const loginData = {
			username: formData.get("username") as string,
			password: formData.get("password") as string,
		};
		const fail = await apiClient.login(fetch, cookies, loginData);
		if (fail !== null) {
			console.log("Login failed:", fail);
			return fail;
		}
		console.log("Login successful, redirecting...");
		throw redirect(303, "/");
	},
} satisfies Actions;
