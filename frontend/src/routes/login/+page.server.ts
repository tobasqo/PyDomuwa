import { type Actions, error, fail, redirect } from "@sveltejs/kit";
import { loginForAccessToken } from "$lib/api/auth";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const err = await loginForAccessToken(
			{
				username: data.get("username")!.toString(),
				password: data.get("password")!.toString(),
			},
			cookies,
		);
		if (err !== undefined) {
			if (err.status === 400 || err.status === 401 || err.status === 422) {
				return fail(err.status, {
					error: err.message,
					details: err.details(),
				});
			}
			throw error(err.status, err);
		}
		throw redirect(303, "/");
	},
} satisfies Actions;
