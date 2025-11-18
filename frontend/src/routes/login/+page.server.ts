import { type Actions, fail, isHttpError, redirect } from "@sveltejs/kit";
import { apiClient } from "$lib/api/client";

export const actions = {
	default: async ({ fetch, cookies, request }) => {
		const formData = await request.formData();
		const loginData = {
			username: formData.get("username") as string,
			password: formData.get("password") as string,
		};
		try {
			await apiClient.login(fetch, cookies, loginData);
		} catch (e) {
			console.error("Login failed:", e);
			if (isHttpError(e)) {
				return fail(400, {
					error: "Invalid username or password",
					details: e.body,
				});
			}
			throw e;
		}
		console.log("Login successful, redirecting...");
		throw redirect(303, "/");
	},
} satisfies Actions;
