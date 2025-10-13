import { type Actions, error, fail, redirect } from "@sveltejs/kit";
import { loginForAccessToken } from "$lib/api/auth";
import { getFreshAxiosInstance } from "$lib/api";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const axiosInstance = getFreshAxiosInstance();
		const err = await loginForAccessToken(
			axiosInstance,
			{
				username: data.get("username")!.toString(),
				password: data.get("password")!.toString(),
			},
			cookies,
		);
		if (err !== null) {
			if (err.status === 400 || err.status === 401 || err.status === 422) {
				return fail(err.status, { error: err.message, details: err.details() });
			}
			throw error(err.status, err);
		}
		throw redirect(303, "/");
	},
} satisfies Actions;
