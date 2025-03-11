import { type Actions, redirect } from "@sveltejs/kit";
import { loginForAccessToken } from "$lib/api/auth";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		await loginForAccessToken({
			username: data.get("username")!.toString(),
			password: data.get("password")!.toString(),
		});
		redirect(302, "/");
	},
} satisfies Actions;
