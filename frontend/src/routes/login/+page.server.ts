import { type Actions, fail, redirect } from "@sveltejs/kit";
import type { UserLogin } from "$lib/api/types/user";
import { apiClient } from "$lib/api/client";

export const actions = {
	default: async ({ fetch, cookies, request }) => {
		const formData = await request.formData();
		const loginData: UserLogin = {
			username: formData.get("username") as string,
			password: formData.get("password") as string,
		};
		try {
			await apiClient.login(fetch, cookies, loginData);
		} catch (e) {
			console.error("Login failed:", e);
			return fail(400, {
				error: "Invalid username or password",
				details: { TODO: "fill this" },
			});
		}
		console.log("Login successful, redirecting...");
		throw redirect(303, "/");
	},
} satisfies Actions;
